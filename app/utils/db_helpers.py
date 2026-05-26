from flask import current_app
from app import mysql
import MySQLdb
import logging

def get_db_cursor(dictionary=False):
    """Safely get database cursor with error handling"""
    try:
        if dictionary:
            return mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        return mysql.connection.cursor()
    except AttributeError as e:
        current_app.logger.error(f"Database connection error: {e}")
        raise Exception("Database connection not initialized. Please check your configuration.")

def execute_query(query, params=None, fetch_one=False, fetch_all=False, commit=False, dictionary=False):
    """Execute a database query with proper error handling"""
    cursor = None
    try:
        cursor = get_db_cursor(dictionary)
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        if commit:
            mysql.connection.commit()
            result = cursor.lastrowid
        elif fetch_one:
            result = cursor.fetchone()
        elif fetch_all:
            result = cursor.fetchall()
        else:
            result = None
            
        return result
    except Exception as e:
        if commit:
            mysql.connection.rollback()
        current_app.logger.error(f"Database error: {e}")
        raise e
    finally:
        if cursor:
            cursor.close()

def get_product_by_id(product_id):
    """Get product details by ID"""
    query = "SELECT id, name, price, stock FROM products WHERE id = %s"
    result = execute_query(query, (product_id,), fetch_one=True, dictionary=True)
    return result

def get_all_products(active_only=True):
    """Get all products"""
    if active_only:
        query = "SELECT id, name, price, stock FROM products WHERE stock > 0 ORDER BY name"
    else:
        query = "SELECT id, name, price, stock FROM products ORDER BY name"
    return execute_query(query, fetch_all=True, dictionary=True)

def search_products(search_term):
    """Search products by name"""
    query = "SELECT id, name, price, stock FROM products WHERE name LIKE %s ORDER BY name"
    return execute_query(query, (f'%{search_term}%',), fetch_all=True, dictionary=True)

def get_customer_by_id(customer_id):
    """Get customer details by ID"""
    query = "SELECT id, name, phone, email, address FROM customers WHERE id = %s"
    return execute_query(query, (customer_id,), fetch_one=True, dictionary=True)

def get_all_customers():
    """Get all customers"""
    query = "SELECT id, name, phone, email, address FROM customers ORDER BY name"
    return execute_query(query, fetch_all=True, dictionary=True)

def create_bill(customer_id, bill_data, items):
    """Create a new bill with items"""
    try:
        # Start transaction
        cursor = get_db_cursor()
        
        # Insert bill
        bill_query = """
            INSERT INTO bills (customer_id, bill_number, total_amount, gst_amount, final_amount, payment_method)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(bill_query, (
            customer_id,
            bill_data['bill_number'],
            bill_data['subtotal'],
            bill_data['gst_amount'],
            bill_data['final_amount'],
            bill_data['payment_method']
        ))
        bill_id = cursor.lastrowid
        
        # Insert bill items and update stock
        for item in items:
            # Check stock
            cursor.execute("SELECT stock FROM products WHERE id = %s", (item['product_id'],))
            stock_result = cursor.fetchone()
            if not stock_result or stock_result[0] < item['quantity']:
                mysql.connection.rollback()
                raise Exception(f"Insufficient stock for product ID {item['product_id']}")
            
            # Insert bill item
            item_query = """
                INSERT INTO bill_items (bill_id, product_id, quantity, unit_price, total_price)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(item_query, (
                bill_id,
                item['product_id'],
                item['quantity'],
                item['price'],
                item['quantity'] * item['price']
            ))
            
            # Update product stock
            cursor.execute("UPDATE products SET stock = stock - %s WHERE id = %s",
                         (item['quantity'], item['product_id']))
        
        mysql.connection.commit()
        cursor.close()
        return bill_id
        
    except Exception as e:
        mysql.connection.rollback()
        current_app.logger.error(f"Error creating bill: {e}")
        raise e

def get_bill_details(bill_id):
    """Get complete bill details with customer and items"""
    # Get bill with customer details
    bill_query = """
        SELECT b.*, c.name, c.phone, c.email, c.address 
        FROM bills b 
        LEFT JOIN customers c ON b.customer_id = c.id 
        WHERE b.id = %s
    """
    bill = execute_query(bill_query, (bill_id,), fetch_one=True, dictionary=True)
    
    if not bill:
        return None
    
    # Get bill items
    items_query = """
        SELECT bi.*, p.name as product_name 
        FROM bill_items bi 
        JOIN products p ON bi.product_id = p.id 
        WHERE bi.bill_id = %s
    """
    items = execute_query(items_query, (bill_id,), fetch_all=True, dictionary=True)
    
    return {'bill': bill, 'items': items}

def get_recent_bills(limit=10):
    """Get recent bills"""
    query = """
        SELECT b.id, b.bill_number, COALESCE(c.name, 'Walk-in Customer') as customer_name, 
               b.final_amount, b.created_at
        FROM bills b
        LEFT JOIN customers c ON b.customer_id = c.id
        ORDER BY b.created_at DESC
        LIMIT %s
    """
    return execute_query(query, (limit,), fetch_all=True, dictionary=True)

def get_dashboard_stats():
    """Get statistics for dashboard"""
    stats = {}
    
    # Today's sales
    query = "SELECT COALESCE(SUM(final_amount), 0) FROM bills WHERE DATE(created_at) = CURDATE()"
    stats['today_sales'] = execute_query(query, fetch_one=True)[0]
    
    # Monthly sales
    query = "SELECT COALESCE(SUM(final_amount), 0) FROM bills WHERE MONTH(created_at) = MONTH(CURDATE())"
    stats['monthly_sales'] = execute_query(query, fetch_one=True)[0]
    
    # Total products
    query = "SELECT COUNT(*) FROM products"
    stats['total_products'] = execute_query(query, fetch_one=True)[0]
    
    # Total bills
    query = "SELECT COUNT(*) FROM bills"
    stats['total_bills'] = execute_query(query, fetch_one=True)[0]
    
    # Low stock count
    query = "SELECT COUNT(*) FROM products WHERE stock < 5"
    stats['low_stock'] = execute_query(query, fetch_one=True)[0]
    
    return stats