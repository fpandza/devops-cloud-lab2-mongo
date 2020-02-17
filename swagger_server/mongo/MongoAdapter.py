import pymongo
from bson import ObjectId


def connect_to_mongo_db(mongo_host, mongo_port, mongo_db_name, username=None, password=None):
    con = pymongo.MongoClient(mongo_host, mongo_port) #, username=username, password=password
    return con[mongo_db_name]

def write_row_to_mongo_db(data_row, collection_name, mongo_db_connection):
    collection = mongo_db_connection[collection_name]
    return collection.insert_one(data_row)

def find_n_rows_from_db(amount_of_rows, connection, collection_name):
    return connection[collection_name].find().limit(amount_of_rows)

def find_n_rows_from_db_containing_string(amount_of_rows, connection, collection_name, column_name, string_value):
    return connection[collection_name].find({column_name: {'$regex': '.*' + string_value + '.*'}}).limit(amount_of_rows)

def find_from_db_containing_first_last_name(connection, collection_name, column_name, string_value, column_name2, string_value2):
    return connection[collection_name].find({column_name: string_value, column_name2: string_value2})
   
def find_from_db_containing_last_name(connection, collection_name, string_value):
    return connection[collection_name].find({"last_name": string_value}).limit(1)
   
def find_highest_id(connection, collection_name):
    return connection[collection_name].find().sort([("student_id",-1)]).limit(1)    

def find_by_id(connection, collection_name, student_id):
    return connection[collection_name].find({"student_id": student_id}).limit(1)

def delete_by_id(connection, collection_name, student_id):
    return connection[collection_name].delete_one({'student_id': student_id})    
    
#db.students.find().sort({student_id:-1}).limit(1).pretty()