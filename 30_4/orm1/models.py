from db import engine
from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey

metadata = MetaData()

users = Table(
    "users",
    metadata,
    Column("id",Integer,primary_key = True),
    Column("name",String(length = 20),nullable = False),
    Column("email",String,nullable = False,unique = True)
)

# one-to-many user ---> n posts
posts = Table(
    "posts",
    metadata,
    Column("id",Integer,primary_key = True),
    Column("user_id",Integer,ForeignKey("users.id",ondelete = "CASCADE"),nullable=False),
    Column("title",String,nullable = False),
    Column("content",String,nullable = False)
)

## one to one
profile = Table(
    "profiles",
    metadata,
    Column("id",Integer,primary_key = True),
    Column("user_id",Integer,ForeignKey("users.id",ondelete = "CASCADE"),nullable=False, unique = True),
    Column("bio",String,nullable = False),
    Column("address",String,nullable = False)
)


## many to many
address = Table(
    "address",
    metadata,
    Column("id",Integer,primary_key=True),
    Column("street",String(length = 50),nullable = False),
    Column("dist",String,nullable = False,unique = True),
    Column("country",String,nullable = False,unique = True)
)

user_address_association = Table(
    'user_address_association',
    metadata,
    Column("user_id",Integer,ForeignKey("users.id",ondelete = 'CASCADE'),primary_key=True),
    Column("address_id",Integer,ForeignKey("address.id",ondelete = 'CASCADE'))
)
## Create table in database
def create_tables():
    metadata.create_all(engine)

## drop table in database
def drop_tables():
    metadata.drop_all(engine)