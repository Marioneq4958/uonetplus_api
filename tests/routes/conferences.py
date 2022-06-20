from tests.checks.status_code import status_check
from tests.routes.login import client


def conference_test(session_data, headers, register_cookies, school_id, host, symbol, ssl, fg):
    response = client.post(
        "/api/v1/uonetplus-uczen/conferences",
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
    status_check(response.status_code, response.json(), fg)
    assert (
        response.json()[0]["subject"]
        == "Podsumowanie I semestru - średnia klasy, oceny, frekwencja, zachowanie."
    )
    assert response.json()[1]["date"] == "06.09.2019 16:30"
