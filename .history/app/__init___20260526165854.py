from flask import Flask, redirect, url_for
from flask_mysqldb import MySQL
from flask_login import LoginManager
from config import Config
import pymysql


# Install pymysql as MySQLdb
pymysql.install_as_MySQLdb()

# Initialize extensions
mysql = MySQL()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__, template_folder='../client/templates', static_folder='../client/static'  )

    app.config.from_object(Config)
    
    # Initialize extensions with app
    mysql.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    # Test database connection
    from app.db import get_db
    try:
        conn = get_db()
        if conn:
            conn.close()
            print("✅ Database connected successfully!")
        else:
            print("❌ Database connection failed!")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
    
    # Import and register blueprints
    from app.auth.routes import auth_bp
    from app.dashboard.routes import dashboard_bp
    from app.products.routes import products_bp
    from app.customers.routes import customers_bp
    from app.billing.routes import billing_bp
    from app.invoices.routes import invoices_bp
    from app.api.routes import api_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(products_bp, url_prefix='/products')
    app.register_blueprint(customers_bp, url_prefix='/customers')
    app.register_blueprint(billing_bp, url_prefix='/billing')
    app.register_blueprint(invoices_bp, url_prefix='/invoices')
    app.register_blueprint(api_bp, url_prefix='/api')
    
    @app.route('/')
    def index():
        from flask_login import current_user
        if current_user.is_authenticated:
            return redirect(url_for('dashboard.dashboard'))
        return redirect(url_for('auth.login'))
    
# =========================
# 403 ERROR HANDLER
# =========================

@app.errorhandler(403)
def forbidden(e):

    return render_template(
        'errors/403.html'
    ), 403


return app
