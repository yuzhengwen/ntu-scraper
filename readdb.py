import db
course = db.collection.find_one({"course_code": "CZ1105"})
print(course)