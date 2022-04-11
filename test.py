from http import cookies
from pydoc import cli
from fastapi.testclient import TestClient
import json
from main import app

client = TestClient(app)


#def test_read_item():
    #response = client.post("/login", headers={"Content-Type": "application/json"})
    #assert response.status_code == 405
    #assert response.json() == {
        #"id": "foo",
        #"title": "Foo",
        #"description": "There goes my hero",
    #}

def test_login_correct():
    response = client.post("/login",headers={"Content-Type": "application/json"},json={"username": "jan@fakelog.cf", "password": "jan123", "host": "fakelog.cf", "symbol": "powiatwulkanowy", "ssl": "false"},)
    assert response.status_code == 200
    assert response.json()["symbol"] == "powiatwulkanowy"
    assert response.json()["host"] == "fakelog.cf"

def test_login_incorrect():
    response = client.post("/login",headers={"Content-Type": "application/json"},json={"username": "cipanowie@pocz.pl", "password": "dupa123", "host": "fakelog.cf", "symbol": "powiatwulkanowy", "ssl": "false"},)
    assert response.status_code == 403
    #print(response.json())
    assert response.json() == {
        "detail": "Username or password is incorrect"
    }
    #assert response.html()["host"] == "fakelog.cf"
    #ciastka = response.json()["vulcan_cookies"]
    #print(ciastka)

def test_symbol_incorrect():
    response = client.post("/login",headers={"Content-Type": "application/json"},json={"username": "jan@fakelog.cf", "password": "jan123", "host": "fakelog.cf", "symbol": "warszawa", "ssl": "false"},)
    assert response.status_code == 403
    #print(response.json())
    assert response.json() == {
        'detail': 'Symbol is incorrect'
    }

def test_notes():
    response = client.post("/login",headers={"Content-Type": "application/json"},json={"username": "jan@fakelog.cf", "password": "jan123", "host": "fakelog.cf", "symbol": "powiatwulkanowy", "ssl": "false"},)
    cookies = response.json()["vulcan_cookies"]
    response = client.post("/uonetplus-uczen/notes",headers={"Content-Type": "application/json"},json={"vulcan_cookies": cookies, "student": {"idBiezacyDziennik": "15", "idBiezacyUczen": "1", "idBiezacyDziennikPrzedszkole": "0", "biezacyRokSzkolny": "2018"}, "school_id": "123456", "host": "fakelog.cf", "symbol": "powiatwulkanowy", "ssl": "false"},)
    assert response.status_code == 200
    #print(response.json())
    assert response.json()['notes'][0]['teacher'] == 'Karolina Kowalska [AN]'
    assert response.json()['notes'][3]['content'] == 'Litwo! Ojczyzno moja! Ty jesteś jak zdrowie. Ile cię trzeba cenić, ten tylko aż kędy pieprz rośnie gdzie podział się? szukać prawodawstwa.'

def test_grades():
    response = client.post("/login",headers={"Content-Type": "application/json"},json={"username": "jan@fakelog.cf", "password": "jan123", "host": "fakelog.cf", "symbol": "powiatwulkanowy", "ssl": "false"},)
    cookies = response.json()["vulcan_cookies"]
    response = client.post("/uonetplus-uczen/grades",headers={"Content-Type": "application/json"},json={"vulcan_cookies": cookies, "student": {"idBiezacyDziennik": "15", "idBiezacyUczen": "1", "idBiezacyDziennikPrzedszkole": "0", "biezacyRokSzkolny": "2018"}, "school_id": "123456", "host": "fakelog.cf", "symbol": "powiatwulkanowy", "ssl": "false", "json": {"okres": 16}},)
    assert response.status_code == 200
    #print(response.json())
    assert response.json()["subjects"][0]["grades"][0]["teacher"] == 'Karolina Kowalska'
    #assert response.json()['grades'][3]['grade'] == '4'
