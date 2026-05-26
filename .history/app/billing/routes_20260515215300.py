from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required
from app.db import get_db
from app.utils.helpers import generate_bill_number
import datetime
import pymysql

billing_bp = Blueprint('billing', __name__)

@billing_bp.route('/')
@login_required
def billing():
    connection = get_db()
    if not connection:
        flash('Database connection error', 'danger')
        return render_template('billing/billing.html', products=[], customers=[])
    
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cur:
            cur.execute("SELECT * FROM products WHERE stock > 0 ORDER BY name")
            products = cur.fetchall()
            
            cur.execute("SELECT * FROM customers ORDER BY name")
            customers = cur.fetchall()
    except Exception as e:
        flash(f'Database error: {str(e)}', 'danger')
        products = []
        customers = []
    finally:
        connection.close()
    
    return render_template('billing/billing.html', products=products, customers=customers)

@billing_bp.route('/create', methods=['POST'])
@login_required
def create_bill():
    data = request.get_json()
    customer_id = data.get('customer_id')
    items = data.get('items', [])
    payment_method = data.get('payment_method', 'Cash')
    
    subtotal = sum(item['quantity'] * item['price'] for item in items)
    gst_amount = subtotal * 0.18
    final_amount = subtotal + gst_amount
    
    connection = get_db()
    if not connection:
        return jsonify({'success': False, 'error': 'Database connection error'}), 500
    
    try:
        with connection.cursor() as cur:
            bill_number = generate_bill_number()
            cur.execute("""
                INSERT INTO bills (customer_id, bill_number, total_amount, gst_amount, final_amount, payment_method) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (customer_id, bill_number, subtotal, gst_amount, final_amount, payment_method))
            
            bill_id = cur.lastrowid
            
            for item in items:
                cur.execute("""
                    INSERT INTO bill_items (bill_id, product_id, quantity, unit_price, total_price) 
                    VALUES (%s, %s, %s, %s, %s)
                """, (bill_id, item['product_id'], item['quantity'], item['price'], item['quantity'] * item['price']))
                
                cur.execute("UPDATE products SET stock = stock - %s WHERE id = %s", 
                           (item['quantity'], item['product_id']))
            
            connection.commit()
            
        return jsonify({'success': True, 'bill_id': bill_id, 'bill_number': bill_number})
    except Exception as e:
        connection.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        connection.close()

@billing_bp.route('/createbill', methods=['POST'])
def createbill_api():
    data = request.get_json()
    
    # Convert empty string to None for customer_id (walk-in customers)
    customer = data.get('customer_id') or None
    payment = data.get('payment_method')
    discounttype = data.get('discount_type')
    discountvalue = data.get('discount_value')
    gsttype = data.get('gst_type')
    subtotal = data.get('subtotal')
    discountamount = data.get('discount_amount')
    cgst = data.get('cgst')
    sgst = data.get('sgst')
    igst = data.get('igst')
    finaltotal = data.get('final_total')
    items = data.get('items')
    
    connection = get_db()
    if not connection:
        return jsonify({'status': 'error', 'error': 'Database connection error'}), 500
    
    try:
        with connection.cursor() as cur:
            bill_number = generate_bill_number()
            gst_amount = float(cgst or 0) + float(sgst or 0) + float(igst or 0)
            
            cur.execute("""
                INSERT INTO bills (customer_id, bill_number, total_amount, discount_type, 
                                 discount_value, discount_amount, gst_type, cgst_amount, 
                                 sgst_amount, igst_amount, gst_amount, final_amount, payment_method)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """, (customer, bill_number, subtotal, discounttype, discountvalue,
                  discountamount, gsttype, cgst, sgst, igst, gst_amount, finaltotal, payment))
            
            billid = cur.lastrowid
            
            for item in items:
                cur.execute("SELECT stock FROM products WHERE id = %s", (item['product_id'],))
                stock_data = cur.fetchone()
                
                if not stock_data:
                    connection.rollback()
                    return jsonify({'status': 'error', 'error': f"Product ID {item['product_id']} not found"}), 400
                
                current_stock = stock_data[0]
                if current_stock < item['qty']:
                    connection.rollback()
                    return jsonify({'status': 'error', 'error': f"Insufficient stock for Product ID {item['product_id']}"}), 400

                cur.execute("""
                    INSERT INTO bill_items (bill_id, product_id, quantity, unit_price, total_price)
                    VALUES (%s,%s,%s,%s,%s)
                """, (billid, item['product_id'], item['qty'], item['price'], item['total']))

                cur.execute("""
                    UPDATE products
                    SET stock = stock - %s
                    WHERE id = %s
                """, (item['qty'], item['product_id']))
            
            connection.commit()
            
            return jsonify({'status': 'success', 'bill_id': billid})
        
    except Exception as e:
        connection.rollback()
        print(f"ERROR in createbill: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'status': 'error', 'error': str(e)}), 400
    finally:
        connection.close()

@billing_bp.route("/createbill.html")
def createbill_success_page():
    return render_template("billing/createbill.html")

@billing_bp.route("/confirm-payment/<int:bill_id>")
@login_required
def confirm_payment(bill_id):
    connection = get_db()
    if not connection:
        flash('Database connection error', 'danger')
        return redirect(url_for('billing.billing'))
    
    try:
        with connection.cursor() as cur:
            cur.execute("SELECT payment_method FROM bills WHERE id=%s", (bill_id,))
            pay = cur.fetchone()
    except Exception as e:
        flash(f'Database error: {str(e)}', 'danger')
        return redirect(url_for('billing.billing'))
    finally:
        connection.close()

    if not pay:
        return "Invalid Bill ID"

    return render_template("billing/confirm.html", bill_id=bill_id, payment_method=pay[0])

@billing_bp.route('/complete-payment/<int:bill_id>', methods=['POST'])
@login_required
def complete_payment(bill_id):
    upi_id = request.form.get("upi_id")
    card_number = request.form.get("card_number")
    card_name = request.form.get("card_name")

    connection = get_db()
    if not connection:
        flash('Database connection error', 'danger')
        return redirect(url_for('billing.billing'))
    
    try:
        with connection.cursor() as cur:
            cur.execute("""
                UPDATE bills 
                SET status='Completed',
                    upi_id=%s,
                    card_number=%s,
                    card_name=%s
                WHERE id=%s
            """, (upi_id, card_number, card_name, bill_id))
            connection.commit()
    except Exception as e:
        flash(f'Database error: {str(e)}', 'danger')
    finally:
        connection.close()

    return redirect(url_for('invoices.print_invoice', bill_id=bill_id))

@billing_bp.route('/savedraft', methods=['POST'])
def save_draft():
    data = request.get_json()

    # Convert empty string to None for customer_id (walk-in customers)
    customer_id = data.get("customer_id") or None
    payment_method = data.get("payment_method")
    discount_type = data.get("discount_type")
    discount_value = data.get("discount_value")
    gst_type = data.get("gst_type")
    subtotal = data.get("subtotal")
    discount_amount = data.get("discount_amount")
    cgst = data.get("cgst")
    sgst = data.get("sgst")
    igst = data.get("igst")
    final_total = data.get("final_total")
    items = data.get("items")

    status = "Payment Pending"
    
    connection = get_db()
    if not connection:
        return jsonify({"status": "error", "error": "Database connection error"}), 500
    
    try:
        with connection.cursor() as cur:
            bill_number = generate_bill_number()
            gst_amount = float(cgst or 0) + float(sgst or 0) + float(igst or 0)
            
            cur.execute("""
                INSERT INTO bills 
                (customer_id, bill_number, total_amount, discount_type, discount_value, discount_amount,
                 gst_type, cgst_amount, sgst_amount, igst_amount, gst_amount, final_amount, payment_method, status)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """, (
                customer_id, bill_number, subtotal, discount_type, discount_value, discount_amount,
                gst_type, cgst, sgst, igst, gst_amount, final_total, payment_method, status
            ))
            bill_id = cur.lastrowid

            for item in items:
                cur.execute("""
                    INSERT INTO bill_items (bill_id, product_id, quantity, unit_price, total_price)
                    VALUES (%s,%s,%s,%s,%s)
                """, (
                    bill_id,
                    item['product_id'],
                    item['qty'],
                    item['price'],
                    item['total']
                ))
            
            connection.commit()
            
        return jsonify({"status": "success", "bill_id": bill_id})
        
    except Exception as e:
        connection.rollback()
        print(f"ERROR in save_draft: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"status": "error", "error": str(e)}), 500
    finally:
        connection.close()