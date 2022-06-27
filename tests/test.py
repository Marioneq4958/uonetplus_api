from fastapi.testclient import TestClient
from main import app
from app.core.config import settings
import requests
from tests.routes import (
    login,
    login_incorrect,
    notes,
    grades,
    school_info,
    conferences,
    mobile_access_register,
    mobile_access_delete_registed,
    mobile_access_registed,
    github,
)
from tests.checks import status_code

client = TestClient(app)


class fg:
    lightgreen = "\x1B[38;5;46m"
    orange = "\x1B[38;5;208m"
    red = "\x1B[38;5;160m"
    rs = "\033[0m"


def test_check_connection():
    check = requests.get("http://" + settings.TESTS_HOST)
    status_code.status_check(check.status_code, check.json, fg)
    if (
        check.status_code == 503
        or check.status_code == 521
        or check.status_code == 522
        or check.status_code == 525
        or check.status_code == 526
        or check.status_code == 429
        or check.status_code == 408
        or check.status_code == 500
        or check.status_code == 502
        or check.status_code == 504
        or check.status_code == 111
    ):
        global host
        host = settings.TESTS_BACKUP_HOST
        print(fg.orange + "Main host unavailable. Changed to backup host" + fg.rs)
    else:
        host = settings.TESTS_HOST


def test_login_correct():
    global session_data, headers, register_cookies, symbol, school_id
    session_data, headers, register_cookies, symbol, school_id = login.login_test(
        settings.TESTS_USERNAME, settings.TESTS_PASSWORD, host, settings.TESTS_SSL, fg
    )


def test_login_incorrect():
    login_incorrect.login_incorrect_test(
        settings.TESTS_USERNAME, settings.TESTS_INVALID_PASSWORD, host, settings.TESTS_SSL, fg
    )


def test_notes():
    notes.notes_test(session_data, headers, register_cookies, school_id, host, symbol, settings.TESTS_SSL, fg)


def test_grades():
    grades.grades_test(
        session_data, headers, register_cookies, school_id, host, symbol, settings.TESTS_SSL, settings.TESTS_SEMESTER, fg
    )


def test_school_info():
    school_info.school_info_test(
        session_data, headers, register_cookies, school_id, host, symbol, settings.TESTS_SSL, fg
    )


def test_conference():
    conferences.conference_test(
        session_data, headers, register_cookies, school_id, host, symbol, settings.TESTS_SSL, fg
    )


def test_mobile_access_registed():
    mobile_access_registed.mobile_access_registed_test(
        session_data, headers, register_cookies, school_id, host, symbol, settings.TESTS_SSL, fg
    )


def test_mobile_access_register():
    mobile_access_register.mobile_access_register_test(
        session_data, headers, register_cookies, school_id, host, symbol, settings.TESTS_SSL, fg
    )


def test_mobile_access_delete_registed():
    mobile_access_delete_registed.mobile_access_delete_registed_test(
        session_data, headers, register_cookies, school_id, host, symbol, settings.TESTS_SSL, settings.TESTS_DEVICE_ID, fg
    )


def test_github_backend_info():
    github.github_info_backend_test(fg)


def test_github_frontend_info():
    github.github_info_frontend_test(fg)

