# JobTrack

JobTrack is a FastAPI-based job application tracking system that helps candidates manage job opportunities and track their applications through RESTful APIs.

## Features

- User registration and login
- Password hashing and authentication
- Role-based access control
- Create and manage job postings
- View all available jobs
- View individual job details
- Apply for jobs with a resume
- Prevent duplicate applications
- View the current user's applications
- Application status tracking

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- Uvicorn
- Passlib / Password Hashing
- Git & GitHub

## API Endpoints

### Users
- `POST /users/register` — Register a new user
- `POST /users/login` — Login user

### Jobs
- `GET /jobs` — Get all jobs
- `POST /jobs` — Create a job
- `GET /jobs/{job_id}` — Get a specific job
- `PUT /jobs/{job_id}` — Update a job
- `DELETE /jobs/{job_id}` — Delete a job

### Applications
- `POST /applications` — Submit a job application
- `GET /applications` — Get the current user's applications

## Database

The project uses SQLite with SQLAlchemy ORM.

Main database models:

- User
- Job
- Application

## Running the Project

1. Clone the repository.
2. Create and activate a virtual environment.
3. Install dependencies:

```bash
pip install -r requirements.txt