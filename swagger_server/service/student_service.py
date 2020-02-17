import json
import logging
import os
import tempfile

from tinydb import TinyDB, Query
from tinydb.middlewares import CachingMiddleware
from functools import reduce
import uuid

from swagger_server.models import Student
from swagger_server.mongo import MongoAdapter as mdb

db_dir_path = tempfile.gettempdir()
print(db_dir_path)
db_file_path = os.path.join(db_dir_path, "students.json")
student_db = TinyDB(db_file_path)

student_db_mongo = mdb.connect_to_mongo_db("78.47.131.57", 27017, "devopslab2_filippandza")

def add_student(student):
    if(student.first_name == None or student.last_name == None):
        return 'You must provide both first name and last name', 405

    res = mdb.find_from_db_containing_first_last_name(student_db_mongo, "students", "first_name", student.first_name, "last_name", student.last_name)
    
    if res.count() != 0:
        return 'already exists', 409

    #doc_id = student_db.insert(student.to_dict())
    highestIDRow = mdb.find_highest_id(student_db_mongo, "students")
    #print(highestIDRow.count())
    
    if highestIDRow.count() == 0:
        newID = 2
    else:
        row = highestIDRow.next()

        #print(row)
        #print(row["student_id"])
        
        highestID = row["student_id"]
        
        if highestID == None:
            newID = 2
        else:
            newID = highestID + 1
        
    student.student_id = newID
    mdb.write_row_to_mongo_db(student.to_dict(), "students", student_db_mongo)
    print(newID)
    #student.student_id = doc_id
    return student.student_id

def get_student_by_id(student_id, subject):
    #student = student_db.get(doc_id=int(student_id))
    #if not student:
    #    return student
    
    student = mdb.find_by_id(student_db_mongo, "students", student_id)
    
    if student.count() == 0:
        return None
    
    student = Student.from_dict(student.next())
    if not subject:
        return student
    
    if subject in student.grades.keys():
        return student
        
def get_student_by_last_name(last_name):
    #students = Query()
    #print(last_name)
    #student = student_db.search(students.last_name == last_name)
    #print(student)
    
    student = mdb.find_from_db_containing_last_name(student_db_mongo, "students", last_name)
    
    if student.count() == 0:
        return None

    student = student.next()
    student = Student.from_dict(student)
    #print(student)
    return student

def delete_student(student_id):
    #student = student_db.get(doc_id=int(student_id))
    #if not student:
    #    return student
    student = mdb.find_by_id(student_db_mongo, "students", student_id)
    
    if student.count() == 0:
        return None
    
    #student_db.remove(doc_ids=[int(student_id)])
    mdb.delete_by_id(student_db_mongo, "students", student_id)
    return student_id
