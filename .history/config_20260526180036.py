import os

class Config:
    # Secret key for sessions
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    
    # MySQL Configuration
    MYSQL_HOST = os.environ.get('MYSQL_HOST') or 'localhost'
    MYSQL_USER = os.environ.get('MYSQL_USER') or 'root'
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD') or 'MYSQL_PASSWORD'
    MYSQL_DB = os.environ.get('MYSQL_DB') or 'shop_billing_db'
    MYSQL_PORT = int(os.environ.get('MYSQL_PORT') or 3306)
    
    # Session configuration
    SESSION_PERMANENT = False
    SESSION_TYPE = 'filesystem'
    SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Application settings
    APP_NAME = "Shop Billing System"
    ITEMS_PER_PAGE = 20
    
    # GST settings
    GST_RATE = 18  # Default GST rate percentage
    
    # Company details for invoices
    COMPANY_NAME = "Shop Billing System"
    COMPANY_ADDRESS = "123 College Street, Academic City, AC 12345"
    COMPANY_PHONE = "(555) 123-4567"
    COMPANY_EMAIL = "shop@college.edu"
    
    # Debug settings
    DEBUG = os.environ.get('FLASK_DEBUG') or True
    TESTING = False
        DEBUG = os.environ.get(

        'FLASK_DEBUG',
        'True'

    ).lower() == 'true'