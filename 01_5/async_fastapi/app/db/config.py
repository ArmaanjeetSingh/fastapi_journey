from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

db_path = os.path.join(BASE_DIR,'sqlitedb.db')

DATABASE_URL = f"sqlite+aiosqlite:///{BASE_DIR}"

engine = create_async_engine(DATABASE_URL)

async_session = async_sessionmaker(bind = engine, expire_on_commit = True)