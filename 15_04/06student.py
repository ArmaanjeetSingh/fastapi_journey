from student import students
from fastapi import FastAPI, Body

app = FastAPI()

@app.get("/students")
def get_all_students(course : str = None,min_marks : int = None):
    # if course is not None:
    #     student_list = []
    #     for student in students:
    #         if student['course'].casefold() == course.casefold():
    #             student_list.append(student)
    #     return student_list
    
    student_list = []
    for student in students:
        if course is not None and student['course'].casefold() != course.casefold():
            continue
        if min_marks is not None and student['marks'] < min_marks:
            continue
        student_list.append(student)
    return student_list

#get student by roll
@app.get("/students/{roll_id}")
def get_student_by_roll(roll_id : int):
        for student in students:
            if student.get('roll_no') == roll_id:
                return student
        return {"message":"student not found"}


@app.post("/students/add_student/")
def add_student(new_student = Body()):
    for student in students:
        if student.get('roll_no') == new_student.get('roll_no'):
            return {"error":"student already exists"}
    students.append(new_student)
    return {"message":"New student added successfully"}
    


@app.put("/students/update_student/{roll_id}")
def update_student(roll_id : int,new_student = Body()):
    for student in students:
        if student.get('roll_no') == roll_id:
           student.update(new_student)
           return {"message":"Student updated successfully"}
    return {"error":"student not found"}


@app.delete("/students/delete_student/{roll_id}")
def delete_student(roll_id : int):
    for i in range(len(students)):
        if students[i].get('roll_no') == roll_id:
           students.pop(i)
           return {"message":"Student deleted successfully"}
    return {"error":"student not found"}