# db_operations.py
def get_all_tasks(db):
    return db.tasks.find()

def add_task(db, task):
    db.tasks.insert_one(task)

# Implement more database operations as needed
