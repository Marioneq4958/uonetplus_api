from tests.checks.status_code import status_check
from tests.routes.login import client


def notes_test(session_data, headers, student, school_id, host, symbol, ssl, fg):
    response = client.post(
        "/api/v1/uonetplus-uczen/notes",
        headers={"Content-Type": "application/json"},
        json={
            "session_data": session_data,
            "student": student,
            "school_id": school_id,
            "host": host,
            "symbol": symbol,
            "ssl": ssl,
            "json": {},
            "headers": headers,
        },
    )
    status_check(response.status_code, response.json(), fg)
    assert response.json()["notes"][0]["teacher"] == "Karolina Kowalska [AN]"
    assert (
        response.json()["notes"][1]["content"]
        == "+ 20p za udział w Konkursie Języka Angielskiego"
    )
