import pytest
from src.utils.faker_config import get600Caracteres, get_name_with_special_chars, fake


def post_customers_cases_params():
    """Define casos parametrizados para POST /customers.
    """
    dup_email = "duplicate@example.com"
    return [
        pytest.param(None, None, 201, marks=pytest.mark.positive, id="valid_full"),
        pytest.param({"email": None}, None, 400, marks=pytest.mark.negative, id="missing_email"),
        pytest.param({}, None, 400, marks=pytest.mark.negative, id="empty_payload"),
        pytest.param({"email": 12345}, None, 400, marks=pytest.mark.negative, id="email_numeric"),
        pytest.param({"email": "no-at-domain"}, None, 400, marks=pytest.mark.negative, id="email_invalid_format"),
        pytest.param({"email": dup_email}, "email", 400, marks=pytest.mark.negative, id="email_already_exists"),
        pytest.param({"first_name": True}, None, 400, marks=pytest.mark.negative, id="first_name_boolean"),
        pytest.param({"first_name": get600Caracteres()}, None, 400, marks=[pytest.mark.negative, pytest.mark.xfail(reason="El sistema permite crear ususarios con un nombre mayor a 600 caracteres")], id="first_name_too_long"),
        pytest.param({"first_name": get_name_with_special_chars()}, None, 201, marks=[pytest.mark.negative, pytest.mark.xfail(reason="Al enviar caracteres especiales la respuesta no coincide con el valor enviado")], id="first_name_special_chars"),
        pytest.param({"first_name": "José María"}, None, 201, marks=pytest.mark.positive, id="first_name_spaces_accents"),
        pytest.param({"last_name": ""}, None, 201, marks=pytest.mark.positive, id="last_name_empty"),
        pytest.param({"username": ""}, None, 201, marks=pytest.mark.positive, id="username_empty"),
        pytest.param({"email": dup_email}, None, 400, marks=pytest.mark.negative, id="email_duplicate_again"),
        pytest.param({"nonexistent_field": "value"}, None, 201, marks=pytest.mark.negative, id="campo_inexistente"),
        pytest.param({"billing": {"address_1": "Only Street"}}, None, 201, marks=pytest.mark.negative, id="billing_incomplete"),
        pytest.param({"shipping": {"city": ""}}, None, 201, marks=pytest.mark.negative, id="shipping_incomplete"),
        pytest.param({"billing": {"country": "US"}, "shipping": {"country": "AR"}}, None, 201, marks=pytest.mark.negative, id="billing_shipping_inconsistent"),
        pytest.param({"billing": {"phone": "INVALID_PHONE"}}, None, 201, marks=pytest.mark.negative, id="billing_phone_invalid"),
        pytest.param({"billing": {"postcode": "!!!"}}, None, 201, marks=pytest.mark.negative, id="postcode_invalid"),
        pytest.param({"billing": {"address_1": "Calle #$%/\""}}, None, 201, marks=pytest.mark.negative, id="address_special_chars"),
    ]