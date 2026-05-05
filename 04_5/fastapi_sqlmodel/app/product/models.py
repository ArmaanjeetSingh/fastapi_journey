from sqlmodel import Field,SQLModel
class Product(SQLModel, table = True):
    id : int = Field(gt = 0,primary_key=True)
    name : str 
    price : str
    quantity : str
