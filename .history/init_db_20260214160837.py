import pymysql
from config import Config

def init_database():
    connection = None
    try:
        # Connect to MySQL server
        connection = pymysql.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            port=Config.MYSQL_PORT
        )
        
        with connection.cursor() as cursor:
            # Create database
            cursor.execute("CREATE DATABASE IF NOT EXISTS shop_billing")
            print("✅ Database 'shop_billing' created")
            
            # Use the database
            cursor.execute("USE shop_billing")
            
            # Create users table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    password_hash VARCHAR(255) NOT NULL
                )
            """)
            print("✅ Users table created")
            
            # Create customers table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS customers (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100),
                    phone VARCHAR(20),
                    email VARCHAR(100),
                    address TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            print("✅ Customers table created")
            
            # Create products table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100),
                    price DECIMAL(10,2),
                    stock INT DEFAULT 0,
                    barcode VARCHAR(100)
                )
            """)
            print("✅ Products table created")
            
            # Create bills table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS bills (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    customer_id INT,
                    bill_number VARCHAR(50),
                    total_amount DECIMAL(10,2),
                    discount_type VARCHAR(50),
                    discount_value DECIMAL(10,2),
                    discount_amount DECIMAL(10,2),
                    gst_type VARCHAR(50),
                    cgst_amount DECIMAL(10,2),
                    sgst_amount DECIMAL(10,2),
                    igst_amount DECIMAL(10,2),
                    gst_amount DECIMAL(10,2),
                    final_amount DECIMAL(10,2),
                    payment_method VARCHAR(50),
                    upi_id VARCHAR(100),
                    card_number VARCHAR(100),
                    card_name VARCHAR(100),
                    status VARCHAR(50) DEFAULT 'Pending',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (customer_id) REFERENCES customers(id)
                )
            """)
            print("✅ Bills table created")
            
            # Create bill_items table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS bill_items (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    bill_id INT,
                    product_id INT,
                    quantity INT,
                    unit_price DECIMAL(10,2),
                    total_price DECIMAL(10,2),
                    FOREIGN KEY (bill_id) REFERENCES bills(id),
                    FOREIGN KEY (product_id) REFERENCES products(id)
                )
            """)
            print("✅ Bill items table created")
            
            # Insert admin user
            cursor.execute("""
                INSERT INTO users (username, password_hash) 
                SELECT 'admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4NQv6Y7I8e'
                WHERE NOT EXISTS (SELECT 1 FROM users WHERE username = 'admin')
            """)
            print("✅ Admin user created (username: admin, password: admin123)")
            
            connection.commit()
            print("\n🎉 Database initialized successfully!")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        if connection:
            connection.close()

if __name__ == "__main__":
    init_database()