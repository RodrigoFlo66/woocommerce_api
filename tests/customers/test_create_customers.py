import pytest

from src.assertions.customers.customers_asserts import assert_customer_created, assert_customer_failure
from src.data.customers.create_customers import post_customers_cases_params
from src.data.customers.create_customers import post_customers_payload_cases_params
from src.data.customers.create_customers import post_customers_create_headers_specs, get_headers

@pytest.mark.parametrize(
    "payload_overrides, expected_message_contains, expected_status, validate_request_schema",
    post_customers_cases_params(),
)
def test_create_customer_parametrized(create_customer, payload_overrides, expected_message_contains, expected_status, validate_request_schema):
    """Test parametrizados para validar el body de POST customers.
    """
    if payload_overrides and isinstance(payload_overrides, dict):
        email = payload_overrides.get("email")
        if email == "duplicate@example.com":
            create_customer(payload_overrides={"email": email})

    resp, used_payload = create_customer(payload_overrides=payload_overrides)

    if expected_status == 400:
        assert_customer_failure(resp, expected_status=400, expected_message_contains=expected_message_contains)
    else:
        assert_customer_created(resp, used_payload, validate_request_schema=validate_request_schema)

@pytest.mark.parametrize(
    "payload_overrides_or_raw, expected_message_contains, expected_status, validate_request_schema",
    post_customers_payload_cases_params(),
)
def test_create_customer_payload_variations(create_customer, payload_overrides_or_raw, expected_message_contains, expected_status, validate_request_schema):
    """Payload focused parametrized tests.
    """
    if isinstance(payload_overrides_or_raw, dict) and payload_overrides_or_raw == {"email": None}:
        payload_overrides_or_raw = {"email": None}  

    resp, used_payload = create_customer(payload=payload_overrides_or_raw if isinstance(payload_overrides_or_raw, (dict, str)) else None, payload_overrides=(None if isinstance(payload_overrides_or_raw, str) else payload_overrides_or_raw))

    if expected_status == 400:
        assert_customer_failure(resp, expected_status=400, expected_message_contains=expected_message_contains)
    else:
        assert_customer_created(resp, used_payload, validate_request_schema=validate_request_schema)

@pytest.mark.parametrize(
    "case_id, expected_status",
    post_customers_create_headers_specs(),
)
def test_create_customer_headers_variations(create_customer, headers, headers_factory, case_id, expected_status):
    """Parametrized tests to validate header scenarios for creating customers.
    """
    case_headers = get_headers(headers, headers_factory, case_id)
    resp, used_payload = create_customer(headers_overrides=case_headers)

    if expected_status == 201:
        assert_customer_created(resp, used_payload)
    else:
        assert_customer_failure(resp, expected_status)

@pytest.mark.negative
def test_create_product_HTTP_incorrect(create_product):
    """Intenta crear un cliente con metodo HTTP incorrecto."""
    resp, used_payload = create_product(metod = "DELETE")
    assert_customer_failure(resp, expected_status=404)