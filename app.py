from flask import Flask, render_template, request, redirect, url_for, session
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
        tasks = db_operations.get_all_tasks()
        return render_template('index.html', logged_in=True, tasks=tasks)
    else:
        # Show the login page if not logged in
        return render_template('login.html', logged_in=False)

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = db.users.find_one({'username': username})
    
    # Check if a user with the given username exists
    if user is not None:
        db_password = user['password']
        if db_password == password:
            # Passwords match, proceed with login
            session['logged_in'] = True
            session['username'] = username
            session['user_id'] = str(user['_id'])
            return redirect(url_for('user_profile', username=username))
        else:
            # Passwords do not match
            return render_template('login.html', error='Invalid credentials', 
                                   input_password=password, db_password=db_password)
    else:
        # No user found with the provided username
        return render_template('login.html', error='Username not found', 
                               input_password=password, db_password='[User not found]')

@app.route('/logout', methods=['POST'])
def logout():
    # Clear the user session or authentication token
    session.clear()
    # Redirect to login page or home page after logout
    return redirect(url_for('login'))

@app.route('/<username>')
def user_profile(username):
    if 'logged_in' in session and session['username'] == username:
        # Ensure user_id is properly retrieved and used for task retrieval
        user_id = session.get('user_id')
        if not user_id:
            return redirect(url_for('index'))  # Redirect if user_id is not in session
        
        tasks = db_operations.get_all_tasks_for_user(db, username)
        return render_template('user_profile.html', logged_in=True, tasks=tasks, username=username)
    else:
        return redirect(url_for('index'))
    
@app.route('/add_task', methods=['POST'])
def add_task():
    if 'logged_in' not in session:
        return redirect(url_for('index'))
    
    task_name = request.form['name']
    task_status = request.form['status']
    task_info = request.form['info']
    db_operations.add_task(db, task_name, task_status, task_info)
    return redirect(url_for('user_profile', username=session['username']))

@app.route('/update_task/<task_id>', methods=['POST'])
def update_task(task_id):
    if 'logged_in' not in session:
        return redirect(url_for('index'))
    
    task_name = request.form['name']
    task_info = request.form['info']
    task_status = request.form['status']
    db_operations.update_task_db(db, task_id, task_name, task_info, task_status)
    return redirect(url_for('user_profile', username=session['username']))

@app.route('/delete_task/<task_id>', methods=['GET'])
def delete_task(task_id):
    if 'logged_in' not in session:
        return redirect(url_for('index'))
    
    db_operations.delete_task(db, task_id)
    return redirect(url_for('user_profile', username=session['username']))

# Ensure the following two functions exist in your db_operations module
# get_all_tasks() - To get all tasks for the logged-in user
# get_all_tasks_for_user(user_id) - To get tasks for a specific user by user_id
# add_task(), update_task_db(), and delete_task() - For CRUD operations on tasks

if __name__ == '__main__':
    app.run(debug=True)