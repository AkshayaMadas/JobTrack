# JobTrack

JobTrack is a FastAPI-based job application tracking system designed to help candidates manage job opportunities and track their application status efficiently.

## Features

- User management
- Job opportunity management
- Job application tracking
- Application status management
- Resume tracking
- SQLite database integration
- SQLAlchemy ORM
- RESTful API development with FastAPI
- Interactive API documentation with Swagger UI

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- Uvicorn
- Git & GitHub

## Database Models

The application uses SQLite with SQLAlchemy ORM.

Main database models:

- **User** – stores candidate information
- **Job** – stores job opportunity details
- **Application** – tracks applications submitted by users

## Project Structure

```text
JobTrack/
│
├── app/
│   ├── database.py
│   ├── main.py
│   └── models.py
│
├── .gitignore
├── requirements.txt
└── README.md