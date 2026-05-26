import pymysql
import pymysql.cursors
from config import Config

def get_db():
    """Get database connection"""
    try:
        connection = pymysql.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DB,
            port=Config.MYSQL_PORT,
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )
        return connection
    except Exception as e:
        print(f"Database connection error: {e}")
        return None