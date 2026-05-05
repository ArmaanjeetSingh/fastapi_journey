from sqlmodel import Field,SQLModel
class User(SQLModel, table = True):
    id : int = Field(gt = 0,primary_key=True)
    name : str 
    email : str
