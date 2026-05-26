from flask import Blueprint, request, jsonify
from flask_login import login_required
from app.db import get_db
import pymysql
import json
import os

api_bp = Blueprint('api', __name__)

@api_bp.route('/products')
@login_required
def api_products():
    connection = get_db()
    if not connection:
        return jsonify({'error': 'Database connection error'}), 500
    
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cur:
            cur.execute("SELECT id, name, price, stock FROM products WHERE stock > 0")
            products = cur.fetchall()
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        connection.close()
    
    products_list = []
    for product in products:
        products_list.append({
            'id': product['id'],
            'name': product['name'],
            'price': float(product['price']),
            'stock': product['stock']
        })
    
    return jsonify(products_list)

@api_bp.route('/products/search')
@login_required
def search_products():
    query = request.args.get('q', '')
    connection = get_db()
    if not connection:
        return jsonify({'error': 'Database connection error'}), 500
    
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cur:
            cur.execute("SELECT id, name, price, stock FROM products WHERE name LIKE %s", (f'%{query}%',))
            rows = cur.fetchall()
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        connection.close()

    products = []
    for r in rows:
        products.append({
            "id": r['id'],
            "name": r['name'],
            "price": float(r['price']),
            "stock": r['stock']
        })

    return jsonify(products)

@api_bp.route('/product/lookup')
@login_required
def api_product_lookup():
    q = request.args.get('q', '').strip()
    if not q:
        return jsonify([])

    connection = get_db()
    if not connection:
        return jsonify({'error': 'Database connection error'}), 500

    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cur:
            rows = []
            if q.isdigit():
                cur.execute("SELECT id, name, price, stock FROM products WHERE id = %s", (q,))
                row = cur.fetchone()
                if row:
                    rows = [row]
            else:
                cur.execute("""
                    SELECT id, name, price, stock
                    FROM products
                    WHERE name LIKE %s
                    ORDER BY name ASC
                    LIMIT 10
                """, (f"%{q}%",))
                rows = cur.fetchall()
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        connection.close()

    result = []
    for r in rows:
        result.append({
            "id": int(r["id"]),
            "name": r["name"],
            "price": float(r["price"]),
            "stock": int(r["stock"]),
        })
    return jsonify(result)

@api_bp.route('/customers')
@login_required
def api_customers():
    connection = get_db()
    if not connection:
        return jsonify({'error': 'Database connection error'}), 500
    
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cur:
            cur.execute("SELECT id, name, phone, email, address FROM customers ORDER BY name")
            customers = cur.fetchall()
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        connection.close()
    
    # Convert to list of dictionaries for JSON response
    customers_list = []
    for customer in customers:
        customers_list.append({
            'id': customer['id'],
            'name': customer['name'],
            'phone': customer['phone'],
            'email': customer['email'],
            'address': customer['address']
        })
    
    return jsonify(customers_list)

@api_bp.route('/customers/quick-add', methods=['POST'])
@login_required
def quick_add_customer():
    try:
        data = request.get_json()
        name = data.get('name')
        phone = data.get('phone', '')
        email = data.get('email', '')
        address = data.get('address', '')
        
        if not name:
            return jsonify({'success': False, 'error': 'Name is required'})
        
        connection = get_db()
        if not connection:
            return jsonify({'success': False, 'error': 'Database connection error'}), 500
        
        try:
            with connection.cursor() as cur:
                cur.execute("INSERT INTO customers (name, phone, email, address) VALUES (%s, %s, %s, %s)",
                           (name, phone, email, address))
                customer_id = cur.lastrowid
                connection.commit()
                
                # Fetch the inserted customer
                cur.execute("SELECT id, name, phone, email, address FROM customers WHERE id = %s", (customer_id,))
                customer = cur.fetchone()
        except Exception as e:
            connection.rollback()
            return jsonify({'success': False, 'error': str(e)})
        finally:
            connection.close()
        
        return jsonify({
            'success': True,
            'customer': {
                'id': customer['id'],
                'name': customer['name'],
                'phone': customer['phone'],
                'email': customer['email'],
                'address': customer['address']
            }
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@api_bp.route('/bill/<int:bill_id>/items/count')
@login_required
def bill_items_count(bill_id):
    connection = get_db()
    if not connection:
        return jsonify({'error': 'Database connection error'}), 500
    
    try:
        with connection.cursor() as cur:
            cur.execute("SELECT COUNT(*) as item_count FROM bill_items WHERE bill_id = %s", (bill_id,))
            result = cur.fetchone()
            item_count = result[0] if result else 0
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        connection.close()
    
    return jsonify({'item_count': item_count})

@api_bp.route('/customer/<int:customer_id>/stats')
@login_required
def customer_stats(customer_id):
    connection = get_db()
    if not connection:
        return jsonify({'error': 'Database connection error'}), 500
    
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cur:
            cur.execute("SELECT COUNT(*) as total_bills FROM bills WHERE customer_id = %s", (customer_id,))
            result = cur.fetchone()
            bill_count = result['total_bills'] if result else 0
            
            cur.execute("SELECT COALESCE(SUM(final_amount), 0) as total_spent FROM bills WHERE customer_id = %s", (customer_id,))
            result = cur.fetchone()
            total_spent = result['total_spent'] if result else 0
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        connection.close()
    
    return jsonify({
        'total_bills': bill_count,
        'total_spent': float(total_spent)
    })

@api_bp.route('/billing/stats')
@login_required
def billing_stats():
    connection = get_db()
    if not connection:
        return jsonify({'error': 'Database connection error'}), 500
    
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cur:
            cur.execute("SELECT COUNT(*) as today_bills FROM bills WHERE DATE(created_at) = CURDATE()")
            result = cur.fetchone()
            today_bills = result['today_bills'] if result else 0
            
            cur.execute("SELECT COUNT(*) as low_stock FROM products WHERE stock < 5")
            result = cur.fetchone()
            low_stock = result['low_stock'] if result else 0
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        connection.close()
    
    return jsonify({
        'today_bills': today_bills,
        'low_stock': low_stock
    })

@api_bp.route('/products/barcode/<barcode>')
@login_required
def search_product_by_barcode(barcode):
    connection = get_db()
    if not connection:
        return jsonify({'success': False, 'error': 'Database connection error'}), 500
    
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cur:
            cur.execute("SELECT * FROM products WHERE barcode = %s AND stock > 0", (barcode,))
            product = cur.fetchone()
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        connection.close()
    
    if product:
        return jsonify({
            'success': True,
            'product': {
                'id': product['id'],
                'name': product['name'],
                'price': float(product['price']),
                'stock': product['stock']
            }
        })
    else:
        return jsonify({'success': False, 'error': 'Product not found'})

@api_bp.route('/import-customers')
def import_customers():
    try:
        # Go to project root
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

        json_path = os.path.join(project_root, "Json", "customers_name.json")

        print("JSON PATH:", json_path)

        if not os.path.exists(json_path):
            return jsonify({"success": False, "error": f"File not found: {json_path}"}), 404

        with open(json_path, "r", encoding="utf-8") as f:
            customers = json.load(f)

        connection = get_db()
        if not connection:
            return jsonify({"success": False, "error": "Database connection error"}), 500

        try:
            with connection.cursor() as cur:
                for c in customers:
                    cur.execute("""
                        INSERT IGNORE INTO customers (name, phone, email, address)
                        VALUES (%s, %s, %s, %s)
                    """, (
                        c.get("name", ""),
                        c.get("phone", ""),
                        c.get("email", ""),
                        c.get("address", "")
                    ))

                connection.commit()

        except Exception as e:
            connection.rollback()
            return jsonify({"success": False, "error": str(e)}), 500
        finally:
            connection.close()

        return jsonify({"success": True, "message": "Customers imported successfully!"})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@api_bp.route('/import-json-products')
def import_json_products():
    try:
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

        json_path = os.path.join(project_root, "Json", "products_name.json")

        print("JSON PATH:", json_path)

        with open(json_path, "r", encoding="utf-8") as f:
            products = json.load(f)

        connection = get_db()
        if not connection:
            return jsonify({"success": False, "error": "Database connection error"}), 500

        try:
            with connection.cursor() as cur:
                for p in products:
                    cur.execute("""
                        INSERT INTO products (name, price, stock)
                        VALUES (%s, %s, %s)
                    """, (p["name"], p["price"], p["stock"]))

                connection.commit()

        except Exception as e:
            connection.rollback()
            return jsonify({"success": False, "error": str(e)}), 500
        finally:
            connection.close()

        return jsonify({"success": True, "message": "Products imported successfully!"})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

    try:
        # Get the correct path to JSON file
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        json_path = os.path.join(project_root, "Json", "customers_name.json")
        
        print(f"Looking for JSON file at: {json_path}")  # Debug line

        with open(json_path, "r", encoding="utf-8") as f:
            customers = json.load(f)

        connection = get_db()
        if not connection:
            return jsonify({"success": False, "error": "Database connection error"}), 500

        try:
            with connection.cursor() as cur:
                # Try to add UNIQUE constraint (ignore if exists)
                try:
                    cur.execute("ALTER TABLE customers ADD UNIQUE(name, phone);")
                    connection.commit()
                except:
                    pass  # Constraint might already exist

                for c in customers:
                    cur.execute("""
                        INSERT IGNORE INTO customers (name, phone, email, address)
                        VALUES (%s, %s, %s, %s)
                    """, (c["name"], c["phone"], c["email"], c["address"]))
                
                connection.commit()
        except Exception as e:
            connection.rollback()
            return jsonify({"success": False, "error": str(e)}), 500
        finally:
            connection.close()

        return jsonify({"success": True, "message": "Customers imported successfully!"})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})