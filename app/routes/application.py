from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.config.database import get_db
from app import models
from app.schemas.application import ApplicationCreate
from app.dependencies.auth import require_role


router = APIRouter(
    prefix="/applications",
    tags=["Applications"]
)


@router.post("/")
def create_application(
    application: ApplicationCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role("candidate"))
):
    job = (
        db.query(models.Job)
        .filter(models.Job.id == application.job_id)
        .first()
    )

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )

    existing_application = (
        db.query(models.Application)
        .filter(
            models.Application.user_id == current_user["user_id"],
            models.Application.job_id == application.job_id
        )
        .first()
    )

    if existing_application:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already applied for this job"
        )

    new_application = models.Application(
        user_id=current_user["user_id"],
        job_id=application.job_id,
        status="Applied",
        resume=application.resume
    )

    db.add(new_application)
    db.commit()
    db.refresh(new_application)

    return {
        "message": "Application submitted successfully",
        "application": new_application
    }


@router.get("/")
def get_my_applications(
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role("candidate"))
):
    applications = (
        db.query(models.Application)
        .filter(
            models.Application.user_id == current_user["user_id"]
        )
        .all()
    )

    return applications