import pytest

def get_all_customers_cases_params():
    """Devuelve una lista de pytest.param para parametrizar tests de params.
    """
    return [
        pytest.param(
            {"per_page": 5, "page": 2},
            200,
            False,
            None,
            marks=pytest.mark.positive,
            id="per_page_5_page_2",
        ),
        pytest.param(None, 200, False, None, marks=pytest.mark.positive, id="get_all_no_params"),
        pytest.param({"orderby": "name", "order": "asc"}, 200, False, None, marks=pytest.mark.positive, id="orderby_name_asc"),
        pytest.param({"role": "customer", "orderby": "email"}, 400, False, None, id="role_and_orderby_email"),
        pytest.param({"invalidParam": "true"}, 200, False, None, marks=pytest.mark.negative, id="invalid_param"),
        pytest.param({"per_page": 1000}, 400, False, None, marks=pytest.mark.negative, id="per_page_excessive"),
        pytest.param({"page": "abc"}, 400, False, None, marks=pytest.mark.negative, id="page_non_numeric"),
        pytest.param({"email": ""}, 400, False, None, marks=pytest.mark.negative, id="email_empty_param"),
        pytest.param({"search": "LONG_600_CHARS"}, 200, False, None, marks=pytest.mark.negative, id="search_600_chars"),
        pytest.param({"email": "__USE_CREATED__"}, 200, False, {"email": None}, id="search_by_email_existing"),
        pytest.param({"email": "no-such-email@example.com"}, 200, True, None, id="search_by_email_nonexistent"),
        pytest.param({"search": "John"}, 200, False, {"first_name": "JohnTest"}, id="search_partial_name"),
        pytest.param({"search": "José"}, 200, False, {"first_name": "José"}, id="search_name_special_chars"),
        pytest.param({"_id": "__CREATED__"}, 200, False, {"first_name": "ByIdTest"}, id="get_by_valid_id"),
        pytest.param({"_id": "abc"}, 404, False, None, marks=pytest.mark.negative, id="get_by_id_non_numeric"),
        pytest.param({"_id": 999999}, 404, False, None, marks=pytest.mark.negative, id="get_by_id_nonexistent"),
        pytest.param({"_id": -1}, 404, False, None, marks=pytest.mark.negative, id="get_by_id_negative"),
        pytest.param({"_id": "!@#"}, 404, False, None, marks=pytest.mark.negative, id="get_by_id_special_chars"),
        pytest.param({"_id": "__DELETED__"}, 404, False, {"first_name": "ToDelete"}, marks=pytest.mark.negative, id="get_deleted_customer"),
        pytest.param({"search": " John"}, 200, False, None, id="search_with_spaces"),
    ]

def get_customers_create_headers_specs():
    """Header scenarios specifically for GET /customers.
    """
    return [
        pytest.param("no_headers", 401, marks=pytest.mark.negative, id="no_headers"),
        pytest.param("no_content_type", 200, marks=pytest.mark.negative, id="no_content_type"),
        pytest.param("invalid_credentials", 401, marks=pytest.mark.negative, id="invalid_credentials"),
        pytest.param("expired_credentials", 401, marks=pytest.mark.negative, id="expired_credentials"),
        pytest.param("user_read", 200, marks=[pytest.mark.negative], id="user_read"),
        pytest.param("user_write", 401, marks=[pytest.mark.positive, pytest.mark.xfail(reason="Permite obtener cleintes con un usuario con credenciales de solo escritura")], id="user_write"),
        pytest.param("user_admin", 200, marks=pytest.mark.positive, id="user_admin"),
    ]