from flask import Flask, render_template, request, redirect
import mysql.connector
from db_config import DB_CONFIG

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    return render_template('index.html', users=users)

@app.route('/add', methods=['POST'])
def add_user():
    name = request.form['name']
    email = request.form['email']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
    conn.commit()
    conn.close()

    return redirect('/')

@app.route('/delete/<int:user_id>')
def delete_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id=%s", (user_id,))
    conn.commit()
    conn.close()

    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

