CREATE DATABASE IF NOT EXISTS shop_billing_db;

USE shop_billing_db;

-- =========================
-- USERS
-- =========================

CREATE TABLE IF NOT EXISTS users (

    id INT PRIMARY KEY AUTO_INCREMENT,

    username VARCHAR(100) UNIQUE NOT NULL,

    password VARCHAR(255) NOT NULL,

    role VARCHAR(20) DEFAULT 'user',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);

-- =========================
-- CUSTOMERS
-- =========================

CREATE TABLE IF NOT EXISTS customers (

    id INT AUTO_INCREMENT PRIMARY KEY,

    name VARCHAR(100),

    phone VARCHAR(20),

    email VARCHAR(100),

    address TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);

-- =========================
-- PRODUCTS
-- =========================

CREATE TABLE IF NOT EXISTS products (

    id INT AUTO_INCREMENT PRIMARY KEY,

    name VARCHAR(100),

    price DECIMAL(10,2),

    stock INT DEFAULT 0,

    barcode VARCHAR(100),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);

-- =========================
-- BILLS
-- =========================

CREATE TABLE IF NOT EXISTS bills (

    id INT AUTO_INCREMENT PRIMARY KEY,

    customer_id INT,

    bill_number VARCHAR(100),

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

    FOREIGN KEY (customer_id)
    REFERENCES customers(id)

);

-- =========================
-- BILL ITEMS
-- =========================

CREATE TABLE IF NOT EXISTS bill_items (

    id INT AUTO_INCREMENT PRIMARY KEY,

    bill_id INT,

    product_id INT,

    quantity INT,

    unit_price DECIMAL(10,2),

    total_price DECIMAL(10,2),

    FOREIGN KEY (bill_id)
    REFERENCES bills(id)
    ON DELETE CASCADE,

    FOREIGN KEY (product_id)
    REFERENCES products(id)

);

-- =========================
-- DEFAULT ADMIN USER
-- username: admin
-- password: admin123
-- =========================

INSERT INTO users (
    username,
    password,
    role
)

SELECT
    'admin',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4NQv6Y7I8e',
    'admin'

WHERE NOT EXISTS (

    SELECT 1
    FROM users
    WHERE username = 'admin'

);

-- =========================
-- SHOW TABLES
-- =========================

SHOW TABLES;