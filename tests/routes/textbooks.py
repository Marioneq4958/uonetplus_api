from tests.checks.status_code import status_check
from tests.routes.login import client


def textbooks_school_years_test(session_data, headers, register_cookies, school_id, host, symbol, ssl, fg):
    response = client.post(
        "/api/v1/uonetplus-uczen/textbooks/get-textbooks-school-years",
        headers={"Content-Type": "application/json"},
        json={
            "session_data": session_data,
            "register_cookies": register_cookies,
            "school_id": school_id,
            "host": host,
            "symbol": symbol,
            "ssl": ssl,
            "json": {},
            "headers": headers,
        },
    )
    assert response.json()[0]["id"] == 2021
    assert response.json()[3]["name"] == "2018/2019"
    status_check(response.status_code, response.json(), fg)


def student_textbooks_test(session_data, headers, register_cookies, school_id, host, symbol, ssl, fg):
    response = client.post(
        "/api/v1/uonetplus-uczen/textbooks/get-student-textbooks",
        headers={"Content-Type": "application/json"},
        json={
            "session_data": session_data,
            "register_cookies": register_cookies,
            "school_id": school_id,
            "host": host,
            "symbol": symbol,
            "ssl": ssl,
            "json": {},
            "headers": headers,
        },
    )
    assert response.json()["textbooks"][0]["id"] == 66
    assert response.json()["textbooks"][2]["description"] == ""
    status_check(response.status_code, response.json(), fg)
