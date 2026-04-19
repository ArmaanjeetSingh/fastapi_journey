from fastapi import FastAPI, Path, Query
from pydantic import BaseModel, Field
from typing import Optional
import json


class Medicine(BaseModel):
    name : str
    manufacturer : str = Field(max_length = 20)
    category : str
    stock : int = Field(gt = 0)
    price : float 
    expiry_date : Optional[str] = None



def load_medicine_data():
    with open("medicine.json","r") as f:
        data = json.load(f)
        return data  

def write_medicine_data(data):
    with open("medicine.json","w") as f:
        json.dump(data,f,indent=4)


app = FastAPI()

@app.get("/medicine")
async def get_medicine_by_filter(category : Optional[str] = None, stock_lt : Optional[int] = None):
    medicines_to_return = []
    medicines = load_medicine_data()
    for medicine in medicines:
        if category is not None and category.casefold() != medicine.get("category").casefold():
            continue
        if stock_lt is not None and stock_lt > medicine.get("stock"):
            continue
        medicines_to_return.append(medicine)
    return medicines_to_return


#get medicine by name
@app.get("/medicine/{medicine_name}")
async def get_medicine_by_name(medicine_name : str):
    medicines = load_medicine_data()
    for medicine in medicines:
        if medicine.get("name").casefold() == medicine_name.casefold():
            return {"message":medicine}
    return {"error":"medicine doesn't exists"}


#create medicine
@app.post("/medicine/create_medicine")
async def create_medicine(medicine : Medicine):
    medicines = load_medicine_data()
    for med in medicines:
        if med['name'].casefold() == medicine.name.casefold():
            return {"error":"medicine alredy exists"}
    medicines.append(medicine.model_dump())
    write_medicine_data(medicines)
    return {"message":"medicine added successfully"}


#update medicine
@app.put("/medicine/")
async def update_medicine(medicine:Medicine):
    medicines = load_medicine_data()
    for med in medicines:
        if medicine.name == med['name']:
            med.update(medicine.model_dump())
            write_medicine_data(medicines)
            return {"message":"medicine updated successfully"}
    return {"error":"no such medicine found"}


@app.delete("/medicine/{medicine_name}")
async def delete_medicine(medicine_name:str):
    medicines = load_medicine_data()
    for med in medicines:
        if medicine_name == med['name']:
            medicines.remove(med)
            write_medicine_data(medicines)
            return {"message":"medicine deleted successfully"}
    return {"error":"no such medicine found"}