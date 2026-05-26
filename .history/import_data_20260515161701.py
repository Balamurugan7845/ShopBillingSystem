#!/usr/bin/env python3
"""
Script to import JSON data into the database
Run this after setting up the database: python import_data.py
"""

import json
import os
import MySQLdb
from config import Config

def import_products(cursor):
    """Import products from JSON file"""
    try:
        json_path = os.path.join(os.path.dirname(__file__), "Json/products_name.json")
        with open(json_path, "r", encoding="utf-8") as f:
            products = json.load(f)
        
        count = 0
        for p in products:
            try:
                cursor.execute("""
                    INSERT INTO products (name, price, stock)
                    VALUES (%s, %s, %s)
                """, (p["name"], p["price"], p["stock"]))
                count += 1
            except Exception as e:
                print(f"Error inserting product {p['name']}: {e}")
        
        print(f"Imported {count} products successfully!")
        return True
        
    except FileNotFoundError:
        print("Error: products_name.json not found in Json/ directory")
        return False
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in products_name.json")
        return False

def import_customers(cursor):
    """Import customers from JSON file"""
    try:
        json_path = os.path.join(os.path.dirname(__file__), "Json/customers_name.json")
        with open(json_path, "r", encoding="utf-8") as f:
            customers = json.load(f)
        
        # Create unique constraint if not exists
        try:
            cursor.execute("ALTER TABLE customers ADD UNIQUE(name, phone);")
        except:
            pass  # Constraint might already exist
        
        count = 0
        for c in customers:
            try:
                cursor.execute("""
                    INSERT IGNORE INTO customers (name, phone, email, address)
                    VALUES (%s, %s, %s, %s)
                """, (c["name"], c["phone"], c["email"], c["address"]))
                if cursor.rowcount > 0:
                    count += 1
            except Exception as e:
                print(f"Error inserting customer {c['name']}: {e}")
        
        print(f"Imported {count} customers successfully!")
        return True
        
    except FileNotFoundError:
        print("Error: customers_name.json not found in Json/ directory")
        return False
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in customers_name.json")
        return False

def main():
    """Main function to import all data"""
    print("=" * 50)
    print("Importing Data into Shop Billing System")
    print("=" * 50)
    
    # Connect to database
    try:
        conn = MySQLdb.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            passwd=Config.MYSQL_PASSWORD,
            db=Config.MYSQL_DB,
            port=Config.MYSQL_PORT
        )
        cursor = conn.cursor()
        print("✓ Connected to database successfully")
    except Exception as e:
        print(f"✗ Failed to connect to database: {e}")
        return
    
    # Import products
    print("\n📦 Importing products...")
    if import_products(cursor):
        conn.commit()
    else:
        print("✗ Failed to import products")
    
    # Import customers
    print("\n👥 Importing customers...")
    if import_customers(cursor):
        conn.commit()
    else:
        print("❌ Failed to import customers")
    
    # Close connection
    cursor.close()
    conn.close()
    print("\n" + "=" * 50)
    print("Import completed!")
    print("=" * 50)

if __name__ == "__main__":
    main()