import pytest
from src.utils.faker_config import get600Caracteres, get_name_with_special_chars, fake
from src.utils.logger import get_logger
logger = get_logger("create_customers")

def post_customers_cases_params():
    """Define casos parametrizados para POST /customers.
    """
    dup_email = "duplicate@example.com"
    return [
        pytest.param(None, None, 201, True, marks=[pytest.mark.positive, pytest.mark.smoke], id="valid_full"),
        pytest.param({"email": None}, None, 400, True, marks=pytest.mark.negative, id="missing_email"),
        pytest.param({}, None, 400, True, marks=[pytest.mark.negative, pytest.mark.smoke], id="empty_payload"),
        pytest.param({"email": 12345}, None, 400, True, marks=pytest.mark.negative, id="email_numeric"),
        pytest.param({"email": "no-at-domain"}, None, 400, True, marks=pytest.mark.negative, id="email_invalid_format"),
        pytest.param({"email": dup_email}, "email", 400, True, marks=pytest.mark.negative, id="email_already_exists"),
        pytest.param({"first_name": True}, None, 400, True, marks=pytest.mark.negative, id="first_name_boolean"),
        pytest.param({"first_name": get600Caracteres()}, None, 400, True, marks=[pytest.mark.negative, pytest.mark.xfail(reason="El sistema permite crear ususarios con un nombre mayor a 600 caracteres")], id="first_name_too_long"),
        pytest.param({"first_name": get_name_with_special_chars()}, None, 201, True, marks=[pytest.mark.negative, pytest.mark.xfail(reason="Al enviar caracteres especiales la respuesta no coincide con el valor enviado")], id="first_name_special_chars"),
        pytest.param({"first_name": "José María"}, None, 201, True, marks=pytest.mark.positive, id="first_name_spaces_accents"),
        pytest.param({"last_name": ""}, None, 201, True, marks=pytest.mark.positive, id="last_name_empty"),
        pytest.param({"username": ""}, None, 201, True, marks=pytest.mark.positive, id="username_empty"),
        pytest.param({"email": dup_email}, None, 400, True, marks=pytest.mark.negative, id="email_duplicate_again"),
        pytest.param({"nonexistent_field": "value"}, None, 201, True, marks=pytest.mark.negative, id="campo_inexistente"),
        pytest.param({"billing": {"address_1": "Only Street"}}, None, 201, True, marks=pytest.mark.negative, id="billing_incomplete"),
        pytest.param({"shipping": {"city": ""}}, None, 201, True, marks=pytest.mark.negative, id="shipping_incomplete"),
        pytest.param({"billing": {"country": "US"}, "shipping": {"country": "AR"}}, None, 201, True, marks=pytest.mark.negative, id="billing_shipping_inconsistent"),
        pytest.param({"billing": {"phone": "INVALID_PHONE"}}, None, 201, True, marks=pytest.mark.negative, id="billing_phone_invalid"),
        pytest.param({"billing": {"postcode": "!!!"}}, None, 201, True, marks=pytest.mark.negative, id="postcode_invalid"),
        pytest.param({"billing": {"address_1": "Calle #$%/\""}}, None, 201, True, marks=pytest.mark.negative, id="address_special_chars"),
    ]


def post_customers_payload_cases_params():
    """Additional payload-focused cases requested by the user.
    """
    return [
        pytest.param({"first_name": 12345, "last_name": 67890}, None, 400, False, id="payload_incorrect_types"),
        pytest.param({"email": None, "first_name": None}, None, 400, False, id="payload_null_main_fields"),
        pytest.param({"email": "JoSe.Test@Example.COM"}, None, 201, False, id="email_mixed_case"),
        pytest.param({"billing": {}}, None, 400, False, id="billing_empty"),
        pytest.param({"shipping": {}}, None, 400, False, id="shipping_empty"),
        pytest.param({"email": None}, None, 400, False, id="only_email_provided"),
        pytest.param('{"email": "badjson@example.com",}', None, 400, False, id="malformed_json_raw"),
        pytest.param({"email": "  spaced@example.com  "}, None, 400, True, id="email_with_spaces"),
    ]

def get_headers(headers, headers_factory, case_id):
    """Test parametrizado para validar múltiples escenarios de headers en GET /products."""
    if case_id == "no_headers":
        case_headers = {}
    elif case_id == "invalid_credentials":
        case_headers = dict(headers)
        case_headers["Authorization"] = "Basic abm90X2FjdHVhbF9rZXk="
    elif case_id == "expired_credentials":
        case_headers = headers_factory(expired=True)
    elif case_id == "user_read":
        case_headers = headers_factory(role="read")
    elif case_id == "user_write":
        case_headers = headers_factory(role="write")
    elif case_id == "user_admin":
        case_headers = headers_factory()
    elif case_id == "no_content_type":
        case_headers = dict(headers)
        case_headers.pop("Content-Type", None)
    else:
        logger.warning(f"Caso desconocido recibido: {case_id}, usando headers por defecto")
        case_headers = dict(headers)

    logger.info(f"Ejecutando caso '{case_id}' con headers: {case_headers}")
    
    return case_headers


def post_customers_create_headers_specs():
    """Header scenarios specifically for POST /customers (create customer).

    Returns tuples (case_id, expected_status). Tests can use `get_headers` to build headers for each case.
    """
    return [
        pytest.param("no_headers", 401, marks=[pytest.mark.negative, pytest.mark.smoke], id="no_headers"),
        pytest.param("no_content_type", 201, marks=pytest.mark.negative, id="no_content_type"),
        pytest.param("content_type_incorrect", 201, marks=pytest.mark.negative, id="content_type_incorrect"),
        pytest.param("invalid_credentials", 401, marks=pytest.mark.negative, id="invalid_credentials"),
        pytest.param("expired_credentials", 401, marks=pytest.mark.negative, id="expired_credentials"),
        pytest.param("user_read", 401, marks=[pytest.mark.negative, pytest.mark.xfail(reason="Permite crear cleintes con un usuario con credenciales de solo lectura")], id="user_read"),
        pytest.param("user_write", 201, marks=pytest.mark.positive, id="user_write"),
        pytest.param("user_write", 201, marks=[pytest.mark.positive, pytest.mark.smoke], id="user_write"),
        pytest.param("user_admin", 201, marks=[pytest.mark.positive, pytest.mark.smoke], id="user_admin"),
    ]