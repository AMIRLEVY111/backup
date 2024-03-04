from pymongo import MongoClient
from bson.objectid import ObjectId


# db_operations.py
def get_all_tasks(db):
    return db.tasks.find()

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