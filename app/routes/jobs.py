from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config.database import get_db
from app import models
from app.schemas.job import JobCreate, JobUpdate
from app.dependencies.auth import get_current_user, require_role


router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"]
)


@router.post("/")
def create_job(
    job: JobCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role("recruiter"))
):
    new_job = models.Job(**job.model_dump())

    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    return {
        "message": "Job added successfully",
        "job": new_job
    }


@router.get("/")
def get_jobs(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return db.query(models.Job).all()


@router.get("/{job_id}")
def get_job(
    job_id: int,
    db: Session = Depends(get_db)
):
    job = (
        db.query(models.Job)
        .filter(models.Job.id == job_id)
        .first()
    )

    if not job:
        return {"message": "Job not found"}

    return job


@router.delete("/{job_id}")
def delete_job(
    job_id: int,
    db: Session = Depends(get_db)
):
    job = (
        db.query(models.Job)
        .filter(models.Job.id == job_id)
        .first()
    )

    if not job:
        return {"message": "Job not found"}

    db.delete(job)
    db.commit()

    return {"message": "Job deleted successfully"}


@router.put("/{job_id}")
def update_job(
    job_id: int,
    job_update: JobUpdate,
    db: Session = Depends(get_db)
):
    job = (
        db.query(models.Job)
        .filter(models.Job.id == job_id)
        .first()
    )

    if not job:
        return {"message": "Job not found"}

    update_data = job_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(job, key, value)

    db.commit()
    db.refresh(job)

    return {
        "message": "Job updated successfully",
        "job": job
    }