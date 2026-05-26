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
    try:
        data = request.get_json()
        if not data:
            return jsonify({'status': 'error', 'error': 'No data received'}), 400
        
        # Convert empty string to None for customer_id (walk-in customers)
        customer_id_raw = data.get('customer_id')
        customer = int(customer_id_raw) if customer_id_raw else None
        
        payment = data.get('payment_method')
        discounttype = data.get('discount_type')
        discountvalue = float(data.get('discount_value', 0) or 0)
        gsttype = data.get('gst_type')
        subtotal = float(data.get('subtotal', 0) or 0)
        discountamount = float(data.get('discount_amount', 0) or 0)
        cgst = float(data.get('cgst', 0) or 0)
        sgst = float(data.get('sgst', 0) or 0)
        igst = float(data.get('igst', 0) or 0)
        finaltotal = float(data.get('final_total', 0) or 0)
        items = data.get('items', [])
        
        # Validate items
        if not items or len(items) == 0:
            return jsonify({'status': 'error', 'error': 'No items in bill'}), 400
        
        connection = get_db()
        if not connection:
            return jsonify({'status': 'error', 'error': 'Database connection error'}), 500
        
        with connection.cursor() as cur:
            try:
                bill_number = generate_bill_number()
                gst_amount = cgst + sgst + igst
                
                cur.execute("""
                    INSERT INTO bills (customer_id, bill_number, total_amount, discount_type, 
                                     discount_value, discount_amount, gst_type, cgst_amount, 
                                     sgst_amount, igst_amount, gst_amount, final_amount, payment_method)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """, (customer, bill_number, subtotal, discounttype, discountvalue,
                      discountamount, gsttype, cgst, sgst, igst, gst_amount, finaltotal, payment))
                
                billid = cur.lastrowid
                
                # Insert items and update stock
                for item in items:
                    product_id = item.get('product_id')
                    qty = int(item.get('qty', 0) or 0)
                    price = float(item.get('price', 0) or 0)
                    total = float(item.get('total', 0) or 0)
                    
                    # Check stock
                    cur.execute("SELECT stock FROM products WHERE id = %s", (product_id,))
                    stock_data = cur.fetchone()
                    
                    if not stock_data:
                        connection.rollback()
                        return jsonify({'status': 'error', 'error': f"Product ID {product_id} not found"}), 400
                    
                    current_stock = int(stock_data[0]) if stock_data[0] else 0
                    if current_stock < qty:
                        connection.rollback()
                        return jsonify({'status': 'error', 'error': f"Insufficient stock for Product ID {product_id}"}), 400
                    
                    # Insert bill item
                    cur.execute("""
                        INSERT INTO bill_items (bill_id, product_id, quantity, unit_price, total_price)
                        VALUES (%s,%s,%s,%s,%s)
                    """, (billid, product_id, qty, price, total))
                    
                    # Update stock
                    cur.execute("UPDATE products SET stock = stock - %s WHERE id = %s", 
                               (qty, product_id))
                
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
    
    except Exception as e:
        print(f"ERROR in createbill outer: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'status': 'error', 'error': str(e)}), 500

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
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "error": "No data received"}), 400

        # Convert empty string to None for customer_id (walk-in customers)
        customer_id_raw = data.get("customer_id")
        customer_id = int(customer_id_raw) if customer_id_raw else None
        payment_method = data.get("payment_method")
        discount_type = data.get("discount_type")
        discount_value = float(data.get("discount_value", 0) or 0)
        gst_type = data.get("gst_type")
        subtotal = float(data.get("subtotal", 0) or 0)
        discount_amount = float(data.get("discount_amount", 0) or 0)
        cgst = float(data.get("cgst", 0) or 0)
        sgst = float(data.get("sgst", 0) or 0)
        igst = float(data.get("igst", 0) or 0)
        final_total = float(data.get("final_total", 0) or 0)
        items = data.get("items", [])

        if not items or len(items) == 0:
            return jsonify({"status": "error", "error": "No items in bill"}), 400

        status = "Payment Pending"
        
        connection = get_db()
        if not connection:
            return jsonify({"status": "error", "error": "Database connection error"}), 500
        
        with connection.cursor() as cur:
            try:
                bill_number = generate_bill_number()
                gst_amount = cgst + sgst + igst
                
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
                    product_id = item.get('product_id')
                    qty = int(item.get('qty', 0) or 0)
                    price = float(item.get('price', 0) or 0)
                    total = float(item.get('total', 0) or 0)
                    
                    cur.execute("""
                        INSERT INTO bill_items (bill_id, product_id, quantity, unit_price, total_price)
                        VALUES (%s,%s,%s,%s,%s)
                    """, (
                        bill_id,
                        product_id,
                        qty,
                        price,
                        total
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
    
    except Exception as e:
        print(f"ERROR in save_draft outer: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"status": "error", "error": str(e)}), 500