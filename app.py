from flask import Flask, render_template, request, redirect, url_for, session,flash
from pymongo import MongoClient
from werkzeug.security import check_password_hash, generate_password_hash
import db_operations  # Replace with your actual DB operations module

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
db_client = MongoClient('mongodb://localhost:27017/')
db = db_client['task_management']

@app.route('/')
def index():
    if 'logged_in' in session:
        # Assuming get_all_tasks() fetches tasks for the logged-in user
        username = session['username'] 
        tasks = db_operations.get_all_tasks(db, username)
        return redirect(url_for('user_profile', username=session['username']))
    else:
       # Show the homepage with login and register options if not logged in
        return render_template('homepage.html', logged_in=False)

@app.route('/login-page')
def show_login():
    # This route just shows the login page
    return render_template('login.html')

@app.route('/register-page')
def show_register():
    # This route just shows the registration page
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username'] 
    password = request.form['password']
    if len(username) <= 3:
        flash('Username must be longer than 4 characters.')
        return redirect(url_for('show_register'))  # Redirect back to the registration form
    if len(password) <= 7:
        flash('Password must be longer than 8 characters.')
        return redirect(url_for('show_register'))  # Redirect back to the registration form

    password_hash = generate_password_hash(password)

    if db_operations.check_new_user(username, password_hash, db):
        db_operations.add_new_user(username, password_hash, db )
        flash('User registered successfully.')
        return redirect(url_for('show_login'))  # Redirect to the login page or home page after registration
    else:
        flash('Username already exists. Choose a different username.')
        return redirect(url_for('show_register'))
    
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']  # This is the plaintext password from the form
    # Find the user in the database
    user = db.users.find_one({'username': username})
    if user:
        # We assume the password hash is stored under the key 'password_hash'
        password_hash = user['password_hash']
        # Verify the password
        if check_password_hash(password_hash, password):
            # Password is correct
            session['logged_in'] = True
            session['username'] = username
            session['user_id'] = str(user['_id'])
            # Redirect to the user's profile or another appropriate page
            return redirect(url_for('user_profile', username=username))
        else:
            # Incorrect password
            flash('Invalid username or password')
    else:
        # Username not found
        flash('Invalid username or password')
    # In case of failure, re-render the login page with an error message
    return render_template('login.html', error='Invalid username or password')

@app.route('/logout', methods=['POST'])
def logout():
    # Clear the user session or authentication token
    session.clear()
    # Redirect to login page or home page after logout
    return redirect(url_for('index'))
@app.route('/<username>')
def user_profile(username):
    if 'logged_in' in session and session['username'] == username:
        user_id = session.get('user_id')
        edit_task_id = request.args.get('edit_task_id')  # Assuming you pass this as a query parameter.
        tasks = db_operations.get_all_tasks_for_user(db, username)
        return render_template('user_profile.html', logged_in=True, tasks=tasks, username=username, user_id=user_id, edit_task_id=edit_task_id)
    else:
        return redirect(url_for('show_login'))

@app.route('/add_task', methods=['POST'])
def add_task():
    if 'logged_in' not in session:
        return redirect(url_for('show_login'))
    username = session['username'] 
    task_name = request.form['name']
    task_status = request.form['status']
    task_info = request.form['info']
    db_operations.add_task(db, task_name, task_status, task_info, username)
    return redirect(url_for('user_profile', username=session['username']))

@app.route('/update_task/<task_id>', methods=['POST'])
def update_task(task_id):
    if 'logged_in' not in session:
        return redirect(url_for('show_login'))
    username = session['username'] 
    task_name = request.form['name']
    task_info = request.form['info']
    task_status = request.form['status']
    db_operations.update_task_db(db, task_id, task_name, task_info, task_status, username)
    return redirect(url_for('user_profile', username=session['username']))

@app.route('/edit_task/<task_id>')
def edit_task(task_id):
    if 'logged_in' not in session:
        flash('Please log in to edit tasks.')
        return redirect(url_for('show_login'))
    # Assuming get_task_by_id is a function in db_operations that retrieves a single task by its ID
    task_to_edit = db_operations.get_task_by_id(db, task_id)
    return render_template('edit_task.html', task=task_to_edit)

@app.route('/delete_task/<task_id>', methods=['GET'])
def delete_task(task_id):
    if 'logged_in' not in session:
        return redirect(url_for('show_login'))
    username = session['username'] 
    db_operations.delete_task(db, task_id, username)
    return redirect(url_for('user_profile', username=session['username']))

# Ensure the following two functions exist in your db_operations module
# get_all_tasks() - To get all tasks for the logged-in user
# get_all_tasks_for_user(user_id) - To get tasks for a specific user by user_id
# add_task(), update_task_db(), and delete_task() - For CRUD operations on tasks

if __name__ == '__main__':
    app.run(debug=True)