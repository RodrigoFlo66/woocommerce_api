import pytest

from src.utils.faker_config import get600Caracteres, get_name_with_special_chars, fake


def put_customers_cases_params():
    """Parametrized cases body for PUT /customers (update customer).
    """
    return [
        pytest.param(None, 200, True, marks=[pytest.mark.positive], id="update_valid_full"),
        pytest.param({"email": None}, 400, False, marks=[pytest.mark.negative, pytest.mark.xfail(reason="Permite actualizar el campo obligatorio email con un valor vacio")], id="update_missing_email"),
        pytest.param({}, 200, False, marks=[pytest.mark.positive], id="update_empty_payload"),
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