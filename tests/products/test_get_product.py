import pytest

from src.assertions.products.products_asserts import assert_product_getted, assert_get_failure
from src.api.endpoints import Endpoints
from src.data.products.get_products import (
    get_all_products_cases_params,
    get_headers,
    get_all_products_cases_headers_specs,
)


@pytest.mark.positive
def test_get_all_products_success(client, headers):
    """Test para obtener todos los productos exitosamente (smoke)."""
    resp = client.getAll(Endpoints.PRODUCTS.value, headers=headers)
    assert_product_getted(resp, 200)

@pytest.mark.parametrize("query_params, expected_status", get_all_products_cases_params())
def test_get_all_products_cases_params(client, headers, query_params, expected_status, logger):
    """Test parametrizado para GET /products con distintos query params.
    """
    enpoint = Endpoints.PRODUCTS.value
    logger.info(f"Endpoint: {enpoint} Query params: {query_params}")
    resp = client.getAll(enpoint, headers=headers, params=query_params)

    if expected_status == 200:
        assert_product_getted(resp, 200)
    else:
        assert_get_failure(resp, expected_status)

@pytest.mark.negative
@pytest.mark.ejecutar
def test_get_all_products_HTTP_incorrect(client, headers):
    """Intenta obtener todos los productos con metodo HTTP incorrecto."""
    resp = client.delete(Endpoints.PRODUCTS.value, headers=headers)
    assert_get_failure(resp, expected_status=404)

@pytest.mark.parametrize("case_id, expected_status", get_all_products_cases_headers_specs())
@pytest.mark.ejecutar
def test_get_all_products_cases_headers(client, headers, headers_factory, case_id, expected_status):
    """Test parametrizado para validar múltiples escenarios de headers en GET /products.
    """
    case_headers = get_headers(headers, headers_factory, case_id)
    resp = client.getAll(Endpoints.PRODUCTS.value, headers=case_headers)
    if expected_status == 200:
        assert_product_getted(resp, expected_status)
    else:
        assert_get_failure(resp, expected_status)
