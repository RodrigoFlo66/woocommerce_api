import pytest

from src.assertions.customers.customers_asserts import assert_customer_created, assert_customer_failure
from src.data.customers.create_customers import post_customers_cases_params


@pytest.mark.parametrize(
    "payload_overrides, expected_message_contains, expected_status",
    post_customers_cases_params(),
)
def test_create_customer_parametrized(create_customer, payload_overrides, expected_message_contains, expected_status):
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
        assert_customer_created(resp, used_payload)
