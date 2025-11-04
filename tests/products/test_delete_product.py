import pytest
from src.api.endpoints import Endpoints
from src.assertions.products.products_asserts import assert_product_getted
from src.data.products.get_products import get_headers
from src.data.products.update_products import put_products_cases_headers
from src.assertions.products.products_asserts import assert_product_failure, assert_product_deleted
from src.data.products.delete_products import delete_products_cases_params

@pytest.mark.negative
def test_delete_product_HTTP_incorrect(create_product, client, headers, logger):
    """Intenta eliminar un producto con metodo HTTP incorrecto."""
    resp_create, used_payload = create_product(update = True)
    try:
        pid = resp_create.json().get("id")
    except Exception:
        pid = None
    assert pid is not None, "No se pudo crear el producto base para el caso de update"
    endpoint = Endpoints.PRODUCT.value.format(pid)
    logger.info(f"Endpoint: {endpoint}")
    resp = client.getAll(endpoint, headers=headers)
    assert_product_getted(resp, 200, single_product=True)

@pytest.mark.parametrize("case_id, expected_status", put_products_cases_headers())
def test_delete_products_cases_headers(client, headers, headers_factory, create_product, case_id, expected_status, logger):
    """Test parametrizado para validar múltiples escenarios de headers en DELETE /products.
    """
    case_headers = get_headers(headers, headers_factory, case_id)
    resp_create, base_payload = create_product(update = True)
    try:
        pid = resp_create.json().get("id")
    except Exception:
        pid = None
    assert pid is not None, "No se pudo crear el producto base"
    endpoint = Endpoints.PRODUCT.value.format(pid)
    logger.info(f"DELETE Endpoint: {endpoint}")
    resp = client.delete(endpoint, headers=case_headers)
    if expected_status == 200:
        assert_product_getted(resp, 200, single_product=True)
    else:
        assert_product_failure(resp, expected_status=expected_status)

@pytest.mark.parametrize("params, expected_status", delete_products_cases_params())
def test_delete_products_cases_params(client, headers, create_product, params, expected_status, logger):
    """Test parametrizado para DELETE /product/{} con distintos params.
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

        logger.info(f"DELETE Endpoint: {target_endpoint}")
        resp = client.delete(target_endpoint, headers=headers)
        if expected_status == 200:
            if id_val == "?force=true":
                assert_product_deleted(resp, 200, client=client, headers=headers, force=True)
            else:
                assert_product_deleted(resp, 200, client=client, headers=headers)
        else:
            assert_product_failure(resp, expected_status=expected_status)