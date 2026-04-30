# from enum import Enum
# from fastapi import FastAPI 


# ## Predefined values
# ## Define enum class with allowed product categories
# class ProductCategory(str, Enum):
#     books = "books"
#     clothing = "clothing"
#     electronics = "Electronics"

# # Use the enum class as type of path parameters
# app = FastAPI()
# @app.get("/product/{category}")
# async def get_products(category : ProductCategory):
#     return {"response":"Product Fetched","category":category}


from enum import Enum
from fastapi import FastAPI 


## Predefined values
## Define enum class with allowed product categories
class ProductCategory(str, Enum):
    books = "books"
    clothing = "clothing"
    electronics = "Electronics"

# Use the enum class as type of path parameters
app = FastAPI()
@app.get("/product/{category}")
async def get_products(category : ProductCategory):
    if category.value == ProductCategory.books:
        return {"response":"books is awesome !!!"}
    elif category.value == ProductCategory.electronics:
        return {"response":"Learn to create new gadgets"}
    else:
        return {"response":"unknown category"}