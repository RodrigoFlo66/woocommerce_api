import pytest

from src.api.endpoints import Endpoints
from src.data.customers.get_customers import get_all_customers_cases_params, get_customers_create_headers_specs
from src.utils.faker_config import get600Caracteres
from src.assertions.customers.customers_asserts import assert_customer_getted, assert_get_failure
from src.data.customers.create_customers import get_headers

@pytest.mark.parametrize(
    "params, expected_status, expect_empty, create_overrides",
    get_all_customers_cases_params(),
)
def test_get_all_customers_parametrized(client, headers, create_customer, logger, params, expected_status, expect_empty, create_overrides):
    """Test parametrizados validando los query params de GET.
    """
    req_params = dict(params) if isinstance(params, dict) else None

    created = None
    if create_overrides:
        resp_create, created_payload = create_customer(payload_overrides=create_overrides, update = True)
        try:
            created = resp_create.json()
        except Exception:
            created = None
        if req_params:
            for k, v in list(req_params.items()):
                if isinstance(v, str) and v == "__USE_CREATED__":
                    req_params[k] = created_payload.get("billing", {}).get("email")
                    logger.info(f"Replaced param {k} with created customer email: {req_params[k]}")
                if isinstance(v, str) and v == "LONG_600_CHARS":
                    req_params[k] = get600Caracteres()

    if req_params:
        for k, v in list(req_params.items()):
            if isinstance(v, str) and v == "LONG_600_CHARS":
                req_params[k] = get600Caracteres()

    if isinstance(req_params, dict) and "_id" in req_params:
        id_val = req_params.pop("_id")
        if id_val == "__CREATED__":
            pid = None
            try:
                pid = resp_create.json().get("id")
            except Exception:
                pid = None
            endpoint = Endpoints.CUSTOMER.value.format(pid if pid is not None else "")
            resp = client.get(endpoint, headers=headers)
        elif id_val == "__DELETED__":
            pid = None
            try:
                pid = resp_create.json().get("id")
            except Exception:
                pid = None
            if pid is not None:
                del_endpoint = f"{Endpoints.CUSTOMERS.value}/{pid}?force=true"
                client.delete(del_endpoint, headers=headers)
                endpoint = Endpoints.CUSTOMER.value.format(pid)
                resp = client.get(endpoint, headers=headers)
            else:
                resp = client.get(Endpoints.CUSTOMERS.value + "/", headers=headers)
        else:
            endpoint = Endpoints.CUSTOMER.value.format(id_val)
            resp = client.get(endpoint, headers=headers)
        if expected_status != 200:
            assert_get_failure(resp, expected_status)
            return
        logger.info(f"GET /customers endpoint: {Endpoints.CUSTOMERS.value}, params: {pid}")
        assert_customer_getted(resp, status_code=200, single_customer=True)
        return

    logger.info(f"GET /customers endpoint: {Endpoints.CUSTOMERS.value}, params: {req_params}")
    resp = client.getAll(Endpoints.CUSTOMERS.value, params=req_params, headers=headers)

    if expected_status != 200:
        assert_get_failure(resp, expected_status)
        return

    assert_customer_getted(resp, status_code=200, single_customer=False)

    if expect_empty:
        try:
            body = resp.json()
        except Exception:
            body = None
        assert isinstance(body, list) and len(body) == 0, "Expected empty list for this search"

@pytest.mark.negative
def test_get_all_customers_HTTP_incorrect(client, headers):
    """Intenta obtener todos los clientes con metodo HTTP incorrecto."""
    resp = client.delete(Endpoints.CUSTOMERS.value, headers=headers)
    assert_get_failure(resp, expected_status=404)

@pytest.mark.parametrize(
    "case_id, expected_status",
    get_customers_create_headers_specs(),
)
def test_create_customer_headers_variations(client, headers, headers_factory, case_id, expected_status):
    """Parametrized tests to validate header scenarios for getted customers.
    """
    case_headers = get_headers(headers, headers_factory, case_id)
    endpoint = Endpoints.CUSTOMERS.value
    resp = client.getAll(endpoint, headers=case_headers)

    if expected_status == 200:
        assert_customer_getted(resp, status_code=200)
    else:
        assert_get_failure(resp, expected_status)