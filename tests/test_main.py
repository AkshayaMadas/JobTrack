from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_get_jobs():
    response = client.get("/jobs/")
    assert response.status_code == 401
def test_get_jobs_authenticated():
    login_response = client.post(
        "/users/login",
        data={
            "username": "akshaya",
            "password": "Test@12345"
        }
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    response = client.get(
        "/jobs/",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200
def test_candidate_cannot_create_job():
    login_response = client.post(
        "/users/login",
        data={
            "username": "akshaya",
            "password": "Test@12345"
        }
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    response = client.post(
        "/jobs/",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "company": "Test Company",
            "position": "Python Developer",
            "location": "Hyderabad",
            "status": "Open",
            "notes": "Testing RBAC"
        }
    )

    assert response.status_code == 403
def test_recruiter_can_create_job():
    login_response = client.post(
        "/users/login",
        data={
            "username": "recruiter2",
            "password": "Recruiter@123"
        }
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    response = client.post(
        "/jobs/",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "company": "Test Recruiter Company",
            "position": "Python Developer",
            "location": "Hyderabad",
            "status": "Open",
            "notes": "Testing recruiter access"
        }
    )

    assert response.status_code == 200
def test_apply_for_nonexistent_job():
    login_response = client.post(
        "/users/login",
        data={
            "username": "akshaya",
            "password": "Test@12345"
        }
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    response = client.post(
        "/applications/",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "job_id": 99999,
            "resume": "resume.pdf"
        }
    )

    assert response.status_code == 404
def test_candidate_can_apply_for_job():
    recruiter_login = client.post(
        "/users/login",
        data={
            "username": "recruiter2",
            "password": "Recruiter@123"
        }
    )

    assert recruiter_login.status_code == 200

    recruiter_token = recruiter_login.json()["access_token"]

    job_response = client.post(
        "/jobs/",
        headers={
            "Authorization": f"Bearer {recruiter_token}"
        },
        json={
            "company": "Application Test Company",
            "position": "Python Developer",
            "location": "Hyderabad",
            "status": "Open",
            "notes": "Test application"
        }
    )

    assert job_response.status_code == 200

    job_id = job_response.json()["job"]["id"]

    candidate_login = client.post(
        "/users/login",
        data={
            "username": "akshaya",
            "password": "Test@12345"
        }
    )

    assert candidate_login.status_code == 200

    candidate_token = candidate_login.json()["access_token"]

    response = client.post(
        "/applications/",
        headers={
            "Authorization": f"Bearer {candidate_token}"
        },
        json={
            "job_id": job_id,
            "resume": "resume.pdf"
        }
    )

    assert response.status_code == 200
def test_candidate_cannot_apply_twice():
    recruiter_login = client.post(
        "/users/login",
        data={
            "username": "recruiter2",
            "password": "Recruiter@123"
        }
    )

    assert recruiter_login.status_code == 200

    recruiter_token = recruiter_login.json()["access_token"]

    job_response = client.post(
        "/jobs/",
        headers={
            "Authorization": f"Bearer {recruiter_token}"
        },
        json={
            "company": "Duplicate Test Company",
            "position": "Python Developer",
            "location": "Hyderabad",
            "status": "Open",
            "notes": "Testing duplicate applications"
        }
    )

    assert job_response.status_code == 200

    job_id = job_response.json()["job"]["id"]

    candidate_login = client.post(
        "/users/login",
        data={
            "username": "akshaya",
            "password": "Test@12345"
        }
    )

    assert candidate_login.status_code == 200

    candidate_token = candidate_login.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {candidate_token}"
    }

    first_application = client.post(
        "/applications/",
        headers=headers,
        json={
            "job_id": job_id,
            "resume": "resume.pdf"
        }
    )

    assert first_application.status_code == 200

    second_application = client.post(
        "/applications/",
        headers=headers,
        json={
            "job_id": job_id,
            "resume": "resume.pdf"
        }
    )

    assert second_application.status_code == 400