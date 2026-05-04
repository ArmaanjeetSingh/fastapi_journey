from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

db_path = os.path.join(BASE_DIR,"test.db")

DATABASE_URL = f"sqlite+aiosqlite:///{db_path}"
engine = create_async_engine(DATABASE_URL)

async_session = async_sessionmaker(expire_on_commit = True, bind = engine)

async def get_db():
    async with async_session()as session:
        yield session
        