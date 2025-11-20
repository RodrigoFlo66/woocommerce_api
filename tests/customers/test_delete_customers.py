import pytest

from src.data.customers.create_customers import get_headers
from src.api.endpoints import Endpoints
from src.data.customers.delete_customers import delete_customers_headers, delete_customers_cases_params
from src.assertions.customers.customers_asserts import assert_customer_getted, assert_customer_failure

@pytest.mark.parametrize("case_id, expected_status", delete_customers_headers())
def test_delete_customers_cases_headers(client, headers, headers_factory, create_customer, case_id, expected_status, logger):
    """Test parametrizado para validar múltiples escenarios de headers en DELETE /customers.
    """
    case_headers = get_headers(headers, headers_factory, case_id)
    resp_create, base_payload = create_customer(update = True)
    try:
        pid = resp_create.json().get("id")
    except Exception:
        pid = None
    assert pid is not None, "No se pudo crear el cliente base"
    endpoint = f"{Endpoints.CUSTOMERS.value}/{pid}?force=true"
    logger.info(f"DELETE Endpoint: {endpoint}")
    resp = client.delete(endpoint, headers=case_headers)
    if expected_status == 200:
        assert_customer_getted(resp, 200, single_customer=True)
    else:
        assert_customer_failure(resp, expected_status=expected_status)

@pytest.mark.parametrize("params, expected_status", delete_customers_cases_params())
def test_delete_customer_params(client, headers, logger, create_customer, params, expected_status):
    """Parametrized deletion cases for customers (IDs and query params).
    """
    id_value = params.get("id")

    if isinstance(id_value, str) and "USE_CREATED" in id_value:
        resp_create, _ = create_customer(update = True)
        try:
            created = resp_create.json()
            pid = created.get("id")
        except Exception:
            pytest.skip("Could not create customer for delete test")

        id_value = id_value.replace("USE_CREATED", str(pid))

    endpoint = Endpoints.CUSTOMER.value.format(id_value)
    logger.info(f"Deleting endpoint: {endpoint}")

    resp = client.delete(endpoint, headers=headers)

    if expected_status == 200:
        assert_customer_getted(resp, 200, single_customer=True)
    else:
        assert_customer_failure(resp, expected_status=expected_status)

@pytest.mark.negative
def test_delete_customer_HTTP_incorrect(create_customer, client, headers, logger):
    """Intenta eliminar un cliente con metodo HTTP incorrecto."""
    resp_create, used_payload = create_customer(update = True)
    try:
        pid = resp_create.json().get("id")
    except Exception:
        pid = None
    assert pid is not None, "No se pudo crear el cliente base"
    endpoint = f"{Endpoints.CUSTOMERS.value}/{pid}?force=true"
    logger.info(f"Endpoint: {endpoint}")
    resp = client.getAll(endpoint, headers=headers)
    assert_customer_getted(resp, 200, single_customer=True)