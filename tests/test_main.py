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