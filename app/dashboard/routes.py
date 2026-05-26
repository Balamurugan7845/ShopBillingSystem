from flask import Blueprint, render_template
from flask_login import login_required
from app.db import get_db
import datetime
import pymysql
from app.utils.admin_required import admin_required

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
@dashboard_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    connection = get_db()
    if not connection:
        # Return empty data on connection error
        return render_template('dashboard/dashboard.html',
                             today_sales=0,
                             monthly_sales=0,
                             total_products=0,
                             total_bills=0,
                             recent_bills=[],
                             labels=[],
                             sales=[],
                             stock_labels=[],
                             stock_values=[])
    
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cur:
            # Weekly Sales
            cur.execute("""
                SELECT DATE(created_at) AS day, COALESCE(SUM(final_amount), 0) AS total
                FROM bills
                WHERE created_at >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
                GROUP BY DATE(created_at)
                ORDER BY day ASC
            """)
            weekly_sales = cur.fetchall()

            today = datetime.date.today()
            labels = []
            sales = []
            for i in range(6, -1, -1):
                day = today - datetime.timedelta(days=i)
                labels.append(day.strftime("%a"))
                amount = 0.0
                for r in weekly_sales:
                    if r['day'] and str(r['day']) == str(day):
                        amount = float(r['total'])
                        break
                sales.append(amount)

            # Stock Availability
            cur.execute("""
                SELECT name, stock FROM products WHERE stock > 0 ORDER BY stock DESC LIMIT 10
            """)
            stock_data = cur.fetchall()
            stock_labels = [row['name'] for row in stock_data]
            stock_values = [row['stock'] for row in stock_data]

            # Dashboard Cards
            cur.execute("SELECT COALESCE(SUM(final_amount), 0) AS total FROM bills WHERE DATE(created_at) = CURDATE()")
            result = cur.fetchone()
            today_sales = float(result['total']) if result else 0

            month_start = today.replace(day=1)
            cur.execute("SELECT COALESCE(SUM(final_amount), 0) AS total FROM bills WHERE DATE(created_at) >= %s", 
                       (month_start,))
            result = cur.fetchone()
            monthly_sales = float(result['total']) if result else 0

            cur.execute("SELECT COUNT(*) AS total FROM products")
            result = cur.fetchone()
            total_products = result['total'] if result else 0

            cur.execute("SELECT COUNT(*) AS total FROM bills")
            result = cur.fetchone()
            total_bills = result['total'] if result else 0

            # Recent bills - fetch as tuples for template compatibility
            cur.execute("""
                SELECT b.id, b.bill_number, COALESCE(c.name, 'Walk-in Customer') as customer_name, 
                       b.final_amount, b.created_at
                FROM bills b
                LEFT JOIN customers c ON b.customer_id = c.id
                ORDER BY b.created_at DESC
                LIMIT 5
            """)
            recent_rows = cur.fetchall()
            
            # Convert to list of tuples for template
            recent_bills = []
            for row in recent_rows:
                recent_bills.append((
                    row['id'],
                    row['bill_number'],
                    row['customer_name'],
                    float(row['final_amount']),
                    row['created_at']
                ))

    except Exception as e:
        print(f"Dashboard error: {e}")
        return render_template('dashboard/dashboard.html',
                             today_sales=0,
                             monthly_sales=0,
                             total_products=0,
                             total_bills=0,
                             recent_bills=[],
                             labels=[],
                             sales=[],
                             stock_labels=[],
                             stock_values=[])
    finally:
        connection.close()

    return render_template('dashboard/dashboard.html',
                         today_sales=today_sales,
                         monthly_sales=monthly_sales,
                         total_products=total_products,
                         total_bills=total_bills,
                         recent_bills=recent_bills,
                         labels=labels,
                         sales=sales,
                         stock_labels=stock_labels,
                         stock_values=stock_values)