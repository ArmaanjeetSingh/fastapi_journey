from pydantic import BaseModel, Field

class CategoryCreate(BaseModel):
    name : str = Field(max_length= 10)
