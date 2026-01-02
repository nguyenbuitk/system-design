from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)
DB_FILE = 'database/users.db'
PORT = 5001

def init_db():
    os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            email TEXT UNIQUE,
            name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.json
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute(
            'INSERT INTO users (email, name) VALUES (?, ?)',
            (data['email'], data['name'])
        )
        user_id = cursor.lastrowid
        conn.commit()
        return jsonify({'id': user_id, 'email': data['email'], 'name': data['name']}), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Email already exists'}), 400
    finally:
        conn.close()

@app.route('/api/users', methods=['GET'])
def get_users():
    conn = get_db()
    users = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    return jsonify([dict(user) for user in users])

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    conn = get_db()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    if user:
        return jsonify(dict(user))
    return jsonify({'error': 'User not found'}), 404

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'service': 'user-service'})

if __name__ == '__main__':
    init_db()
    print(f"\nUser Service running on http://localhost:{PORT}")
    app.run(host='0.0.0.0', port=PORT, debug=True)

