from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

login_data = []

def test_login_correct():
    global login_data
    response = client.post(
        "/login",
        headers={"Content-Type": "application/json"},
        json={
            "username": "jan@fakelog.cf",
            "password": "jan123",
            "host": "fakelog.cf",
            "symbol": "powiatwulkanowy",
            "ssl": False
        },
    )
    assert response.status_code == 200
    assert response.json()["symbol"] == "powiatwulkanowy"
    assert response.json()["host"] == "fakelog.cf"
    login_data = response

def test_login_incorrect():
    response = client.post(
        "/login",
        headers={"Content-Type": "application/json"},
        json={
            "username": "maria@fakelog.cf",
            "password": "maria123",
            "host": "fakelog.cf",
            "symbol": "powiatwulkanowy",
            "ssl": False
        },
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Username or password is incorrect"

def test_symbol_incorrect():
    response = client.post(
        "/login",
        headers={"Content-Type": "application/json"},
        json={
            "username": "jan@fakelog.cf",
            "password": "jan123",
            "host": "fakelog.cf",
            "symbol": "warszawa",
            "ssl": False
        },
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Symbol is incorrect"

def test_notes():
    response = client.post(
        "/uonetplus-uczen/notes",
        headers={"Content-Type": "application/json"},
        json={
            "host": login_data.json()["host"],
            "symbol": login_data.json()["symbol"],
            "school_id": login_data.json()["students"][0]["school_id"],
            "ssl": login_data.json()["ssl"],
            "headers": login_data.json()["students"][0]["headers"],
            "student": login_data.json()["students"][0]["cookies"],
            "vulcan_cookies": login_data.json()["vulcan_cookies"],
            "payload": {},
        },
    )
    assert response.status_code == 200
    assert response.json()['notes'][0]['teacher'] == 'Karolina Kowalska [AN]'
    assert response.json()['notes'][3]['content'] == 'Litwo! Ojczyzno moja! Ty jesteś jak zdrowie. Ile cię trzeba cenić, ten tylko aż kędy pieprz rośnie gdzie podział się? szukać prawodawstwa.'

def test_grades():
    response = client.post(
        "/uonetplus-uczen/grades",
        headers={"Content-Type": "application/json"},
        json={
            "host": login_data.json()["host"],
            "symbol": login_data.json()["symbol"],
            "school_id": login_data.json()["students"][0]["school_id"],
            "ssl": login_data.json()["ssl"],
            "headers": login_data.json()["students"][0]["headers"],
            "student": login_data.json()["students"][0]["cookies"],
            "vulcan_cookies": login_data.json()["vulcan_cookies"],
            "payload": {"okres": 16},
        },
    )
    assert response.status_code == 200
    assert response.json()["subjects"][0]["grades"][0]["teacher"] == 'Karolina Kowalska'
    assert response.json()["subjects"][0]["grades"][0]["symbol"] == 'Akt'

def test_school_info():
    response = client.post(
        "/uonetplus-uczen/school-info",
        headers={"Content-Type": "application/json"},
        json={
            "host": login_data.json()["host"],
            "symbol": login_data.json()["symbol"],
            "school_id": login_data.json()["students"][0]["school_id"],
            "ssl": login_data.json()["ssl"],
            "headers": login_data.json()["students"][0]["headers"],
            "student": login_data.json()["students"][0]["cookies"],
            "vulcan_cookies": login_data.json()["vulcan_cookies"],
            "payload": {},
        },
    )
    assert response.status_code == 200
    assert response.json()["school"]["name"] == "Publiczna szkoła Wulkanowego nr 1 w fakelog.cf"
    assert response.json()["teachers"][0]["name"] == "Karolina Kowalska [AN]"
    print(response.json())

def test_conferences():
    response = client.post(
        "/uonetplus-uczen/conferences",
        headers={"Content-Type": "application/json"},
        json={
            "host": login_data.json()["host"],
            "symbol": login_data.json()["symbol"],
            "school_id": login_data.json()["students"][0]["school_id"],
            "ssl": login_data.json()["ssl"],
            "headers": login_data.json()["students"][0]["headers"],
            "student": login_data.json()["students"][0]["cookies"],
            "vulcan_cookies": login_data.json()["vulcan_cookies"],
            "payload": {},
        },
    )
    assert response.status_code == 200
    assert response.json()[1]["title"] == "ZSW"

def test_mobile_access_registed():
    response = client.post(
        "/uonetplus-uczen/mobile-access/get-registered-devices",
        headers={"Content-Type": "application/json"},
        json={
            "host": login_data.json()["host"],
            "symbol": login_data.json()["symbol"],
            "school_id": login_data.json()["students"][0]["school_id"],
            "ssl": login_data.json()["ssl"],
            "headers": login_data.json()["students"][0]["headers"],
            "student": login_data.json()["students"][0]["cookies"],
            "vulcan_cookies": login_data.json()["vulcan_cookies"],
            "payload": {},
        },
    )
    assert response.status_code == 200
    assert response.json()[0]["name"] == "To Be Filled By O.E.M.#To Be Filled By O.E.M. (Windows 8.1)"
    assert response.json()[1]["id"] == 1234

def test_mobile_access_register():
    response = client.post(
        "/uonetplus-uczen/mobile-access/register-device",
        headers={"Content-Type": "application/json"},
        json={
            "host": login_data.json()["host"],
            "symbol": login_data.json()["symbol"],
            "school_id": login_data.json()["students"][0]["school_id"],
            "ssl": login_data.json()["ssl"],
            "headers": login_data.json()["students"][0]["headers"],
            "student": login_data.json()["students"][0]["cookies"],
            "vulcan_cookies": login_data.json()["vulcan_cookies"],
            "payload": {},
        },
    )
    assert response.status_code == 200
    assert response.json()["token"] == "FK100000"
    assert response.json()["pin"] == "999999"

def test_mobile_access_delete_registed():
    response = client.post(
        "/uonetplus-uczen/mobile-access/delete-registered-device",
        headers={"Content-Type": "application/json"},
        json={
            "host": login_data.json()["host"],
            "symbol": login_data.json()["symbol"],
            "school_id": login_data.json()["students"][0]["school_id"],
            "ssl": login_data.json()["ssl"],
            "headers": login_data.json()["students"][0]["headers"],
            "student": login_data.json()["students"][0]["cookies"],
            "vulcan_cookies": login_data.json()["vulcan_cookies"],
            "payload": {"id": 1234},
        },
    )
    assert response.status_code == 200
    assert response.json()["success"] == True
