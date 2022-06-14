from fastapi.testclient import TestClient
from tests.checks.status_code import status_check
from main import app

client = TestClient(app)


def login_test(username, password, host, ssl, fg):
    login = client.post(
        "/api/v1/auth/signin",
        headers={"Content-Type": "application/json"},
        json={
            "username": username,
            "password": password,
            "host": host,
            "ssl": ssl,
        },
    )
    assert login.json()[0]["name"] == "powiatwulkanowy"
    assert login.json()[0]["session_data"]
    session_data = login.json()[0]["session_data"]
    headers = login.json()[0]["schools"][0]["headers"]
    student = login.json()[0]["schools"][0]["students"][0]["cookies"]
    symbol = login.json()[0]["name"]
    school_id = login.json()[0]["schools"][0]["id"]
    status_check(login.status_code, login.json(), fg)
    return session_data, headers, student, symbol, school_id