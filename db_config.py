import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",          # default user XAMPP
        password="",          # kosongkan jika tidak ada password
        database="db_flask"   # nama database
    )