import pytest
from src.data.products.update_products import put_products_cases_params, put_products_cases_payload
from src.assertions.products.products_asserts import assert_product_update, assert_product_failure
from src.api.endpoints import Endpoints
from src.data.products.get_products import (
    get_headers,
    get_all_products_cases_headers_specs,
)


@pytest.mark.parametrize(
    "payload_overrides, expected_generated_name, expected_status",
    put_products_cases_payload(),
)
def test_update_product_payload_parametrized(client, headers, payload, create_product, payload_overrides, expected_generated_name,logger, expected_status):
    """Test parametrizado para UPDATE /products/{id}.
    """
    resp_create, base_payload = create_product(update = True)
    data_payload = payload
    try:
        pid = resp_create.json().get("id")
    except Exception:
        pid = None
    assert pid is not None, "No se pudo crear el producto base para el caso de update"

    if payload_overrides is None:
        update_payload = dict(data_payload) if isinstance(data_payload, dict) else {}
    else:
        update_payload = dict(data_payload) if isinstance(data_payload, dict) else {}
        if payload_overrides == {}:
            update_payload = payload_overrides
        else:
            update_payload.update(payload_overrides)

    endpoint = Endpoints.PRODUCT.value.format(pid)
    logger.info(f"Endpoint de update: {endpoint} Payload de update: {update_payload}")
    resp_update = client.put(endpoint, json=update_payload, headers=headers)

    if expected_status == 400:
        logger.info(f"respuesta de update: {resp_update.json()}")
        assert_product_failure(resp_update, expected_status=400)
    else:
        rp = update_payload.get("regular_price") if isinstance(update_payload, dict) else None
        if rp == "rt12.3xr":
            assert_product_update(resp_update, update_payload, status_code=200, equal=False)
        else:
            assert_product_update(resp_update, update_payload, status_code=200)

@pytest.mark.parametrize("params, expected_status", put_products_cases_params())
def test_put_products_cases_params(client, payload, headers, create_product, params, expected_status, logger):
    """Test parametrizado para PUT /product/{} con distintos params.
    """
    enpoint = Endpoints.PRODUCTS.value

    if isinstance(params, dict) and "id" in params:
        id_val = params.get("id")
        if id_val == "USE_CREATED_PRODUCT":
            resp_create, used_payload = create_product(update = True)
            try:
                pid = resp_create.json().get("id")
            except Exception:
                pid = None
            assert pid is not None, "Failed to create product for path-param test"
            target_endpoint = f"{enpoint}/{pid}"
        else:
            if isinstance(id_val, str) and id_val.startswith("?"):
                resp_create, used_payload = create_product(update=True)
                try:
                    pid = resp_create.json().get("id")
                except Exception:
                    pid = None
                assert pid is not None, "Failed to create product for path-param test"
                target_endpoint = f"{enpoint}/{pid}{id_val}"
            else:
                target_endpoint = f"{enpoint}/{id_val}"

        logger.info(f"Endpoint de update: {target_endpoint} Payload de update: {payload}")
        resp = client.put(target_endpoint, json = payload, headers=headers)
        if expected_status == 200:
            assert_product_update(resp, payload, status_code=200)
        else:
            assert_product_failure(resp, expected_status=expected_status)

@pytest.mark.parametrize("case_id, expected_status", get_all_products_cases_headers_specs())
def test_put_products_cases_headers(client, payload, headers, headers_factory, create_product, case_id, expected_status, logger):
    """Test parametrizado para validar múltiples escenarios de headers en PUT /products.
    """
    case_headers = get_headers(headers, headers_factory, case_id)
    resp_create, base_payload = create_product(update = True)
    try:
        pid = resp_create.json().get("id")
    except Exception:
        pid = None
    assert pid is not None, "No se pudo crear el producto base para el caso de update"
    endpoint = Endpoints.PRODUCT.value.format(pid)
    logger.info(f"Endpoint de update: {endpoint} Payload de update: {payload}")
    resp = client.put(endpoint, json=payload, headers=case_headers)
    if expected_status == 200:
        assert_product_update(resp, payload, status_code=200)
    else:
        assert_product_failure(resp, expected_status=expected_status)