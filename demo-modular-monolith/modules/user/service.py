from shared.database import get_db
import sqlite3

class UserService:
    @staticmethod
    def create_user(email, name):
        conn = get_db()
        cursor = conn.cursor()
        try:
            cursor.execute(
                'INSERT INTO users (email, name) VALUES (?, ?)',
                (email, name)
            )
            user_id = cursor.lastrowid
            conn.commit()
            return {'id': user_id, 'email': email, 'name': name}
        except sqlite3.IntegrityError:
            raise ValueError('Email already exists')
        finally:
            conn.close()
    
    @staticmethod
    def get_all_users():
        conn = get_db()
        users = conn.execute('SELECT * FROM users').fetchall()
        conn.close()
        return [dict(user) for user in users]

