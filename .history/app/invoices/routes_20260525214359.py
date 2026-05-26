from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file
from flask_login import login_required
from app.db import get_db
import pymysql
from app.utils.pdf_generator import generate_invoice_pdf
import datetime
import decimal

invoices_bp = Blueprint('invoices', __name__)

@invoices_bp.route('/')
@login_required
def invoices():
    connection = get_db()
    if not connection:
        flash('Database connection error', 'danger')
        return render_template('invoices/invoices.html', invoices=[])
    
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cur:
            cur.execute("""
                SELECT b.id, b.bill_number, COALESCE(c.name, 'Walk-in Customer') as customer_name, 
                       b.total_amount, b.gst_amount, b.final_amount, 
                       b.payment_method, b.created_at
                FROM bills b 
                LEFT JOIN customers c ON b.customer_id = c.id 
                ORDER BY b.created_at DESC
            """)
            invoices = cur.fetchall()
    except Exception as e:
        flash(f'Database error: {str(e)}', 'danger')
        invoices = []
    finally:
        connection.close()
    
    return render_template('invoices/invoices.html', invoices=invoices)

@invoices_bp.route('/<int:bill_id>')
@login_required
def invoice_detail(bill_id):
    connection = get_db()
    if not connection:
        flash('Database connection error', 'danger')
        return redirect(url_for('invoices.invoices'))
    
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cur:
            cur.execute("""
                SELECT b.*, c.name, c.phone, c.email, c.address 
                FROM bills b 
                LEFT JOIN customers c ON b.customer_id = c.id 
                WHERE b.id = %s
            """, (bill_id,))
            bill = cur.fetchone()
            
            cur.execute("""
                SELECT bi.*, p.name 
                FROM bill_items bi 
                JOIN products p ON bi.product_id = p.id 
                WHERE bi.bill_id = %s
            """, (bill_id,))
            items = cur.fetchall()
    except Exception as e:
        flash(f'Database error: {str(e)}', 'danger')
        return redirect(url_for('invoices.invoices'))
    finally:
        connection.close()
    
    return render_template('invoices/invoice_detail.html', bill=bill, items=items)

@invoices_bp.route('/<int:bill_id>/pdf', methods=['GET', 'POST'])
@login_required
def generate_pdf(bill_id):
    connection = get_db()
    if not connection:
        flash('Database connection error', 'danger')
        return redirect(url_for('invoices.invoices'))
    
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cur:
            cur.execute("""
                SELECT b.*, c.name, c.phone, c.email, c.address 
                FROM bills b 
                LEFT JOIN customers c ON b.customer_id = c.id 
                WHERE b.id = %s
            """, (bill_id,))
            bill = cur.fetchone()
            
            cur.execute("""
                SELECT bi.*, p.name 
                FROM bill_items bi 
                JOIN products p ON bi.product_id = p.id 
                WHERE bi.bill_id = %s
            """, (bill_id,))
            items = cur.fetchall()
    except Exception as e:
        flash(f'Database error: {str(e)}', 'danger')
        return redirect(url_for('invoices.invoices'))
    finally:
        connection.close()
    
    if not bill:
        flash('Bill not found', 'danger')
        return redirect(url_for('invoices.invoices'))
    
    # Convert Decimal to float for PDF generator
    for key, value in bill.items():
        if isinstance(value, decimal.Decimal):
            bill[key] = float(value)
    
    for item in items:
        for key, value in item.items():
            if isinstance(value, decimal.Decimal):
                item[key] = float(value)
    
    # Generate PDF
    pdf_buffer = generate_invoice_pdf(bill, items)
    
    return send_file(
        pdf_buffer,
        download_name=f"invoice_{bill['bill_number']}.pdf",
        as_attachment=True,
        mimetype='application/pdf'
    )

@invoices_bp.route('/<int:bill_id>/print')
@login_required
def print_invoice(bill_id):
    connection = get_db()
    if not connection:
        flash('Database connection error', 'danger')
        return redirect(url_for('invoices.invoices'))
    
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cur:
            cur.execute("""
                SELECT b.*, c.name, c.phone, c.email, c.address 
                FROM bills b 
                LEFT JOIN customers c ON b.customer_id = c.id 
                WHERE b.id = %s
            """, (bill_id,))
            bill = cur.fetchone()
            
            cur.execute("""
                SELECT bi.*, p.name 
                FROM bill_items bi 
                JOIN products p ON bi.product_id = p.id 
                WHERE bi.bill_id = %s
            """, (bill_id,))
            items = cur.fetchall()
    except Exception as e:
        flash(f'Database error: {str(e)}', 'danger')
        return redirect(url_for('invoices.invoices'))
    finally:
        connection.close()
    
    if not bill:
        flash('Bill not found', 'danger')
        return redirect(url_for('invoices.invoices'))

    # Convert Decimal to float for template
    for key, value in bill.items():
        if isinstance(value, decimal.Decimal):
            bill[key] = float(value)
    
    processed_items = []
    for item in items:
        item_dict = dict(item)
        for key, value in item_dict.items():
            if isinstance(value, decimal.Decimal):
                item_dict[key] = float(value)
        processed_items.append(item_dict)

    return render_template('invoices/invoice_print.html', bill=bill, items=processed_items)