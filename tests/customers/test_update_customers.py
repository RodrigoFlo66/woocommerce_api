import pytest

from src.api.endpoints import Endpoints
from src.data.customers.update_customers import put_customers_cases_params, put_customers_cases_body, put_customers_headers_specs
from src.assertions.customers.customers_asserts import assert_customer_updated, assert_customer_failure
from src.data.customers.create_customers import get_headers


@pytest.mark.parametrize("payload_overrides, expected_status, validate_request_schema", put_customers_cases_body())
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

@pytest.mark.parametrize("case_id, expected_status", put_customers_headers_specs())
def test_put_customers_cases_headers(client, payload_customer, headers, headers_factory, create_customer, case_id, expected_status, logger):
    """Test parametrizado para validar múltiples escenarios de headers en PUT /customers.
    """
    case_headers = get_headers(headers, headers_factory, case_id)
    resp_create, base_payload = create_customer(update = True)
    if isinstance(payload_customer, dict):
        payload_put = dict(payload_customer)
        payload_put.pop("username", None)
    else:
        payload_put = payload_customer
    try:
        pid = resp_create.json().get("id")
    except Exception:
        pid = None
    assert pid is not None, "No se pudo crear el cliente base para el caso de update"
    endpoint = Endpoints.CUSTOMER.value.format(pid)
    logger.info(f"Endpoint: {endpoint} Payload de update: {payload_put}")
    resp = client.put(endpoint, json=payload_put, headers=case_headers)
    if expected_status == 200:
        assert_customer_updated(resp, payload_put, status_code=200)
    else:
        assert_customer_failure(resp, expected_status=expected_status)

@pytest.mark.negative
@pytest.mark.xfail(reason="No sigue la semantica REST documentada y permite usar un metodo HTTP incorrecto (POST) para actualizar clientes")
def test_update_customer_HTTP_incorrect(client, payload_customer, headers, create_customer):
    """Intenta actualizar un cliente con metodo HTTP incorrecto."""
    resp_create, used_payload = create_customer(update = True)
    if isinstance(payload_customer, dict):
        payload_put = dict(payload_customer)
        payload_put.pop("username", None)
    else:
        payload_put = payload_customer
    try:
        pid = resp_create.json().get("id")
    except Exception:
        pid = None
    assert pid is not None, "No se pudo crear el cliente base para el caso de update"
    endpoint = Endpoints.CUSTOMER.value.format(pid)
    resp = client.post(endpoint, json=payload_put, headers=headers)
    assert_customer_failure(resp, expected_status=404)

@pytest.mark.parametrize("params, expected_status", put_customers_cases_params())
def test_put_customers_cases_params(client, payload_customer, headers, create_customer, params, expected_status, logger):
    """Test parametrizado para PUT /customers/{} con distintos params.
    """
    enpoint = Endpoints.CUSTOMERS.value
    if isinstance(payload_customer, dict):
        payload_put = dict(payload_customer)
        payload_put.pop("username", None)
    else:
        payload_put = payload_customer
    if isinstance(params, dict) and "id" in params:
        id_val = params.get("id")
        if id_val == "USE_CREATED":
            resp_create, used_payload = create_customer(update = True)
            try:
                pid = resp_create.json().get("id")
            except Exception:
                pid = None
            assert pid is not None, "Falló la creación del cliente para la prueba con path-param"
            target_endpoint = f"{enpoint}/{pid}"
        else:
            if isinstance(id_val, str) and id_val.startswith("?"):
                resp_create, used_payload = create_customer(update=True)
                try:
                    pid = resp_create.json().get("id")
                except Exception:
                    pid = None
                assert pid is not None, "Failed to create product for path-param test"
                target_endpoint = f"{enpoint}/{pid}{id_val}"
            else:
                target_endpoint = f"{enpoint}/{id_val}"

        logger.info(f"Endpoint: {target_endpoint} Payload de update: {payload_put}")
        resp = client.put(target_endpoint, json = payload_put, headers=headers)
        if expected_status == 200:
            assert_customer_updated(resp, payload_put, status_code=200)
        else:
            assert_customer_failure(resp, expected_status=expected_status)