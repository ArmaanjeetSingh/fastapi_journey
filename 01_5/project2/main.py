from models import create_tables, drop_tables
import asyncio
from db import async_session
from services import create_user, db_dependency

async def main():
    await create_tables()
    async with async_session() as db:
      await create_user('armaan', 'arm23@outlook.com', db_dependency)

if __name__ == "__main__":
    asyncio.run(main())