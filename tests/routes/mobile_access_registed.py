from tests.checks.status_code import status_check
from tests.routes.login import client


def mobile_access_registed_test(
    session_data, headers, register_cookies, school_id, host, symbol, ssl, fg
):
    response = client.post(
        "/api/v1/uonetplus-uczen/mobile-access/get-registered-devices",
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
            response.json()[0]["name"]
            == "Szkolny.eu - nie usuwać"
    )
    assert response.json()[1]["id"] == -2137
