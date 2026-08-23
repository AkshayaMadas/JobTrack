from fastapi import FastAPI, Depends,HTTPException, status
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from .database import engine, Base, get_db
from . import models
from jose import jwt
from datetime import datetime, timedelta, timezone


app = FastAPI()
Base.metadata.create_all(bind=engine)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "jobtrack-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("sub")
        role = payload.get("role")

        if user_id is None or role is None:
            raise credentials_exception

        return {
            "user_id": int(user_id),
            "role": role
        }

    except Exception:
        raise credentials_exception
def require_role(required_role: str):
    def role_checker(current_user: dict = Depends(get_current_user)):
        if current_user["role"] != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource"
            )

        return current_user

    return role_checker
   
    
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

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
class Job(BaseModel):
    id: int
    company: str
    position: str
    location: str
    status: str
    notes: str | None = None
class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    role: str
class UserLogin(BaseModel):
    username: str
    password: str
class ApplicationCreate(BaseModel):
    job_id: int
    resume: str | None = None
class Job(JobCreate):
    id: int


@app.post("/users/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(user.password)

    new_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        role=user.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User registered successfully",
        "user": {
            "id": new_user.id,
            "username": new_user.username,
            "email": new_user.email,
            "role": new_user.role
        }
    }
@app.post("/users/login")
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    db_user = (
        db.query(models.User)
        .filter(models.User.username == form_data.username)
        .first()
    )

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={
            "sub": str(db_user.id),
            "role": db_user.role
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@app.post("/applications")
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

@app.get("/applications")
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


@app.get("/")
def home():
    return {"message": "Welcome to JobTrack API"}


jobs = []

@app.post("/jobs")
def create_job(job: JobCreate,
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

@app.get("/jobs")
def get_jobs(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
    ):
    return db.query(models.Job).all()
@app.get("/jobs/{job_id}")
def get_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(models.Job).filter(models.Job.id == job_id).first()

    if not job:
        return {"message": "Job not found"}

    return job

@app.delete("/jobs/{job_id}")
def delete_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(models.Job).filter(models.Job.id == job_id).first()

    if not job:
        return {"message": "Job not found"}

    db.delete(job)
    db.commit()

    return {"message": "Job deleted successfully"}
@app.put("/jobs/{job_id}")
def update_job(
    job_id: int,
    job_update: JobUpdate,
    db: Session = Depends(get_db)
):
    job = db.query(models.Job).filter(models.Job.id == job_id).first()

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