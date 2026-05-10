from database.db import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash


class User:

    @staticmethod
    def register(name, email, password, role="patient"):
        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO users (name, email, password, role)
                VALUES (?, ?, ?, ?)
            """, (name, email, generate_password_hash(password), role))
            conn.commit()
            return True
        except Exception as e:
            print("Register Error:", e)
            return False
        finally:
            conn.close()

    @staticmethod
    def login(email, password):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE email=?", (email,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user["password"], password):
            return user
        return None

    @staticmethod
    def update_profile(user_id, name, email):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE users SET name=?, email=? WHERE id=?
        """, (name, email, user_id))

        conn.commit()
        conn.close()

    @staticmethod
    def reset_password(email, new_password):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE users SET password=? WHERE email=?
        """, (generate_password_hash(new_password), email))

        conn.commit()
        conn.close()

    @staticmethod
    def get_by_id(user_id):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
        user = cursor.fetchone()

        conn.close()
        return user