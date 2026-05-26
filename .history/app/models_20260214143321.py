from flask_login import UserMixin
from app import login_manager
from app.db import get_db
import pymysql

class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username

@login_manager.user_loader
def load_user(user_id):
    connection = get_db()
    if not connection:
        return None
    
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cur:
            cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
            user = cur.fetchone()
            if user:
                return User(user['id'], user['username'])
            return None
    except Exception as e:
        print(f"Error loading user: {e}")
        return None
    finally:
        if connection:
            connection.close()