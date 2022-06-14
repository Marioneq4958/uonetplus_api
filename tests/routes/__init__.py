import pytest

pytest.register_assert_rewrite("tests.routes.login_incorrect")
pytest.register_assert_rewrite("tests.endpoints.conferences")
pytest.register_assert_rewrite("tests.endpoints.grades")
pytest.register_assert_rewrite("tests.routes.login")
pytest.register_assert_rewrite("tests.endpoints.mobile_access_delete_registed")
pytest.register_assert_rewrite("tests.endpoints.mobile_access_register")
pytest.register_assert_rewrite("tests.endpoints.mobile_access_registed")
pytest.register_assert_rewrite("tests.endpoints.notes")
pytest.register_assert_rewrite("tests.endpoints.school_info")
