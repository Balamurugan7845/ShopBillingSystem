CREATE DATABASE IF NOT EXISTS shop_billing_db;

USE shop_billing_db;

-- =========================================
-- USERS TABLE
-- =========================================

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

);

-- =========================================
-- CUSTOMERS TABLE
-- =========================================

CREATE TABLE IF NOT EXISTS customers (

    id INT AUTO_INCREMENT PRIMARY KEY,

    name VARCHAR(100)
    NOT NULL,

    phone VARCHAR(20),

    email VARCHAR(100),

    address TEXT,

    created_at TIMESTAMP
    DEFAULT CURRENT_TIMESTAMP

);

-- =========================================
-- PRODUCTS TABLE
-- =========================================

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

);

-- =========================================
-- BILLS TABLE
-- =========================================

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

    CONSTRAINT fk_bill_customer
    FOREIGN KEY (customer_id)
    REFERENCES customers(id)
    ON DELETE SET NULL

);

-- =========================================
-- BILL ITEMS TABLE
-- =========================================

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

    CONSTRAINT fk_bill_items_bill
    FOREIGN KEY (bill_id)
    REFERENCES bills(id)
    ON DELETE CASCADE,

    CONSTRAINT fk_bill_items_product
    FOREIGN KEY (product_id)
    REFERENCES products(id)
    ON DELETE CASCADE

);

-- =========================================
-- DEFAULT ADMIN USER
-- username: admin
-- password: admin123
-- =========================================

INSERT INTO users (

    username,
    password,
    role

)

SELECT

    'admin',

    'pbkdf2:sha256:600000$kT6X8YjL$8b2d1f9b62f97d5d8c14f2cb7b35d82b71d31c7b85f3d8b6b4d80f7a43b5b6f5',

    'admin'

WHERE NOT EXISTS (

    SELECT 1
    FROM users
    WHERE username = 'admin'

);

-- =========================================
-- SAMPLE PRODUCTS
-- =========================================

INSERT INTO products (

    name,
    price,
    stock,
    barcode

)

VALUES

('Rice Bag 25KG', 1200.00, 15, '100001'),

('Sugar 1KG', 48.00, 120, '100002'),

('Milk Packet', 28.00, 80, '100003'),

('Cooking Oil 1L', 145.00, 40, '100004'),

('Soap', 35.00, 200, '100005');

-- =========================================
-- SHOW TABLES
-- =========================================

SHOW TABLES;

-- =========================================
-- CHECK USERS
-- =========================================

SELECT
    id,
    username,
    role
FROM users;