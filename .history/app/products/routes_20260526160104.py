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

@products_bp.route('/import-excel', methods=['POST'])
@login_required
def import_products_excel():

    try:

        if 'excel_file' not in request.files:
            flash('No file selected', 'danger')
            return redirect(url_for('products.products'))

        file = request.files['excel_file']

        if file.filename == '':
            flash('No file selected', 'danger')
            return redirect(url_for('products.products'))

        # Read Excel
        df = pd.read_excel(file)

        # Required columns
        required_columns = ['name', 'price', 'stock']

        for col in required_columns:

            if col not in df.columns:

                flash(f'Missing column: {col}', 'danger')
                return redirect(url_for('products.products'))

        connection = get_db()

        with connection.cursor() as cur:

            imported_count = 0

            for _, row in df.iterrows():

                name = str(row['name']).strip()
                price = float(row['price'])
                stock = int(row['stock'])

                # Skip empty product names
                if not name:
                    continue

                cur.execute("""
                    INSERT INTO products (
                        name,
                        price,
                        stock
                    )
                    VALUES (%s,%s,%s)
                """, (
                    name,
                    price,
                    stock
                ))

                imported_count += 1

            connection.commit()

        flash(
            f'{imported_count} products imported successfully!',
            'success'
        )

    except Exception as e:

        print("IMPORT ERROR:", str(e))

        flash(
            f'Import failed: {str(e)}',
            'danger'
        )

    finally:

        try:
            connection.close()
        except:
            pass

    return redirect(url_for('products.products'))