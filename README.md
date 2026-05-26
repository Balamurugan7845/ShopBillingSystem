# 🛒 Shop Billing System

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-2.3-black?style=for-the-badge&logo=flask)
![MySQL](https://img.shields.io/badge/MySQL-Database-orange?style=for-the-badge&logo=mysql)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5-purple?style=for-the-badge&logo=bootstrap)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

A modern Flask-based Shop Billing System with authentication, billing, invoice generation, dashboard analytics, product management, and customer management.

</div>

---

# ✨ Features

## 🔐 Authentication

- Login / Logout
- Secure Password Hashing (Bcrypt)
- Role-Based Access Control
- Admin & User Roles
- Profile Settings
- Change Password

---

## 📊 Dashboard

- Today's Sales
- Monthly Sales
- Total Products
- Total Bills
- Weekly Sales Chart
- Product Stock Chart
- Recent Bills

---

## 🧾 Billing System

- Create Bills
- GST Calculation
- Discount System
- Multiple Payment Methods
- Invoice Print
- PDF Invoice
- Draft Bills

---

## 📦 Product Management

- Add/Edit/Delete Products
- Product Search
- Barcode Support
- Excel Import
- Price Sorting
- Stock Sorting
- Low Stock Alert

---

## 👥 Customer Management

- Add/Edit/Delete Customers
- Customer Search
- Billing History

---

# 🛠️ Tech Stack

| Technology | Usage |
|---|---|
| Python | Backend |
| Flask | Web Framework |
| MySQL | Database |
| Bootstrap 5 | Frontend |
| Chart.js | Dashboard Charts |
| Flask-Login | Authentication |
| Flask-Bcrypt | Password Hashing |
| Pandas | Excel Import |
| OpenPyXL | Excel Reader |

---

# 📁 Project Structure

```text
shop-billing-system/

├── Json/
│   ├── customers_name.json
│   └── products_name.json

├── app/
│   ├── api/
│   ├── auth/
│   ├── billing/
│   ├── customers/
│   ├── dashboard/
│   ├── invoices/
│   ├── products/
│   ├── utils/
│   ├── __init__.py
│   ├── db.py
│   └── models.py

├── database/
│   └── schema.sql

├── static/
│   ├── css/
│   ├── fonts/
│   ├── images/
│   └── js/

├── templates/
│   ├── auth/
│   ├── billing/
│   ├── customers/
│   ├── dashboard/
│   ├── invoices/
│   ├── products/
│   ├── settings/
│   └── base.html

├── config.py
├── requirements.txt
├── run.py
└── README.md
````


# ⚙️ Installation

## 📥 Clone Repository

```bash
git clone https://github.com/yourusername/shop-billing-system.git
```

---

## 📂 Open Project

```bash
cd shop-billing-system
```

---

## 🧪 Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

---

# 📦 Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🗄️ Configure Database

Create MySQL database:

```sql
CREATE DATABASE shop_billing_db;
```

---

# ⚡ Update Config

Inside:

```python
config.py
```

Set your MySQL credentials:

```python
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'your-password'
MYSQL_DB = 'shop_billing_db'
```

---

# 🚀 Initialize Database

```bash
python init_db.py
```

---

# ▶️ Run Application

```bash
python run.py
```

Open browser:

```text
http://127.0.0.1:5000
```

---

# 🔑 Default Admin Login

| Username | Password |
| -------- | -------- |
| admin    | admin123 |

---

# 👨‍💼 User Roles

| Role  | Access       |
| ----- | ------------ |
| admin | Full Access  |
| user  | Billing Only |

---

# 📄 Excel Import Format

Required columns:

| name | price | stock |
| ---- | ----- | ----- |

Example:

| Rice | 50 | 100 |
| Oil | 150 | 25 |

---

# 🔒 Security Features

* Bcrypt Password Hashing
* Secure Sessions
* Protected Routes
* Admin Access Control

---

# 🌟 Future Improvements

* Barcode Scanner
* Thermal Printer
* WhatsApp Invoice
* Sales Reports
* Dark Mode
* Multi-Store Support

---

# 📜 MIT License

MIT License

Copyright (c) 2026

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software.

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.

---

# 👨‍💻 Author

Developed using Flask + MySQL + Bootstrap 5 ❤️

---

<div align="center">

⭐ Star this repository if you like this project!

</div>
```
