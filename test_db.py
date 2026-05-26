import pymysql
from config import Config

try:
    connection = pymysql.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DB,
        port=Config.MYSQL_PORT
    )
    print("✅ MySQL connection successful!")
    connection.close()
except Exception as e:
    print(f"❌ MySQL connection failed: {e}")