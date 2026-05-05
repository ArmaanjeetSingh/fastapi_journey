from fastapi import FastAPI
from app.db.config import create_tables
from app.task.services import *
from contextlib import asynccontextmanager
from app.task.models import TaskUpdate, TaskCreate, TaskOut, TaskPatch

@asynccontextmanager
async def lifespan(app :FastAPI):
    create_tables()
    yield

app = FastAPI(lifespan = lifespan)


@app.post("/task",response_model = TaskOut)
async def task_create(new_task : TaskCreate):
    task = await create_task(title = new_task.title,content = new_task.content)
    return task

@app.get("/task",response_model = list[TaskOut])
async def task_get_all():
    task = await get_all_tasks()
    return task

@app.get("/task/{id}",response_model = TaskOut)
async def task_get_by_id(id : int):
    task = await get_task_by_id(id)
    return task

@app.put("/task/{id}",response_model = TaskOut)
async def task_update(id:int,new_task : TaskUpdate):
    task = await update_task(id,new_task.title,new_task.content)
    return task

@app.patch("/task/{id}",response_model = TaskOut)
async def task_patch(id:int,new_task : TaskPatch):
    task = await patch_task(id,new_task.title,new_task.content)
    return task

@app.delete("/task/{id}")
async def task_delete(id : int):
    await delete_task(id)