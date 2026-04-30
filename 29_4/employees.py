# Fields: title, company, salary, location, experience_required
from fastapi import FastAPI, Query, Path
from pydantic import BaseModel, Field
from typing import Annotated, Literal, Optional

class Job(BaseModel):
    title : Annotated[str,Field(max_length = 15)]
    company : Annotated[Literal["armaco","cmax"],Field(max_length = 8)]
    salary : Annotated[float,Field(gt = 10000)]
    location: Annotated[str,Field(min_length = 3)]
    experience_required : Annotated[int,Field(ge = 1)]


class JobUpdate(BaseModel):
    title : Optional[Annotated[str|None,Field(max_length = 15)]] = None
    company : Optional[Annotated[Literal["armaco","cmax"]|None,Field(max_length = 4)]] = None
    salary : Optional[Annotated[float|None,Field(gt = 10000)]] = None
    location: Optional[Annotated[str|None,Field(min_length = 3)]] = None
    experience_required : Optional[Annotated[int|None,Field(ge = 1)]] = None

jobs = [
    {"id":1,"title":"software engineer","company":"armaco","salary":20000,"location":"bengalore","experience_required":2},
    {"id":2,"title":"junior developer","company":"cmax","salary":15000,"location":"mumbai","experience_required":5},
    {"id":3,"title":"data analyst","company":"cmax","salary":18000,"location":"mumbai","experience_required":4},
    {"id":4,"title":"software engineer","company":"armaco","salary":30000,"location":"benglore","experience_required":7},
    {"id":5,"title":"data analyst","company":"armaco","salary":28000,"location":"mumbai","experience_required":3},
]
app = FastAPI()

@app.get("/jobs")
async def get_jobs(title : Optional [Annotated[str,Query(max_length = 15)]] = None,location: Optional[Annotated[str|None,Query(min_length = 3)]] = None, min_salary: Optional[Annotated[float|None,Field(gt = 10000)]] = None):
    filtered_jobs = []
    for job in jobs:
        if title is not None and title.casefold() not in job.get("title").casefold():
            continue
        if location is not None and location != job.get("location"):
            continue
        if min_salary is not None and min_salary > job.get("salary"):
            continue
        filtered_jobs.append(job)
    return filtered_jobs

@app.get("/jobs/{job_id}")
async def get_jobs_by_id(job_id : Annotated[int,Path(gt = 0)]):
    for job in jobs:
        if job.get("id") == job_id:
            return job
    return {"status":"job id not found"}


@app.post("/jobs")
async def create_job(job : Job):
    create_job_model = job.model_dump()
    create_job_model.update({"id":len(jobs)+1})
    jobs.append(create_job_model)
    return {"status":"job created successfully"}


@app.put("/jobs/{job_id}")
async def update_job(update_job : Job, job_id : Annotated[int,Path(gt = 0)]):
    for job in jobs:
        if job_id == job.get("id"):
            job.update(update_job.dict(exclude_unset = True))
            return {"status":"job updated successfully"}
    return {"status":"job id not found"}


@app.delete("/jobs/{job_id}")
async def delete_job(job_id : Annotated[int,Path(gt = 0)]):
    for index,job in enumerate(jobs):
        if job_id == job.get("id"):
            jobs.pop(index)
            return {"status":"job deleted successfully"}
    return {"status":"job id not found"}