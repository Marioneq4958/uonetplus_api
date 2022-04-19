from errno import errorcode
from re import S
from fastapi.testclient import TestClient
from main import app
import pytest
import json
import requests
client = TestClient(app)
class fg:
    lightgreen = "\x1B[38;5;46m"
    orange = "\x1B[38;5;208m"
    red = "\x1B[38;5;160m"
    rs = "\033[0m"

# Ustawienia dla wszystkich testów
nick = "jan@fakelog.cf"
password = "jan123"
host = "fakelog.cf"
backuphost = "fakelog.tk"
symbol = "powiatwulkanowy"
ssl = "false"
# Ustawienia tygodni dla testów
week_grades = "16"
# Ustawienia id dla testów
id_mobile_deleted = 1234
# Ustawienia dla test_login_incorrect i test_symbol_incorrect
nick_invalid = "jan@fakelog.cf"
password_invalid = "Jan321"
symbol_invalid = "warszawa"


def status_check(status_check_code, status_check_json):
    if status_check_code == 200:
        status_check_response = print("\n" + fg.lightgreen + "OK " + str(status_check_code) + fg.rs)
    elif status_check_code == 111:
        status_check_response = print("\n" + fg.red + "Connection refused " + str(status_check_code) + fg.rs)
    elif status_check_code == 307:
        status_check_response = print("\n" + fg.orange + "Temporary redirect " + str(status_check_code) + fg.rs)
    elif status_check_code == 308:
        status_check_response = print("\n" + fg.orange + "Permanent redirect " + str(status_check_code) + fg.rs)
    elif status_check_code == 310:
        status_check_response = print("\n" + fg.red + "Too many redirects " + str(status_check_code) + fg.rs)
    elif status_check_code == 400:
        status_check_response = print("\n" + fg.red + "Bad Request " + str(status_check_code) + fg.rs)
        try:
            print(json.dumps(status_check_json, indent=4))
        except:
            print(status_check_json)
    elif status_check_code == 401:
        status_check_response = print("\n" + fg.red + "Unauthorized " + str(status_check_code) + fg.rs)
    elif status_check_code == 403:
        status_check_response = print("\n" + fg.red + "Forbidden " + str(status_check_code) + fg.rs)
    elif status_check_code == 404:
        status_check_response = print("\n" + fg.orange + "Not Found " + str(status_check_code) + fg.rs)
    elif status_check_code == 405:
        status_check_response = print("\n" + fg.orange + "Method Not Allowed " + str(status_check_code) + fg.rs)
        try:
            print(json.dumps(status_check_json, indent=4))
        except:
            print(status_check_json)
    elif status_check_code == 408:
        status_check_response = print("\n" + fg.orange + "Request Timeout " + str(status_check_code) + fg.rs)
    elif status_check_code == 422:
        status_check_response = print("\n" + fg.red + "Unprocessable Entity " + str(status_check_code) + fg.rs)
        try:
            print(json.dumps(status_check_json, indent=4))
        except:
            print(status_check_json)
    elif status_check_code == 429:
        status_check_response = print("\n" + fg.red + "Too Many Requests " + str(status_check_code) + fg.rs)
    elif status_check_code == 500:
        status_check_response = print("\n" + fg.red + "Internal Server Error " + str(status_check_code) + fg.rs)
    elif status_check_code == 502:
        status_check_response = print("\n" + fg.orange + "Bad Gateway " + str(status_check_code) + fg.rs)
    elif status_check_code == 503:
        status_check_response = print("\n" + fg.orange + "Service Unavailable " + str(status_check_code) + fg.rs)
    elif status_check_code == 504:
        status_check_response = print("\n" + fg.orange + "Gateway Timeout " + str(status_check_code) + fg.rs)
    elif status_check_code == 505:
        status_check_response = print("\n" + fg.orange + "HTTP Version Not Supported " + str(status_check_code) + fg.rs)
    elif status_check_code == 521:
        status_check_response = print("\n" + fg.red + "Web server is down " + str(status_check_code) + fg.rs)
    elif status_check_code == 522:
        status_check_response = print("\n" + fg.red + "Connection timed out " + str(status_check_code) + fg.rs)
    elif status_check_code == 525:
        status_check_response = print("\n" + fg.red + "SSL Handshake Failed " + str(status_check_code) + fg.rs)
    elif status_check_code == 526:
        status_check_response = print("\n" + fg.red + "Invalid SSL Certificate " + str(status_check_code) + fg.rs)
    try:
        return status_check_response, status_check_json
    except:
        return status_check_response


def test_check_connection():
    if ssl == "true":
        check = requests.get(
            "https://fakelog.cf",
        )
    elif ssl == "false":
        check = requests.get(
            "http://fakelog.cf",
        )
    status_check(check.status_code, check.json)
    if check.status_code == 503 or check.status_code == 521 or check.status_code == 522 or check.status_code == 525 or check.status_code == 526 or check.status_code == 429 or check.status_code == 408 or check.status_code == 500 or check.status_code == 502 or check.status_code == 504 or check.status_code == 111:
        global host
        host = backuphost
        print(fg.orange + "Main host unavailable. Changed to backup host" + fg.rs)


def test_login_correct():
    global cookies, headars, student, school_id, errorcode
    login = client.post(
        "/login",
        headers={"Content-Type": "application/json"},
        json={
            "username": nick,
            "password": password,
            "host": host,
            "symbol": symbol,
            "ssl": ssl,
        },
    )
    cookies = login.json()["vulcan_cookies"]
    headars = login.json()["students"][0]["headers"]
    student = login.json()["students"][0]["cookies"]
    school_id = login.json()["students"][0]["school_id"]
    # print(login.json())
    if login.status_code == 200:
        print("\n" + fg.lightgreen + "OK " + str(login.status_code) + fg.rs)
        assert login.json()["symbol"] == "powiatwulkanowy"
        try:
            assert login.json()["host"] == "fakelog.cf"
        except:
            assert login.json()["host"] == "fakelog.tk"
    if not cookies:
        errorcode = 1
        print("\nCookies output: ")
        print(login.json()["vulcan_cookies"])
        pytest.fail("No VULCAN cookies detected")
    elif not headars:
        errorcode = 2
        print("\nHeaders output: ")
        print(login.json()["students"][0]["headers"])
        pytest.fail("No headers detected")
    elif not student:
        errorcode = 3
        print("\nStudent output: ")
        print(login.json()["students"][0]["cookies"])
        pytest.fail("No student cookies detected")
    elif not school_id:
        errorcode = 4
        print("\nSchool ID output: ")
        print(login.json()["students"][0]["school_id"])
        pytest.fail("No school ID detected")


def test_login_incorrect():
    if errorcode == 1:
        pytest.skip("Skipped due to no cookies detected")
    elif errorcode == 2:
        pytest.skip("Skipped due to no headers detected")
    elif errorcode == 3:
        pytest.skip("Skipped due to no student cookies detected")
    elif errorcode == 4:
        pytest.skip("Skipped due to no school ID detected")
    response = client.post(
        "/login",
        headers={"Content-Type": "application/json"},
        json={
            "username": nick_invalid,
            "password": password_invalid,
            "host": host,
            "symbol": symbol,
            "ssl": ssl,
            "json": {},
            "headers": headars,
        },
    )
    status_check(response.status_code, response.json())
    assert response.json() == {'detail': 'Username or password is incorrect'}


def test_symbol_incorrect():
    if errorcode == 1:
        pytest.skip("Skipped due to no cookies detected")
    elif errorcode == 2:
        pytest.skip("Skipped due to no headers detected")
    elif errorcode == 3:
        pytest.skip("Skipped due to no student cookies detected")
    elif errorcode == 4:
        pytest.skip("Skipped due to no school ID detected")
    response = client.post(
        "/login",
        headers={"Content-Type": "application/json"},
        json={
            "username": nick,
            "password": password,
            "host": host,
            "symbol": symbol_invalid,
            "ssl": ssl,
            "json": {},
            "headers": headars,
        },
    )
    status_check(response.status_code, response.json())
    assert response.json() == {"detail": "Symbol is incorrect"}


def test_notes():
    if errorcode == 1:
        pytest.skip("Skipped due to no cookies detected")
    elif errorcode == 2:
        pytest.skip("Skipped due to no headers detected")
    elif errorcode == 3:
        pytest.skip("Skipped due to no student cookies detected")
    elif errorcode == 4:
        pytest.skip("Skipped due to no school ID detected")
    response = client.post(
        "/uonetplus-uczen/notes",
        headers={"Content-Type": "application/json"},
        json={
            "vulcan_cookies": cookies,
            "student": student,
            "school_id": school_id,
            "host": host,
            "symbol": symbol,
            "ssl": ssl,
            "json": {},
            "headers": headars,
        },
    )
    status_check(response.status_code, response.json())
    assert response.json()["notes"][0]["teacher"] == "Karolina Kowalska [AN]"
    assert (
        response.json()["notes"][3]["content"]
        == "Litwo! Ojczyzno moja! Ty jesteś jak zdrowie. Ile cię trzeba cenić, ten tylko aż kędy pieprz rośnie gdzie podział się? szukać prawodawstwa."
    )
    # print(response.json())


def test_grades():
    if errorcode == 1:
        pytest.skip("Skipped due to no cookies detected")
    elif errorcode == 2:
        pytest.skip("Skipped due to no headers detected")
    elif errorcode == 3:
        pytest.skip("Skipped due to no student cookies detected")
    elif errorcode == 4:
        pytest.skip("Skipped due to no school ID detected")
    response = client.post(
        "/uonetplus-uczen/grades",
        headers={"Content-Type": "application/json"},
        json={
            "vulcan_cookies": cookies,
            "student": student,
            "school_id": school_id,
            "host": host,
            "symbol": symbol,
            "ssl": ssl,
            "json": {"okres": week_grades},
            "headers": headars,
        },
    )
    status_check(response.status_code, response.json())
    assert response.json()["subjects"][0]["grades"][0]["teacher"] == "Karolina Kowalska"
    assert response.json()["subjects"][0]["grades"][0]["symbol"] == "Akt"
    # print(response.json())
    # assert response.json()['grades'][3]['grade'] == '4'


def test_school_info():
    if errorcode == 1:
        pytest.skip("Skipped due to no cookies detected")
    elif errorcode == 2:
        pytest.skip("Skipped due to no headers detected")
    elif errorcode == 3:
        pytest.skip("Skipped due to no student cookies detected")
    elif errorcode == 4:
        pytest.skip("Skipped due to no school ID detected")
    response = client.post(
        "/uonetplus-uczen/school-info",
        headers={"Content-Type": "application/json"},
        json={
            "vulcan_cookies": cookies,
            "student": student,
            "school_id": school_id,
            "host": host,
            "symbol": symbol,
            "ssl": ssl,
            "json": {},
            "headers": headars,
        },
    )
    status_check(response.status_code, response.json())
    assert (
        response.json()["school"]["name"]
        == "Publiczna szkoła Wulkanowego nr 1 w fakelog.cf"
    )
    assert response.json()["teachers"][0]["name"] == "Karolina Kowalska [AN]"
    # print(response.json())


def test_conference():
    if errorcode == 1:
        pytest.skip("Skipped due to no cookies detected")
    elif errorcode == 2:
        pytest.skip("Skipped due to no headers detected")
    elif errorcode == 3:
        pytest.skip("Skipped due to no student cookies detected")
    elif errorcode == 4:
        pytest.skip("Skipped due to no school ID detected")
    response = client.post(
        "/uonetplus-uczen/conferences",
        headers={"Content-Type": "application/json"},
        json={
            "vulcan_cookies": cookies,
            "student": student,
            "school_id": school_id,
            "host": host,
            "symbol": symbol,
            "ssl": ssl,
            "json": {},
            "headers": headars,
        },
    )
    status_check(response.status_code, response.json())
    assert (
        response.json()[0]["subject"]
        == "Podsumowanie I semestru - średnia klasy, oceny, frekwencja, zachowanie."
    )
    assert response.json()[1]["date"] == "06.09.2019 16:30"
    # print(response.json())


def test_mobile_access_registed():
    if errorcode == 1:
        pytest.skip("Skipped due to no cookies detected")
    elif errorcode == 2:
        pytest.skip("Skipped due to no headers detected")
    elif errorcode == 3:
        pytest.skip("Skipped due to no student cookies detected")
    elif errorcode == 4:
        pytest.skip("Skipped due to no school ID detected")
    response = client.post(
        "/uonetplus-uczen/mobile-access/get-registered-devices",
        headers={"Content-Type": "application/json"},
        json={
            "vulcan_cookies": cookies,
            "student": student,
            "school_id": school_id,
            "host": host,
            "symbol": symbol,
            "ssl": ssl,
            "json": {},
            "headers": headars,
        },
    )
    status_check(response.status_code, response.json())
    assert (
        response.json()[0]["name"]
        == "To Be Filled By O.E.M.#To Be Filled By O.E.M. (Windows 8.1)"
    )
    assert response.json()[1]["id"] == 1234
    # print(response.json())


def test_mobile_access_register():
    if errorcode == 1:
        pytest.skip("Skipped due to no cookies detected")
    elif errorcode == 2:
        pytest.skip("Skipped due to no headers detected")
    elif errorcode == 3:
        pytest.skip("Skipped due to no student cookies detected")
    elif errorcode == 4:
        pytest.skip("Skipped due to no school ID detected")
    response = client.post(
        "/uonetplus-uczen/mobile-access/register-device",
        headers={"Content-Type": "application/json"},
        json={
            "vulcan_cookies": cookies,
            "student": student,
            "school_id": school_id,
            "host": host,
            "symbol": symbol,
            "ssl": ssl,
        },
    )
    status_check(response.status_code, response.json())
    assert response.json()["pin"] == "999999"
    assert response.json()["qr_code_image"]
    # print(response.json())


def test_mobile_access_delete_registed():
    if errorcode == 1:
        pytest.skip("Skipped due to no cookies detected")
    elif errorcode == 2:
        pytest.skip("Skipped due to no headers detected")
    elif errorcode == 3:
        pytest.skip("Skipped due to no student cookies detected")
    elif errorcode == 4:
        pytest.skip("Skipped due to no school ID detected")
    response = client.post(
        "/uonetplus-uczen/mobile-access/delete-registered-device",
        headers={"Content-Type": "application/json"},
        json={
            "vulcan_cookies": cookies,
            "student": student,
            "school_id": school_id,
            "host": host,
            "symbol": symbol,
            "ssl": ssl,
            "json": {"id": id_mobile_deleted},
            "headers": headars,
        },
    )
    status_check(response.status_code, response.json())
    # Nowa metoda testowania
    # if response.status_code == 404:
    #    print(response.json())
    # else:
    #    print("Test")
    assert response.json()["success"] == True
    # print(response.json())
