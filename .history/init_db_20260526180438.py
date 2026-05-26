import pymysql

from config import Config

from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

# =========================================
# INIT DATABASE
# =========================================

def init_database():

    connection = None

    try:

        # =====================================
        # CONNECT MYSQL
        # =====================================

        connection = pymysql.connect(

            host=Config.MYSQL_HOST,

            user=Config.MYSQL_USER,

            password=Config.MYSQL_PASSWORD,

            port=Config.MYSQL_PORT

        )

        with connection.cursor() as cursor:

            # =====================================
            # CREATE DATABASE
            # =====================================

            cursor.execute(

                """
                CREATE DATABASE IF NOT EXISTS
                shop_billing_db
                """
            )

            print(
                "✅ Database created"
            )

            # =====================================
            # USE DATABASE
            # =====================================

            cursor.execute(

                """
                USE shop_billing_db
                """
            )

            # =====================================
            # USERS TABLE
            # =====================================

            cursor.execute(

                """
                CREATE TABLE IF NOT EXISTS users (

                    id INT PRIMARY KEY AUTO_INCREMENT,

                    username VARCHAR(100)
                    UNIQUE NOT NULL,

                    password VARCHAR(255)
                    NOT NULL,

                    role VARCHAR(20)
                    DEFAULT 'user',

                    phone VARCHAR(20),

                    created_at TIMESTAMP
                    DEFAULT CURRENT_TIMESTAMP

                )
                """
            )

            print(
                "✅ Users table created"
            )

            # =====================================
            # CUSTOMERS TABLE
            # =====================================

            cursor.execute(

                """
                CREATE TABLE IF NOT EXISTS customers (

                    id INT AUTO_INCREMENT PRIMARY KEY,

                    name VARCHAR(100)
                    NOT NULL,

                    phone VARCHAR(20),

                    email VARCHAR(100),

                    address TEXT,

                    created_at TIMESTAMP
                    DEFAULT CURRENT_TIMESTAMP

                )
                """
            )

            print(
                "✅ Customers table created"
            )

            # =====================================
            # PRODUCTS TABLE
            # =====================================

            cursor.execute(

                """
                CREATE TABLE IF NOT EXISTS products (

                    id INT AUTO_INCREMENT PRIMARY KEY,

                    name VARCHAR(150)
                    NOT NULL,

                    price DECIMAL(10,2)
                    NOT NULL DEFAULT 0.00,

                    stock INT
                    DEFAULT 0,

                    barcode VARCHAR(100),

                    created_at TIMESTAMP
                    DEFAULT CURRENT_TIMESTAMP

                )
                """
            )

            print(
                "✅ Products table created"
            )

            # =====================================
            # BILLS TABLE
            # =====================================

            cursor.execute(

                """
                CREATE TABLE IF NOT EXISTS bills (

                    id INT AUTO_INCREMENT PRIMARY KEY,

                    customer_id INT,

                    bill_number VARCHAR(100)
                    UNIQUE,

                    total_amount DECIMAL(10,2)
                    DEFAULT 0.00,

                    discount_type VARCHAR(50),

                    discount_value DECIMAL(10,2)
                    DEFAULT 0.00,

                    discount_amount DECIMAL(10,2)
                    DEFAULT 0.00,

                    gst_type VARCHAR(50),

                    cgst_amount DECIMAL(10,2)
                    DEFAULT 0.00,

                    sgst_amount DECIMAL(10,2)
                    DEFAULT 0.00,

                    igst_amount DECIMAL(10,2)
                    DEFAULT 0.00,

                    gst_amount DECIMAL(10,2)
                    DEFAULT 0.00,

                    final_amount DECIMAL(10,2)
                    DEFAULT 0.00,

                    payment_method VARCHAR(50),

                    upi_id VARCHAR(100),

                    card_number VARCHAR(100),

                    card_name VARCHAR(100),

                    status VARCHAR(50)
                    DEFAULT 'Pending',

                    created_at TIMESTAMP
                    DEFAULT CURRENT_TIMESTAMP,

                    FOREIGN KEY (customer_id)
                    REFERENCES customers(id)
                    ON DELETE SET NULL

                )
                """
            )

            print(
                "✅ Bills table created"
            )

            # =====================================
            # BILL ITEMS TABLE
            # =====================================

            cursor.execute(

                """
                CREATE TABLE IF NOT EXISTS bill_items (

                    id INT AUTO_INCREMENT PRIMARY KEY,

                    bill_id INT
                    NOT NULL,

                    product_id INT
                    NOT NULL,

                    quantity INT
                    DEFAULT 1,

                    unit_price DECIMAL(10,2)
                    DEFAULT 0.00,

                    total_price DECIMAL(10,2)
                    DEFAULT 0.00,

                    FOREIGN KEY (bill_id)
                    REFERENCES bills(id)
                    ON DELETE CASCADE,

                    FOREIGN KEY (product_id)
                    REFERENCES products(id)
                    ON DELETE CASCADE

                )
                """
            )

            print(
                "✅ Bill items table created"
            )

            # =====================================
            # CREATE ADMIN USER
            # =====================================

            admin_password = bcrypt.generate_password_hash(

                "admin123"

            ).decode("utf-8")

            cursor.execute(

                """
                SELECT id
                FROM users
                WHERE username = 'admin'
                """
            )

            existing_admin = cursor.fetchone()

            if not existing_admin:

                cursor.execute(

                    """
                    INSERT INTO users (

                        username,
                        password,
                        role

                    )

                    VALUES (%s, %s, %s)
                    """,

                    (
                        "admin",
                        admin_password,
                        "admin"
                    )

                )

                print(
                    "✅ Admin user created"
                )

            # =====================================
            # COMMIT
            # =====================================

            connection.commit()

            print(
                "\n🎉 Database initialized successfully!"
            )

            print(
                "\nAdmin Login:"
            )

            print(
                "Username: admin"
            )

            print(
                "Password: admin123"
            )

    except Exception as e:

        print(
            f"❌ Error: {e}"
        )

    finally:

        if connection:

            connection.close()

# =========================================
# RUN
# =========================================

if __name__ == "__main__":

    init_database()