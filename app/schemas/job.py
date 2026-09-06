from pydantic import BaseModel


class JobCreate(BaseModel):
    company: str
    position: str
    location: str
    status: str
    notes: str | None = None


class JobUpdate(BaseModel):
    company: str | None = None
    position: str | None = None
    location: str | None = None
    status: str | None = None
    notes: str | None = None


class Job(JobCreate):
    id: int