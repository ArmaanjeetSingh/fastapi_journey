from fastapi  import FastAPI, Query
from typing import Annotated

app = FastAPI()

PRODUCTS = [
    {"id":1,"title":"Toothbrush","description":"doctor's prescription"},
    {"id":2,"title":"Slim fit T-shirts","description":"100% pure cotton"},
    {"id":3,"title":"Sports shoes","description":"best for football with spikes"},
    {"id":4,"title":"Backpack","description":"for travelling, hiking, trekking"}
]


# #Basic Query parameter
# @app.get("/products")
# async def get_products(search:str | None = None):
#     if search:
#         search_lower = search.lower()
#         filtered_products = []
#         for product in PRODUCTS:
#             if search_lower in product['title'].lower():
#                 filtered_products.append(product)
#         return filtered_products
#     return PRODUCTS

#Validation without Annotated
# @app.get("/products")
# async def get_products(search:str | None = Query(default = None, max_length = 5)):
#     if search:
#         search_lower = search.lower()
#         filtered_products = []
#         for product in PRODUCTS:
#             if search_lower in product['title'].lower():
#                 filtered_products.append(product)
#         return filtered_products
#     return PRODUCTS

#Validation with annotated
@app.get("/products")
async def get_products(search: 
    Annotated[str | None,
    Query(max_length = 5)]
    = None):
    if search:
        search_lower = search.lower()
        filtered_products = []
        for product in PRODUCTS:
            if search_lower in product['title'].lower():
                filtered_products.append(product)
        return filtered_products
    return PRODUCTS


# 