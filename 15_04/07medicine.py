from fastapi import FastAPI
from medicine import medicines
from typing import Optional

app = FastAPI()

@app.get("/medicines")
def get_all_medicines(category : Optional[str] = None):
    if category:
        medicine_list = []
        for medicine in medicines:
           if category.casefold() == medicine['category']:
              medicine_list.append(medicine)
        return medicine_list

    return medicines


@app.get("/medicines/byName/{name}")
def get_medicine_by_name(name : Optional[str] = None,manufacturer : str = None):
    medicine_list = []
    for medicine in medicines:
        if medicine.get("medicine_name").casefold() == name.casefold() and name is not None:
            return {"message":medicine}

    return {"error":"medicine not found"}


# Get medicines by manufacturer
@app.get("/medicines/byManufacturer/{manufacturer}")
def get_medicine_by_manufact(manufacturer : str = None):
    for medicine in medicines:
        if medicine.get("manufacturer").casefold() == manufacturer.casefold():
            return {"message":medicine}

    return {"error":"medicine not found"}


#Add new medicine
@app.post("/medicines/add_medicine")
def add_medicine(new_medicine = Body()):
    for i in range(len(medicines)):
        if new_medicine['medicine_name'].casefold() == medicines[i].get('medicine_name').casefold():
            return {"message":"medicine already exists"}
    medicines.append(new_medicine)
    return {"message":"Medicine added successfully","medicine":new_medicine}


#Delete Medicine
@app.post("/medicines/delete_medicine/{name}")
def add_medicine(name : str):
    for i in range(len(medicines)):
        if name.casefold() == medicines[i].get("medicine_name").casefold():
            deleted_medicine = medicines.pop(i)
            return {"message":deleted_medicine}
    return {"message":"medicine not found"}