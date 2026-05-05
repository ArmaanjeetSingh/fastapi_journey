from sqlmodel import Field, SQLModel, Relationship

class UserAddressLink(SQLModel, table = True):
    user_id : int = Field(primary_key = True,foreign_key = 'user.id',ondelete = "CASCADE")
    address_id : int = Field(primary_key = True,foreign_key = 'address.id',ondelete = 'CASCADE')


class User(SQLModel, table = True):
    id : int = Field(gt = 0,primary_key=True)
    name : str 
    email : str

    profile : "Profile" = Relationship(back_populates = 'user', cascade_delete = True) #bidrectional access
    posts : list["Post"] | None = Relationship(back_populates = 'user',cascade_delete = True) 
    address : list["Address"] | None = Relationship(back_populates = 'user',link_model = UserAddressLink,cascade_delete = True) 

    def __repr__(self)->str:
        return f"User (id : {self.id} name : {self.name} email {self.email})"

class Profile(SQLModel, table = True):
    id : int = Field(gt = 0,primary_key=True)
    bio : str
    user_id : int = Field(foreign_key = 'user.id',unique = True,ondelete = "CASCADE")

    user : "User" = Relationship(back_populates = 'posts')


class Post(SQLModel, table = True):
    id : int = Field(gt = 0,primary_key=True)
    title : str
    content : str
    user_id : int = Field(foreign_key = 'user.id',ondelete = "SET NULL",nullable = True)


class Address(SQLModel, table = True):
    id : int = Field(gt = 0,primary_key=True)
    street : str
    city : str

    user : list["User"] | None = Relationship(back_populates = 'adddress',link_model = UserAddressLink,cascade_delete = True) 