from fastapi import FastAPI, status, Query, Path

from pydantic import BaseModel, EmailStr, Field
from typing import Annotated

class Student(BaseModel):
    name : Annotated[str,Field(max_length = 30)]
    email : EmailStr
    age : Annotated[int,Field(ge = 16, lt = 60)]
    course : list[str]
    marks : Annotated[float,Field(ge = 0,lt = 100)]


STUDENTS = [
    {"id":1,"name":"Sumit","email":"sumit12@gmail.com","age":18,"course":["Accounts","IT"],"marks":56.78},
    {"id":2,"name":"Armaan","email":"st12@gmail.com","age":18,"course":["IT","Diploma"],"marks":96.21},
    {"id":3,"name":"Simran","email":"mran134@yahoo.com","age":36,"course":["Btech","IT","Home science"],"marks":85.34},
    {"id":4,"name":"Shruti","email":"so456@gmail.com","age":28,"course":["Btech","IT"],"marks":61.23},
    {"id":5,"name":"Arjun","email":"aer12@gmail.com","age":25,"course":["Btech","IT"],"marks":61.23},
]

app = FastAPI()


@app.get("/students",status_code = status.HTTP_200_OK)
async def get_all_students(course : Annotated[str|None, Query(alias = 'c')] = None, min_marks : Annotated[float|None,Query()] = None):
    filtered_products = []
    for student in STUDENTS:
        if course is not None and course not in student.get("course"):
            continue
        if min_marks is not None and min_marks > student.get("marks"):
            continue
        filtered_products.append(student)
    return filtered_products


@app.get("/students/{student_id}",status_code = status.HTTP_200_OK)
async def get_student_by_id(student_id : Annotated[int,Path(gt = 0)]):
    for student in STUDENTS:
        if student_id == student.get("id"):
            return student
    return {"status":"Student not found"}


@app.post("/students",status_code = status.HTTP_201_CREATED)
async def create_student(student : Student):
    create_student = student.model_dump()
    create_student['id'] = len(STUDENTS)+1
    STUDENTS.append(create_student)
    {"status":"student created successfully"}


@app.put("/students/{student_id}",status_code = status.HTTP_204_NO_CONTENT)
async def update_student(student_id : Annotated[int,Path(gt = 0)],update_student : Student):
    for index,student in enumerate(STUDENTS):
        if student_id == student.get("id"):
            student_model = update_student.model_dump()
            student_model.update({"id":student_id})
            STUDENTS[index] = student_model
            return {"status":"Student updated successfully"}
    return {"status":"Student not found"}
    

@app.delete("/students/{student_id}",status_code = status.HTTP_204_NO_CONTENT)
async def delete_student(student_id : Annotated[int,Path(gt = 0)]):
    for index,student in enumerate(STUDENTS):
        if student_id == student.get("id"):
            STUDENTS.pop(index)
            return {"status":"Student deleted successfully"}
    return {"status":"Student not found"}
