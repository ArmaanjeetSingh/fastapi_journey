from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Literal
import json

class Employee(BaseModel):
    employee_id : Optional[int] = Field(gt=100,default=None)
    name : str = Field(min_lenght=3, max_length=20)
    department : Literal["sales","finance","H R","I T"]
    salary : float = Field(ge=10000, lt=90000)
    age : int = Field(ge = 18, lt = 60)
    email : EmailStr
    is_active : Optional[bool] = Field(default=False)



app = FastAPI()


def load_employees_data():
    with open("employees.json","r") as f:
        data = json.load(f)
        return data  


def write_employees_data(data):
    with open("employees.json","w") as f:
        json.dump(data,f,indent=4)


@app.get("/employees")
async def get_employees():
    employees = load_employees_data()
    return employees


@app.get("/employees/{employee_id}/")
async def get_employee(employee_id : int):
    employees = load_employees_data()
    employee_found = 0
    for employee in employees:
        if employee.get("employee_id") == employee_id:
            employee_found = 1
            return employee
    if not employee_found:
        raise HTTPException(status_code=404,detail="no such id exists")



@app.post("/employees")
async def create_employees(employee : Employee):
    employees = load_employees_data()
    for employ in employees:
        if employ.get("employee_id") == employee.employee_id:
            raise HTTPException(status_code=400, detail='id already exists')
    employee1 = find_employee_id(employee,employees) 
    # print(employee1)     
    employees.append(employee1.model_dump())
    # print(employees)
    write_employees_data(employees)


@app.put("/employees")
async def update_employee(employee : Employee):
    employees = load_employees_data()
    for employ in employees:
        if employ.get("employee_id") == employee.employee_id:
            employ.update(employee.model_dump())

            write_employees_data(employees)
            return {"message":"Employee updated successfully"}
    raise HTTPException(status_code=404,detail=f'No such employee id exists')



@app.delete("/employees/{employee_id}")
async def delete_employee(employee_id : int = Path(gt = 100)):
    employees = load_employees_data()
    for employ in employees:
        if employ.get("employee_id") == employee_id:
            employees.remove(employ)
            write_employees_data(employees)
            return {"message":"Employee deleted successfully"}
    raise HTTPException(status_code=404,detail=f'No such employee id exists')



def find_employee_id(employee : Employee, employees: list):
    employee.employee_id = 1 if len(employees) < 0 else employees[-1].get('employee_id') + 1
    return employee