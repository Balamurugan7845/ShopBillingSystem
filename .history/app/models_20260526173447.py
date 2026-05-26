from flask_login import UserMixin
from app import login_manager
from app.db import get_db

import pymysql

# =========================================
# USER MODEL
# =========================================

class User(UserMixin):

    def __init__(

        self,
        id,
        username,
        password,
        role

    ):

        self.id = id

        self.username = username

        self.password = password

        self.role = role

# =========================================
# LOAD USER
# =========================================

@login_manager.user_loader

def load_user(user_id):

    connection = get_db()

    if not connection:

        return None

    try:

        with connection.cursor(
            pymysql.cursors.DictCursor
        ) as cur:

            cur.execute(

                """
                SELECT *
                FROM users
                WHERE id = %s
                """,

                (user_id,)
            )

            user = cur.fetchone()

            if user:

                return User(

                    user["id"],
                    user["username"],
                    user["password"],
                    user["role"]

                )

            return None

    except Exception as e:

        print(
            f"Error loading user: {e}"
        )

        return None

    finally:

        if connection:

            connection.close()