from fastapi  import FastAPI

app = FastAPI()

@app.get("/product/rode_nt_str")
async def single_product_static():
    return {'response':'Single product fetched'}

## Always put static over dynamic
@app.get("/product/{product_title}")
async def single_product(product_title : str):
    return {'response':'Single product fetched','product_title':product_title}

