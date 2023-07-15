from flask import Flask, render_template, redirect, url_for, request, session
from flask_socketio import SocketIO
from database.sql import Todo, User, get_todos, delete_todo, sign_in, is_name_available, delete_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# this can also be database storage but this is temporary for learning
arr = []

# views
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', todos=get_todos(session['username']))

# funcs
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    if sign_in(username, password):
        session['username'] = username
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('index'))
    
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/signup', methods=['POST'])
def signup():
    username = request.form.get('username')
    password = request.form.get('password')
    
    if is_name_available(username):
        user = User(username, password)
        user.save()
        session['username'] = username
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('index'))

@app.route('/del_profile')
def del_profile():
    delete_user(session['username'])
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/add_todo', methods=['POST'])
def add_todo():
    body = request.form.get('body')
    username = session['username']
    todo = Todo(body, username)
    todo.save()
    return redirect(url_for('dashboard'))

@app.route('/del_todo/<id>')
def del_todo(id):
    delete_todo(id)
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')