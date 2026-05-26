CREATE DATABASE IF NOT EXISTS shop_billing_db;

USE shop_billing_db;

-- =========================
-- USERS
-- =========================

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

-- =========================
-- CUSTOMERS
-- =========================

CREATE TABLE IF NOT EXISTS customers (

    id INT AUTO_INCREMENT PRIMARY KEY,

    name VARCHAR