from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required
from app.db import get_db
import pymysql

customers_bp = Blueprint('customers', __name__)

@customers_bp.route('/')
@login_required
def customers():
    search = request.args.get('search', '')
    connection = get_db()
    
    if not connection:
        flash('Database connection error', 'danger')
        return render_template('customers/customers.html', customers=[], search=search)
    
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cur:
            if search:
                cur.execute(
                    "SELECT id, name, phone, email, address, created_at "
                    "FROM customers WHERE name LIKE %s OR phone LIKE %s ORDER BY name",
                    (f'%{search}%', f'%{search}%')
                )
            else:
                cur.execute("SELECT id, name, phone, email, address, created_at FROM customers ORDER BY name")

            rows = cur.fetchall()

            customers = []
            for c in rows:
                customers.append({
                    "id": c['id'],
                    "name": c['name'],
                    "phone": c['phone'],
                    "email": c['email'],
                    "address": c['address'],
                    "created_at": c['created_at'].strftime("%Y-%m-%d") if c['created_at'] else ""
                })
    except Exception as e:
        flash(f'Database error: {str(e)}', 'danger')
        customers = []
    finally:
        connection.close()

    return render_template('customers/customers.html', customers=customers, search=search)

@customers_bp.route('/add', methods=['POST'])
@login_required
def add_customer():
    name = request.form['name']
    phone = request.form.get('phone', '')
    email = request.form.get('email', '')
    address = request.form.get('address', '')
    
    connection = get_db()
    if not connection:
        flash('Database connection error', 'danger')
        return redirect(url_for('customers.customers'))
    
    try:
        with connection.cursor() as cur:
            cur.execute("INSERT INTO customers (name, phone, email, address) VALUES (%s, %s, %s, %s)", 
                       (name, phone, email, address))
            connection.commit()
        flash('Customer added successfully!', 'success')
    except Exception as e:
        flash(f'Database error: {str(e)}', 'danger')
    finally:
        connection.close()
    
    return redirect(url_for('customers.customers'))

@customers_bp.route('/edit/<int:customer_id>', methods=['POST'])
@login_required
def edit_customer(customer_id):
    name = request.form['name']
    phone = request.form.get('phone', '')
    email = request.form.get('email', '')
    address = request.form.get('address', '')
    
    connection = get_db()
    if not connection:
        flash('Database connection error', 'danger')
        return redirect(url_for('customers.customers'))
    
    try:
        with connection.cursor() as cur:
            cur.execute("UPDATE customers SET name = %s, phone = %s, email = %s, address = %s WHERE id = %s", 
                       (name, phone, email, address, customer_id))
            connection.commit()
        flash('Customer updated successfully!', 'success')
    except Exception as e:
        flash(f'Database error: {str(e)}', 'danger')
    finally:
        connection.close()
    
    return redirect(url_for('customers.customers'))

@customers_bp.route('/delete/<int:customer_id>')
@login_required
def delete_customer(customer_id):
    connection = get_db()
    if not connection:
        flash('Database connection error', 'danger')
        return redirect(url_for('customers.customers'))
    
    try:
        with connection.cursor() as cur:
            cur.execute("DELETE FROM customers WHERE id = %s", (customer_id,))
            connection.commit()
        flash('Customer deleted successfully!', 'success')
    except Exception as e:
        flash(f'Database error: {str(e)}', 'danger')
    finally:
        connection.close()
    
    return redirect(url_for('customers.customers'))