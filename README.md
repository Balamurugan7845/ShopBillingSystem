# 🛒 Shop Billing System

<div align="center">

# Shop Billing System

A modern **Flask-based Shop Billing System** designed for retail stores and supermarkets. It provides secure authentication, billing, invoice generation, customer management, inventory management, sales analytics, and an intuitive dashboard.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge\&logo=python\&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.3-000000?style=for-the-badge\&logo=flask)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge\&logo=mysql\&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5-7952B3?style=for-the-badge\&logo=bootstrap\&logoColor=white)
![Chart.js](https://img.shields.io/badge/Chart.js-FF6384?style=for-the-badge\&logo=chartdotjs\&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

</div>

---

## 📑 Table of Contents

- [📌 Overview](#-overview)
- [✨ Features](#-features)
- [🛠️ Tech Stack](#️-tech-stack)
- [📁 Project Structure](#-project-structure)
- [📸 Screenshots](#-screenshots)
- [⚙️ Installation](#️-installation)
- [🔑 Environment Variables](#-environment-variables)
- [🗄️ Database Setup](#️-database-setup)
- [🚀 Run the Application](#-run-the-application)
- [👤 Default Admin Login](#-default-admin-login)
- [👥 User Roles](#-user-roles)
- [📊 Excel Import Format](#-excel-import-format)
- [📋 Requirements](#-requirements)
- [🚀 Future Improvements](#-future-improvements)
- [🤝 Contributing](#-contributing)
- [📜 License](#-license)
- [👨‍💻 Author](#-author)

---

# 📌 Overview

The **Shop Billing System** is a web application developed using **Python**, **Flask**, **MySQL**, and **Bootstrap 5**. It helps shop owners manage products, customers, billing, invoices, inventory, and sales reports efficiently through a modern dashboard.

---

# ✨ Features

## 🔐 Authentication

* Secure Login & Logout
* Flask-Login Authentication
* Password Hashing using Flask-Bcrypt
* Change Password
* Profile Management
* Session Management
* Role-Based Access Control
* Admin & User Accounts

---

## 📊 Dashboard

* Today's Sales
* Monthly Sales
* Yearly Sales
* Total Revenue
* Total Products
* Total Customers
* Total Bills
* Low Stock Products
* Weekly Sales Chart
* Product Stock Chart
* Recent Transactions

---

## 🧾 Billing System

* Create Bills
* Edit Bills
* Delete Bills
* GST Calculation
* Discount Calculation
* Multiple Payment Methods
* Invoice Preview
* Invoice Printing
* PDF Invoice Generation
* Draft Bills

---

## 📦 Product Management

* Add Products
* Edit Products
* Delete Products
* Search Products
* Barcode Support
* Product Categories
* Product Images
* Stock Management
* Low Stock Alerts
* Excel Import
* Excel Export

---

## 👥 Customer Management

* Add Customers
* Update Customers
* Delete Customers
* Customer Search
* Purchase History
* Billing History
* Customer Reports

---

## 📈 Reports & Analytics

* Daily Sales Report
* Weekly Sales Report
* Monthly Sales Report
* Product Sales Report
* Customer Purchase Report
* Dashboard Charts using Chart.js

---

## 🔒 Security

* Password Hashing
* Secure Sessions
* Protected Routes
* Admin Authorization
* SQL Injection Protection
* CSRF Protection
* Input Validation

---

# 🛠️ Tech Stack

| Technology   | Usage                          |
| ------------ | ------------------------------ |
| Python       | Backend Programming Language   |
| Flask        | Web Framework                  |
| MySQL        | Database                       |
| HTML5        | Page Structure                 |
| CSS3         | Styling                        |
| Bootstrap 5  | Frontend Framework             |
| JavaScript   | Client-side Interactivity      |
| Chart.js     | Dashboard Charts               |
| Flask-Login  | Authentication                 |
| Flask-Bcrypt | Password Security              |
| Pandas       | Excel Import & Data Processing |
| OpenPyXL     | Excel File Reader              |
| Jinja2       | HTML Template Engine           |
| Git & GitHub | Version Control                |

---

# 📁 Project Structure

```text
shop-billing-system/
│
├── app/
│   ├── auth/
│   ├── billing/
│   ├── customers/
│   ├── dashboard/
│   ├── invoices/
│   ├── products/
│   ├── reports/
│   ├── utils/
│   ├── __init__.py
│   ├── db.py
│   └── models.py
│
├── database/
│   └── schema.sql
│
├── docs/
│   └── screenshots/
│       ├── login.png
│       ├── dashboard.png
│       ├── billing.png
│       ├── products.png
│       └── customers.png
│
├── static/
│   ├── css/
│   ├── js/
│   ├── images/
│   └── fonts/
│
├── templates/
│   ├── auth/
│   ├── billing/
│   ├── customers/
│   ├── dashboard/
│   ├── invoices/
│   ├── products/
│   ├── settings/
│   └── base.html
│
├── Json/
│   ├── customers_name.json
│   └── products_name.json
│
├── .github/
│   ├── ISSUE_TEMPLATE/
│   ├── workflows/
│   └── PULL_REQUEST_TEMPLATE.md
│
├── .gitignore
├── .env.example
├── CHANGELOG.md
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── LICENSE
├── README.md
├── requirements.txt
├── config.py
├── init_db.py
└── run.py
```

---

# 📸 Screenshots

Store your screenshots inside:

```text
docs/screenshots/
```

Example:

```text
docs/screenshots/login.png
docs/screenshots/dashboard.png
docs/screenshots/billing.png
docs/screenshots/products.png
docs/screenshots/customers.png
```

Then reference them like:

```markdown
![Dashboard](docs/screenshots/dashboard.png)

![Billing](docs/screenshots/billing.png)

![Products](docs/screenshots/products.png)

![Customers](docs/screenshots/customers.png)
```

---

# ⚙️ Installation

## 1️⃣ Clone Repository

```bash
git clone https://github.com/yourusername/shop-billing-system.git
```

## 2️⃣ Open Project

```bash
cd shop-billing-system
```

## 3️⃣ Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

## 4️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file.

```env
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DB=shop_billing_db
SECRET_KEY=your_secret_key
```

---

# 🗄️ Database Setup

Create the database:

```sql
CREATE DATABASE shop_billing_db;
```

Import the schema:

```bash
mysql -u root -p shop_billing_db < database/schema.sql
```

---

# 🚀 Run the Application

```bash
python run.py
```

Visit:

```text
http://127.0.0.1:5000
```

---

# 👤 Default Admin Login

| Username | Password |
| -------- | -------- |
| admin    | admin123 |

> Change the default credentials after the first login.

---

# 👥 User Roles

| Role  | Access                        |
| ----- | ----------------------------- |
| Admin | Full System Access            |
| User  | Billing & Customer Operations |

---

# 📊 Excel Import Format

Required columns:

| name | price | stock |
| ---- | ----: | ----: |
| Rice |    50 |   100 |
| Oil  |   150 |    25 |

---

# 📋 Requirements

* Python 3.10+
* MySQL 8+
* pip
* Git

---

# 🚀 Future Improvements

* Barcode Scanner
* QR Code Billing
* Thermal Printer Support
* WhatsApp Invoice
* Email Invoice
* Inventory Forecasting
* Dark Mode
* Multi-Store Management
* Cloud Deployment
* REST API

---

# 🤝 Contributing

Contributions are welcome.

1. Fork the repository.
2. Create a feature branch.

```bash
git checkout -b feature/new-feature
```

3. Commit your changes.

```bash
git commit -m "Add new feature"
```

4. Push your branch.

```bash
git push origin feature/new-feature
```

5. Open a Pull Request.

---

# 📜 License

This project is licensed under the **MIT License**.

See the **LICENSE** file for more information.

---

# 👨‍💻 Author

**Balamurugan**

* B.Tech Computer Science Engineering Student
* Python Developer
* Flask Developer
* Full Stack Developer

---

# ⭐ Support

If you found this project useful:

* ⭐ Star this repository
* 🍴 Fork this repository
* 🐛 Report bugs
* 💡 Suggest new features

---

<div align="center">

Made with ❤️ using **Python**, **Flask**, **MySQL**, and **Bootstrap 5**

**Happy Coding! 🚀**

</div>
