import pytest

from src.api.endpoints import Endpoints
from src.data.customers.update_customers import put_customers_cases_params
from src.assertions.customers.customers_asserts import assert_customer_updated, assert_customer_failure


@pytest.mark.parametrize("payload_overrides, expected_status, validate_request_schema", put_customers_cases_params())
def test_update_customer_parametrized(client, payload_customer, logger, headers, create_customer, payload_overrides, expected_status, validate_request_schema):
    """Parametrized update tests for customers.
    """
    resp_create, base_payload = create_customer(update = True)
    if isinstance(payload_customer, dict):
        payload_put = dict(payload_customer)
        payload_put.pop("username", None)
    else:
        payload_put = payload_customer
    try:
        created = resp_create.json()
        pid = created.get("id")
    except Exception:
        pytest.skip("Could not create customer for update test")

    if payload_overrides is None:
        update_payload = dict(payload_put)
    else:
        if payload_overrides == {}:
            update_payload = payload_overrides
        else:
            update_payload = dict(payload_put)
            update_payload.update(payload_overrides)

    endpoint = Endpoints.CUSTOMER.value.format(pid)
    logger.info(f"Endpoint de update: {endpoint} Payload de update: {update_payload}")
    resp = client.put(endpoint, json=update_payload, headers=headers)

    if expected_status != 200:
        assert_customer_failure(resp, expected_status=expected_status)
    else:
        if isinstance(payload_overrides, dict) and "role" in payload_overrides:
            role = payload_overrides.get("role")
            if role == "superuser":
                assert_customer_updated(resp, update_payload, validate_request_schema=validate_request_schema, equal=False)
        else:
            assert_customer_updated(resp, update_payload, validate_request_schema=validate_request_schema)  