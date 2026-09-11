# JobTrack

A full-stack Job Application Tracking System built with FastAPI, SQLAlchemy, SQLite, HTML, CSS, and JavaScript.

JobTrack provides separate workflows for candidates and recruiters, including job discovery, applications, job management, applicant tracking, and application status updates.

## Features

### Candidate Features

- User registration and login
- JWT-based authentication
- Browse available jobs
- Search jobs by job title, company, or location
- View job details
- Apply for jobs
- Prevent duplicate applications
- View submitted applications
- Track application status
- View candidate profile
- Logout

### Recruiter Features

- Recruiter authentication
- Recruiter dashboard
- Create job postings
- View and manage posted jobs
- Edit existing job postings
- Delete job postings
- View applicants for jobs
- Update application status
- Logout

### Application Tracking

Recruiters can update application statuses such as:

- Applied
- Shortlisted
- Interview
- Selected
- Rejected

Candidates can see updated application statuses from their dashboard.

## Tech Stack

### Backend

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- Uvicorn
- JWT Authentication
- Passlib / Password Hashing

### Frontend

- HTML5
- CSS3
- JavaScript

### Testing & Tools

- Pytest
- HTTPX
- Git
- GitHub
- VS Code

## Project Structure

```text
JobTrack/
│
├── app/
│   ├── config/
│   │   ├── database.py
│   │   └── security.py
│   │
│   ├── dependencies/
│   │   └── auth.py
│   │
│   ├── models/
│   │   ├── user.py
│   │   ├── job.py
│   │   └── application.py
│   │
│   ├── routes/
│   │   ├── jobs.py
│   │   ├── user.py
│   │   └── application.py
│   │
│   ├── schemas/
│   │   ├── user.py
│   │   ├── job.py
│   │   └── application.py
│   │
│   └── main.py
│
├── frontend/
│   ├── index.html
│   ├── dashboard.html
│   ├── jobs.html
│   ├── applications.html
│   ├── profile.html
│   ├── recruiter-dashboard.html
│   ├── post-job.html
│   ├── manage-jobs.html
│   ├── applicants.html
│   ├── *.js
│   └── style.css
│
├── tests/
│   └── test_main.py
│
├── requirements.txt
├── README.md
└── .gitignore