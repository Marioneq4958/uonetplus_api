from tests.checks.status_code import status_check
from tests.routes.login import client


def mobile_access_delete_registed_test(
    session_data, headers, register_cookies, school_id, host, symbol, ssl, id_mobile_deleted, fg
):
    response = client.post(
        "/api/v1/uonetplus-uczen/mobile-access/delete-registered-device",
        headers={"Content-Type": "application/json"},
        json={
            "session_data": session_data,
            "register_cookies": register_cookies,
            "school_id": school_id,
            "host": host,
            "symbol": symbol,
            "ssl": ssl,
            "json": {"id": id_mobile_deleted},
            "headers": headers,
        },
    )
    status_check(response.status_code, response.json(), fg)
    assert response.json()["success"] == True
