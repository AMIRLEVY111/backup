# app.py
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import db_operations  # Assuming you have another Python file for DB operations

app = Flask(__name__)
db_client = MongoClient('mongodb://localhost:27017/')
db = db_client['task_management']

@app.route('/')
def index():
    tasks = db_operations.get_all_tasks(db)
    return render_template('index.html', tasks=tasks)

@app.route('/add_task', methods=['POST'])
def add_task():
    task_name = request.form['name']
    task_status = request.form['status']
    task_info = request.form['info']
    db_operations.add_task(db, task_name, task_status, task_info)
    return redirect(url_for('index'))
# Add more routes as needed

@app.route('/update_task/<task_id>', methods=['GET'])
def update_task(task_id):
    # Placeholder for your update logic
    db_operations.update_task(task_id)
    return redirect(url_for('index'))

@app.route('/delete_task/<task_id>', methods=['GET'])
def delete_task(task_id):
    # Placeholder for your delete logic
    db_operations.delete_task(db, task_id)
    return redirect(url_for('index'))
if __name__ == '__main__':
    app.run(debug=True)
    
