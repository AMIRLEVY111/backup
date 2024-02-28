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

# Add more routes as needed

if __name__ == '__main__':
    app.run(debug=True)
