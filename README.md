# JobTrack

JobTrack is a FastAPI-based job application tracking system designed to manage job listings and candidate applications through a RESTful API.

## Features

- User registration and login
- JWT-based authentication
- Candidate and recruiter roles
- Role-based access control (RBAC)
- Job creation, retrieval, update and deletion
- Candidate job applications
- Duplicate application prevention
- Resume information storage
- SQLite database
- SQLAlchemy ORM
- Pydantic schemas
- Swagger / OpenAPI documentation

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- JWT
- OAuth2
- Passlib / bcrypt
- Uvicorn
- Git & GitHub

## Project Structure

JobTrack/
├── app/
│   ├── config/
│   │   ├── database.py
│   │   └── security.py
│   ├── dependencies/
│   │   └── auth.py
│   ├── models/
│   │   ├── user.py
│   │   ├── job.py
│   │   └── application.py
│   ├── routes/
│   │   ├── user.py
│   │   ├── jobs.py
│   │   └── application.py
│   ├── schemas/
│   │   ├── user.py
│   │   ├── job.py
│   │   └── application.py
│   ├── services/
│   ├── utils/
│   └── main.py
├── tests/
├── .gitignore
├── requirements.txt
└── README.md

## API Endpoints

### Users

- `POST /users/register` — Register a new user
- `POST /users/login` — Login and receive JWT access token

### Jobs

- `GET /jobs/` — Get available jobs
- `GET /jobs/{job_id}` — Get a specific job
- `POST /jobs/` — Create a job (Recruiter)
- `PUT /jobs/{job_id}` — Update a job
- `DELETE /jobs/{job_id}` — Delete a job

### Applications

- `POST /applications/` — Apply for a job (Candidate)
- `GET /applications/` — View candidate applications

## Authentication

JobTrack uses JWT-based authentication with OAuth2 password flow.

Different operations are protected according to the user's role:

- **Candidate** — Can view jobs and submit applications
- **Recruiter** — Can create and manage job listings

## Running the Project

Install the dependencies:

`pip install -r requirements.txt`

Start the FastAPI server:

`uvicorn app.main:app --reload`

Open the interactive API documentation:

`http://127.0.0.1:8000/docs`

## Project Highlights

JobTrack demonstrates practical backend development concepts including:

- REST API development
- Authentication and authorization
- Role-based access control
- Database design and ORM usage
- API validation
- Modular project architecture
- CRUD operations
- Git and GitHub workflow