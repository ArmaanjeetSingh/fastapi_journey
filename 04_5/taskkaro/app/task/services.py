from sqlmodel import select, Session
from app.task.models import  Task
from app.db.config import engine
from fastapi import HTTPException

async def create_task(title : str,content : str):
    with Session(engine) as session:
        task = Task(title = title, content = content)
        session.add(task)
        session.commit()
        session.refresh(task)
        return task


async def get_all_tasks():
    with Session(engine) as session:
        stmt = select(Task)
        result = session.scalars(stmt)
        return result.all()


async def get_task_by_id(id:int):
    with Session(engine) as session:
        task= session.get(Task,id)
        if not task:
            raise HTTPException(status = 404, detail = 'task not found')
        return task


async def update_task(id:int, title : str, content : str):
    with Session(engine) as session:
        task= session.get(Task,id)
        if not task:
            raise HTTPException(status = 404, detail = 'task not found')
        task.title = title
        task.content = content
        session.add(task)
        session.commit()
        session.refresh(task)
        return task

async def patch_task(id:int, title : str|None = None, content : str|None = None):
    with Session(engine) as session:
        task= session.get(Task,id)
        if not task:
            raise HTTPException(status = 404, detail = 'task not found')
        if  title is not None:
            task.title = title
        if content is not None:
            task.content = content
        session.add(task)
        session.commit()
        session.refresh(task)
        return task

async def delete_task(id:int):
    with Session(engine) as session:
        task= session.get(Task,id)
        if not task:
            raise HTTPException(status = 404, detail = 'task not found')
        session.delete(task)
        session.commit()
        return {"message":"task deleted"}