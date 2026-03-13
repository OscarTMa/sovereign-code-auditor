import sqlite3

def get_user(username):
    # Vulnerabilidad: Inyección SQL por concatenación de strings
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    conn = sqlite3.connect('users.db')
    return conn.execute(query)
