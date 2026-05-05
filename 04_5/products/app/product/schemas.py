from pydantic import BaseModel, Field

class ProductCreate(BaseModel):
    name : str = Field(max_length= 10)
    stock : int = Field(gt = 0)
    price : float = Field(gt = 0)
    category_id : int