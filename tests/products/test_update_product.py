import pytest
from src.data.products.update_products import put_products_cases_params, put_products_cases_payload, put_products_cases_headers
from src.assertions.products.products_asserts import assert_product_update, assert_product_failure
from src.api.endpoints import Endpoints
from src.data.products.get_products import (
    get_headers
)
from src.resources.payloads.products.payload_products import payload_product_image_scenarios


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

@pytest.mark.parametrize("case_id, expected_status", put_products_cases_headers())
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

@pytest.mark.parametrize("scenario",
    [
    pytest.param(s, marks=[pytest.mark.positive], id=s["title"]) if s.get("expected_status") == 201
    else pytest.param(s, marks=[pytest.mark.negative], id=s["title"]) for s in payload_product_image_scenarios()
    ])
def test_update_product_with_images(payload, logger, client, headers, create_product, scenario):
    """Prueba la actualizacion de productos con distintas configuraciones de imagenes.
    """
    resp_create, base_payload = create_product(update = True)
    data_payload = payload
    payload_overrides = {"images": scenario["images"]}
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
    expected = 200 if scenario.get("expected_status") == 201 else scenario.get("expected_status")
    if expected == 200:
        assert_product_update(resp_update, update_payload, status_code=200)
    else:
        assert_product_failure(resp_update, expected_status=expected)

@pytest.mark.negative
@pytest.mark.xfail(reason="No sigue la semantica REST documentada y permite usar un metodo HTTP incorrecto (POST) para actualizar productos")
def test_update_product_HTTP_incorrect(create_product, client, headers, payload, logger):
    """Intenta actualizar un producto con metodo HTTP incorrecto."""
    resp_create, used_payload = create_product(update = True)
    try:
        pid = resp_create.json().get("id")
    except Exception:
        pid = None
    assert pid is not None, "No se pudo crear el producto base para el caso de update"
    endpoint = Endpoints.PRODUCT.value.format(pid)
    logger.info(f"Endpoint de update: {endpoint} Payload de update: {payload}")
    resp = client.post(endpoint, json=payload, headers=headers)
    assert_product_failure(resp, expected_status=404)
