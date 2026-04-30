from fastapi import FastAPI

app = FastAPI()


# GET Request
## Read or fetch all data
@app.get("/product")
async def all_products():
    return {'response':"return all products"}


## Read or fetch single product
@app.get("/product/{product_id}")
async def get_product(product_id : int):
    return {"response":"Single product fetched","id":product_id}


## POST Request
## Create or Insert data
@app.post("/product")
async def create_product(new_proudct : dict):
    return {'response':'Product created','new_product':new_product}


## PUT Request
## Update data
@app.put("/product/{product_id}")
async def update_product(product_id:int, new_updated_product : dict):
    return {'response':'Complete Data Updated','product_id':product_id,"new_updated_product":new_updated_product}


## PATCH Request
## Update data
@app.patch("/product/{product_id}")
async def partial_update_product(product_id:int, new_updated_product : dict):
    return {'response':'Partial Data Updated','product_id':product_id,"new_updated_product":new_updated_product}


## DELETE Request
## Delete data
@app.delete("/product/{product_id}")
async def delete_product(product_id:int):
    return {'response':'Complete Data Updated','product_id':product_id,"new_updated_product":new_updated_product}