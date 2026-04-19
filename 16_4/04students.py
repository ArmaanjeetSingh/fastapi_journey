from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional
import json

class Student(BaseModel):
    name : str = Field(min_length=3)
    roll_no : Optional[int] = Field(gt = 120, lt = 140, default = None)
    course : str = Field(max_length= 10)
    marks : float = Field(gt = 33, lt = 100)

app = FastAPI()

def load_student_data():
    with open("student.json","r") as f:
        data = json.load(f)
        return data

def write_student_data(data):
    with open("student.json","w") as f:
        json.dump(data,f,indent=4)
        print("data appended to file")


@app.get("/students")
async def get_all_students(course: Optional[str] = None,marks : Optional[float] = None):
    data = load_student_data()
    student_to_return = []
    for student in data:
        if course is not None and student.get("course").casefold() != course.casefold():
            continue

        if marks is not None and marks > student.get("marks"):
            continue
        student_to_return.append(student)
    return student_to_return if student_to_return else {"message":"no student found"}



@app.post("/students/create_student")
async def create_student(student : Student):
    data = load_student_data()
    # print(type(data))
    for i in range(len(data)):
        if data[i].get('roll_no') == student.roll_no:
            return {"error":"Student already exists"}

    data_append = find_roll_num(student)
    data.append(data_append.model_dump())
    write_student_data(data)
    return {"message":"Student created successfully"}


@app.put("/students/update_student/{roll_no}")
async def update_student(student : Student,roll_no : int):
    data = load_student_data()
    for i in range(len(data)):
        if data[i].get('roll_no') == roll_no:
            data[i] = student.model_dump()
            write_student_data(data)
            return {"message":"student updated successfully"}
    return {"error":"no student exists with such roll no"}


@app.delete("/students/delete_student/{roll_no}")
async def delete_student(roll_no : int):
    data = load_student_data()
    for i in range(len(data)):
        if data[i].get('roll_no') == roll_no:
            deleted = data.pop(i)
            write_student_data(data)
            return {"message":"Student deleted successfully","student":deleted}
    


def find_roll_num(student : Student):
    data  = load_student_data()
    student.roll_no = data[-1].get('roll_no') + 1 if data else 121
    return student
