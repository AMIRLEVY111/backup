from pymongo import MongoClient
from bson.objectid import ObjectId

def check_new_user(username, password_hash, db):
    existing_user = db.users.find_one({"username": username})
    return existing_user is None

def add_new_user(username, password_hash, db):
    db.users.insert_one({"username": username, "password_hash": password_hash})
# db_operations.py
def get_all_tasks(db, collection):
    return db.collection.find()

def add_task(db, task_name, task_status, task_info):
    # Insert the new task into the tasks collection
    db.tasks.insert_one({'name': task_name, 'status': task_status, 'info': task_info})
    
def delete_task(db, task_id):
    # Converts the string task_id to an ObjectId because MongoDB uniquely identifies documents using ObjectId
    #not strings, ensuring accurate document operations.
    task_id_obj = ObjectId(task_id)
    db.tasks.delete_one({'_id': task_id_obj})

def update_task_db(db, task_id, name, info, status):
    # Convert task_id to ObjectId
    task_id_obj = ObjectId(task_id)
    
    # Update the task in the database
    result = db.tasks.update_one(
        {'_id': task_id_obj},
        {'$set': 
            {
                'name': name,
                'info': info,
                'status': status
            }
        }
    )
    return result.modified_count  # Returns the count of documents modified

def get_all_tasks_for_user(db, username):
    # Assuming each user has a collection named after their user_id for their tasks
    collection = db[username]  # Access collection dynamically based on user_id
    tasks = collection.find()  # Find all tasks in the user's collection
    tasks_list = list(tasks)  # Convert to list
    return tasks_list
