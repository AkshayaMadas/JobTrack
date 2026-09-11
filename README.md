# JobTrack

A full-stack Job Application Tracking System built with **FastAPI, SQLAlchemy, SQLite, HTML, CSS, and JavaScript**.

JobTrack provides separate workflows for **candidates and recruiters**, allowing candidates to discover and apply for jobs while recruiters can manage job postings and track applications.

---

## 🚀 Key Features

### 👩‍💻 Candidate Portal

- User registration and login
- JWT-based authentication
- Browse available jobs
- Search jobs by job title, company, or location
- View job information
- Apply for jobs
- Duplicate application prevention
- View submitted applications
- Track application status
- Candidate profile
- Logout

### 🧑‍💼 Recruiter Portal

- Recruiter authentication
- Recruiter dashboard
- Create and publish job postings
- View and manage job postings
- Edit existing jobs
- Delete job postings
- View applicants for jobs
- Update application status
- Logout

### 📊 Application Tracking

Recruiters can update application statuses:

- Applied
- Shortlisted
- Interview
- Selected
- Rejected

Candidates can view the latest application status from their **My Applications** page.

---

## 🔐 Authentication & Authorization

JobTrack uses **JWT-based authentication** with role-based access control.

### Candidate

Candidates can:

- Browse jobs
- Apply for jobs
- View their applications
- View their profile

### Recruiter

Recruiters can:

- Create jobs
- Manage jobs
- View applicants
- Update application statuses

Protected API endpoints require a valid authentication token.

---

## 🛠️ Tech Stack

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
- Fetch API
- Browser Local Storage

### Testing & Development

- Pytest
- HTTPX
- Git
- GitHub
- VS Code

---

## 🏗️ Project Architecture

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