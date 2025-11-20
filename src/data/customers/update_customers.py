import pytest

from src.utils.faker_config import get600Caracteres, get_name_with_special_chars, fake


def put_customers_cases_body():
    """Parametrized cases body for PUT /customers (update customer).
    """
    return [
        pytest.param(None, 200, True, marks=[pytest.mark.positive, pytest.mark.smoke], id="update_valid_full"),
        pytest.param({"email": None}, 400, False, marks=[pytest.mark.negative, pytest.mark.xfail(reason="Permite actualizar el campo obligatorio email con un valor vacio")], id="update_missing_email"),
        pytest.param({}, 200, False, marks=[pytest.mark.positive, pytest.mark.smoke], id="update_empty_payload"),
        pytest.param({"email": "correo@sin_dominio"}, 400, True, marks=[pytest.mark.negative], id="update_email_malformed"),
        pytest.param({"email": "jlopez@example.org"}, 400, True, marks=[pytest.mark.negative], id="update_email_duplicate"),
        pytest.param({"billing": {"phone": "(abc)-***"}}, 200, True, marks=[pytest.mark.negative], id="update_phone_non_numeric"),
        pytest.param({"billing": {"phone": "1"}}, 200, True, marks=[pytest.mark.negative], id="update_phone_too_short"),
        pytest.param({"billing": {"address_1": get600Caracteres()}}, 200, True, marks=[pytest.mark.negative], id="update_address1_too_long"),
        pytest.param({"billing": {"address_1": "Calle 😀🏠 #$%"}}, 200, True, marks=[pytest.mark.positive], id="update_address1_special_chars"),
        pytest.param({"first_name": ""}, 200, True, marks=[pytest.mark.positive], id="update_first_name_spaces"),
        pytest.param({"nonexistent_field": "value"}, 200, True, marks=[pytest.mark.positive], id="update_nonexistent_field"),
        pytest.param({"email": 12345}, 400, True, marks=[pytest.mark.negative], id="update_email_numeric"),
        pytest.param({"first_name": True}, 400, True, marks=[pytest.mark.negative], id="update_first_name_boolean"),
        pytest.param({"date_created": "2020-01-01T00:00:00"}, 200, True, marks=[pytest.mark.positive], id="update_readonly_date_created"),
        pytest.param({"role": "superuser"}, 200, True, marks=[pytest.mark.negative], id="update_role_invalid"),
    ]

def put_customers_headers_specs():
    """Header scenarios specifically for PUT /customers.
    """
    return [
        pytest.param("no_headers", 401, marks=pytest.mark.negative, id="no_headers"),
        pytest.param("no_content_type", 200, marks=pytest.mark.negative, id="no_content_type"),
        pytest.param("invalid_credentials", 401, marks=pytest.mark.negative, id="invalid_credentials"),
        pytest.param("expired_credentials", 401, marks=pytest.mark.negative, id="expired_credentials"),
        pytest.param("user_read", 401, marks=[pytest.mark.negative, pytest.mark.xfail(reason="Permite actualizar cleintes con un usuario con credenciales de solo lectura")], id="user_read"),
        pytest.param("user_write", 200, marks=[pytest.mark.positive, pytest.mark.smoke], id="user_write"),
        pytest.param("user_admin", 200, marks=[pytest.mark.positive, pytest.mark.smoke], id="user_admin"),
    ]

def put_customers_cases_params():
    """Devuelve una lista de pytest.param para parametrizar tests de params.
    """
    return [
        pytest.param(
            {"id": "USE_CREATED"},
            200,
            marks=[pytest.mark.positive, pytest.mark.smoke],
            id="id_producto_valido",
        ),
        pytest.param(
            {"id": 9999999},
            404,
            marks=pytest.mark.negative,
            id="id_invalido",
        ),
        pytest.param(
            {"id": "abc"},
            404,
            marks=pytest.mark.negative,
            id="id_no_numerico",
        ),
        pytest.param(
            {"id": -1},
            404,
            marks=pytest.mark.negative,
            id="id_negativo",
        ),
        pytest.param(
            {"id": ""},
            404,
            marks=pytest.mark.negative,
            id="id_con_espacios",
        ),
        pytest.param(
            {"id": None},
            404,
            marks=pytest.mark.negative,
            id="id_vacio",
        ),
        pytest.param(
            {"id": "()&$/&%"},
            404,
            marks=pytest.mark.negative,
            id="id_special_chars",
        ),
        pytest.param(
            {"id": "?force=true&force=false"},
            200,
            marks=pytest.mark.negative,
            id="query_param_force_multiple_in_id",
        ),
        pytest.param(
            {"id": "?page=abc"},
            200,
            marks=pytest.mark.negative,
            id="query_param_page_in_id",
        ),
        pytest.param(
            {"id": "?force=true"},
            200,
            marks=pytest.mark.negative,
            id="query_param_force_in_id",
        ),
        pytest.param(
            {"id": "?force=false"},
            200,
            marks=pytest.mark.negative,
            id="guery_param_force_false",
        ),
    ]