from flask import Flask, render_template, request, redirect, url_for, jsonify
from db_config import get_db_connection
import mysql.connector

app = Flask(__name__)

# Helper function untuk query dictionary
def dict_cursor_execute(query, params=None):
    """Helper untuk eksekusi query dan hasilnya berupa list of dict."""
    temp_db = get_db_connection()
    temp_cursor = temp_db.cursor(dictionary=True)
    if params:
        temp_cursor.execute(query, params)
    else:
        temp_cursor.execute(query)
    results = temp_cursor.fetchall()
    temp_db.close()
    return results

# Route utama (GUI)
@app.route('/')
def index():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    connection.close()
    return render_template("index.html", users=users)

# Route tambah user (GUI)
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        nama = request.form['nama']
        email = request.form['email']
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO users (nama, email) VALUES (%s, %s)", (nama, email))
        connection.commit()
        connection.close()
        return redirect(url_for('index'))
    return render_template('add.html')

# Route detail user (GUI)
@app.route('/user/<int:id>')
def detail(id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE id = %s", (id,))
    user = cursor.fetchone()
    connection.close()
    return render_template('detail.html', user=user)

# Route update user (GUI dan API Postman)
@app.route('/update/<int:id>', methods=['GET', 'POST', 'PUT'])
def update(id):
    if request.method == 'POST':
        # Update dari Form HTML
        nama = request.form['nama']
        email = request.form['email']
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("UPDATE users SET nama=%s, email=%s WHERE id=%s", (nama, email, id))
        connection.commit()
        connection.close()
        return redirect(url_for('index'))

    elif request.method == 'PUT':
        # Update dari Postman
        data = request.get_json()
        nama = data['nama']
        email = data['email']
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("UPDATE users SET nama=%s, email=%s WHERE id=%s", (nama, email, id))
        connection.commit()
        connection.close()
        return jsonify({"message": "User berhasil diupdate", "id": id})

# Route delete user (GUI)
@app.route('/delete/<int:id>')
def delete(id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM users WHERE id = %s", (id,))
    connection.commit()
    connection.close()
    return redirect(url_for('index'))

# API - Get All Users
@app.route('/api/users', methods=['GET'])
def api_get_users():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    connection.close()
    return jsonify(users)

# API - Tambah User
@app.route('/api/users', methods=['POST'])
def api_add_user():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400

    nama = data.get('nama')
    email = data.get('email')
    if not nama or not email:
        return jsonify({'error': 'Missing nama or email'}), 400

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('INSERT INTO users (nama, email) VALUES (%s, %s)', (nama, email))
    connection.commit()
    connection.close()
    return jsonify({'message': 'User berhasil ditambahkan'}), 201

# API - Update User
@app.route('/api/users/<int:id>', methods=['PUT'])
def api_update_user(id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400

    nama = data.get('nama')
    email = data.get('email')
    if not nama or not email:
        return jsonify({'error': 'Missing nama or email'}), 400

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('UPDATE users SET nama = %s, email = %s WHERE id = %s', (nama, email, id))
    connection.commit()
    connection.close()
    return jsonify({'message': 'User berhasil diupdate'})

# API - Delete User
@app.route('/api/users/<int:id>', methods=['DELETE'])
def api_delete_user(id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('DELETE FROM users WHERE id = %s', (id,))
    connection.commit()
    connection.close()
    return jsonify({'message': 'User berhasil dihapus'})

# API - Get User By ID
@app.route('/api/users/<int:id>', methods=['GET'])
def api_get_user_by_id(id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM users WHERE id = %s', (id,))
    user = cursor.fetchone()
    connection.close()

    if user:
        return jsonify(user)
    else:
        return jsonify({'message': 'User tidak ditemukan'}), 404

if __name__ == '__main__':
    app.run(debug=True)
