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

    connection = None

    try:

        # =========================
        # FILE VALIDATION
        # =========================
        if 'excel_file' not in request.files:

            flash(
                'No Excel file selected',
                'danger'
            )

            return redirect(
                url_for('products.products')
            )

        file = request.files['excel_file']

        if file.filename == '':

            flash(
                'Please choose an Excel file',
                'danger'
            )

            return redirect(
                url_for('products.products')
            )

        # =========================
        # FILE EXTENSION CHECK
        # =========================
        allowed_extensions = ('.xlsx', '.xls')

        if not file.filename.lower().endswith(allowed_extensions):

            flash(
                'Only Excel files (.xlsx, .xls) are allowed',
                'danger'
            )

            return redirect(
                url_for('products.products')
            )

        # =========================
        # READ EXCEL
        # =========================
        df = pd.read_excel(file)

        if df.empty:

            flash(
                'Excel file is empty',
                'danger'
            )

            return redirect(
                url_for('products.products')
            )

        # =========================
        # REQUIRED COLUMNS
        # =========================
        required_columns = [
            'name',
            'price',
            'stock'
        ]

        # lowercase columns
        df.columns = df.columns.str.lower().str.strip()

        for column in required_columns:

            if column not in df.columns:

                flash(
                    f'Missing required column: {column}',
                    'danger'
                )

                return redirect(
                    url_for('products.products')
                )

        # =========================
        # DATABASE
        # =========================
        connection = get_db()

        if not connection:

            flash(
                'Database connection failed',
                'danger'
            )

            return redirect(
                url_for('products.products')
            )

        imported_count = 0
        skipped_count = 0

        with connection.cursor(
            pymysql.cursors.DictCursor
        ) as cur:

            for _, row in df.iterrows():

                try:

                    # =========================
                    # CLEAN DATA
                    # =========================
                    name = str(
                        row['name']
                    ).strip()

                    if not name or name.lower() == 'nan':

                        skipped_count += 1
                        continue

                    price = float(
                        row['price']
                    )

                    stock = int(
                        row['stock']
                    )

                    # =========================
                    # DUPLICATE CHECK
                    # =========================
                    cur.execute("""
                        SELECT id
                        FROM products
                        WHERE name = %s
                    """, (name,))

                    existing = cur.fetchone()

                    if existing:

                        skipped_count += 1
                        continue

                    # =========================
                    # INSERT PRODUCT
                    # =========================
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

                except Exception as row_error:

                    print(
                        "ROW IMPORT ERROR:",
                        str(row_error)
                    )

                    skipped_count += 1
                    continue

            # =========================
            # COMMIT
            # =========================
            connection.commit()

        flash(
            f'{imported_count} products imported successfully! '
            f'{skipped_count} skipped.',
            'success'
        )

    except Exception as e:

        print(
            "IMPORT ERROR:",
            str(e)
        )

        import traceback
        traceback.print_exc()

        flash(
            f'Import failed: {str(e)}',
            'danger'
        )

    finally:

        if connection:

            try:
                connection.close()
            except:
                pass

    return redirect(
        url_for('products.products')
    )