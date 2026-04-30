from fastapi import FastAPI
from typing import Optional

app = FastAPI()

# Single Query Parameter
# @app.get("/product")
# async def product(category : str):
#     return {"status":"OK","category":category}

# Default Query Parameter
@app.get("/product")
async def product(category : Optional[str] = None, limit : int = 10):
    return {"status":"OK","category":category, "limit":limit}