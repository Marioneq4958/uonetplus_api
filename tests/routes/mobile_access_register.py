from tests.checks.status_code import status_check
from tests.routes.login import client


def mobile_access_register_test(
    session_data, headers, student, school_id, host, symbol, ssl, fg
):
    response = client.post(
        "/api/v1/uonetplus-uczen/mobile-access/register-device",
        headers={"Content-Type": "application/json"},
        json={
            "session_data": session_data,
            "student": student,
            "school_id": school_id,
            "host": host,
            "symbol": symbol,
            "ssl": ssl,
        },
    )
    status_check(response.status_code, response.json(), fg)
    assert response.json()["pin"] == "999999"
    assert response.json()["qr_code_image"]
