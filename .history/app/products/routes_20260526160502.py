from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required
from app.db import get_db
import pymysql
import pandas as pd
from werkzeug.utils import secure_filename
import os

products_bp = Blueprint('products', __name__)

@products_bp.route('/')
@login_required
def products():
    search = request.args.get('search', '')
    connection = get_db()
    
    if not connection:
        flash('Database connection error', 'danger')
        return render_template('products/products.html', products=[], search=search)
    
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cur:
            if search:
                cur.execute("SELECT * FROM products WHERE name LIKE %s ORDER BY name", (f'%{search}%',))
            else:
                cur.execute("SELECT * FROM products ORDER BY name")
            
            products = cur.fetchall()
    except Exception as e:
        flash(f'Database error: {str(e)}', 'danger')
        products = []
    finally:
        connection.close()
    
    return render_template('products/products.html', products=products, search=search)

@products_bp.route('/add', methods=['POST'])
@login_required
def add_product():
    name = request.form['name']
    price = float(request.form['price'])
    stock = int(request.form['stock'])
    
    connection = get_db()
    if not connection:
        flash('Database connection error', 'danger')
        return redirect(url_for('products.products'))
    
    try:
        with connection.cursor() as cur:
            cur.execute("INSERT INTO products (name, price, stock) VALUES (%s, %s, %s)", 
                       (name, price, stock))
            connection.commit()
        flash('Product added successfully!', 'success')
    except Exception as e:
        flash(f'Database error: {str(e)}', 'danger')
    finally:
        connection.close()
    
    return redirect(url_for('products.products'))

@products_bp.route('/edit/<int:product_id>', methods=['POST'])
@login_required
def edit_product(product_id):
    name = request.form['name']
    price = float(request.form['price'])
    stock = int(request.form['stock'])
    
    connection = get_db()
    if not connection:
        flash('Database connection error', 'danger')
        return redirect(url_for('products.products'))
    
    try:
        with connection.cursor() as cur:
            cur.execute("UPDATE products SET name = %s, price = %s, stock = %s WHERE id = %s", 
                       (name, price, stock, product_id))
            connection.commit()
        flash('Product updated successfully!', 'success')
    except Exception as e:
        flash(f'Database error: {str(e)}', 'danger')
    finally:
        connection.close()
    
    return redirect(url_for('products.products'))

@products_bp.route('/delete/<int:product_id>')
@login_required
def delete_product(product_id):
    connection = get_db()
    if not connection:
        flash('Database connection error', 'danger')
        return redirect(url_for('products.products'))
    
    try:
        with connection.cursor() as cur:
            cur.execute("DELETE FROM products WHERE id = %s", (product_id,))
            connection.commit()
        flash('Product deleted successfully!', 'success')
    except Exception as e:
        flash(f'Database error: {str(e)}', 'danger')
    finally:
        connection.close()
    
    return redirect(url_for('products.products'))

