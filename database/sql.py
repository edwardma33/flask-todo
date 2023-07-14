import sqlite3
import random
from string import ascii_lowercase

# Setup table and connect
conn = sqlite3.connect('./database/db.sqlite', check_same_thread=False)
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS todos (id TEXT, body TEXT, username TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)")

def create_id():
    id = ''
    for i in range(8):
        picker = random.randint(0, 9)
        if picker > 5:
            id += ascii_lowercase[random.randint(0, len(ascii_lowercase) - 1)]
        else:
            id += str(random.randint(0, 9))
    return id

def get_todos(username):
    arr = []
    todos = c.execute("SELECT * FROM todos WHERE user = ?", (username, )).fetchall()
    
    for i in todos:
        arr.append({
            "id": i[0],
            "body": i[1]
        })
    return arr

def delete_todo(id):
    c.execute("DELETE FROM todos WHERE id = ?", (id, ))
    conn.commit()


class Todo():
    def __init__(self, body, username) -> None:
        self.id = create_id()
        self.body = str(body)
        self.username = username

    def save(self):
        c.execute("INSERT INTO todos VALUES (?, ?, ?)", (self.id, self.body, self.username))
        conn.commit()

def is_name_available(username):
    users = c.execute("SELECT * FROM users").fetchall()

    for user in users:
        if username in user[0]:
            return False
    return True

def sign_in(username, password):
    users = c.execute("SELECT * FROM users").fetchall()
    for user in users:
        if username in user and password in user:
            return True
    return False

class User():
    def __init__(self, username, password) -> None:
        self.username = username
        self.password = password

    def save(self):
        if is_name_available(self.username):
            c.execute("INSERT INTO users VALUES (?, ?)", (self.username, self.password))
            conn.commit()
            return True
        else:
            return False