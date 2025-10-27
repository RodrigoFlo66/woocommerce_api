import pytest

from src.assertions.products.products_asserts import assert_product_getted, assert_get_failure
from src.api.endpoints import Endpoints
from src.resources.params.products.params_products import get_all_products_cases


@pytest.mark.positive
def test_get_all_products_success(client, headers):
    """Test para obtener todos los productos exitosamente (smoke)."""
    resp = client.getAll(Endpoints.PRODUCTS.value, headers=headers)
    assert_product_getted(resp, 200)


@pytest.mark.parametrize("query_params, expected_status", get_all_products_cases())
def test_get_all_products_parametrized(client, headers, query_params, expected_status, logger):
    """Test parametrizado para GET /products con distintos query params.
    """
    enpoint = Endpoints.PRODUCTS.value
    logger.info(f"Endpoint: {enpoint} Query params: {query_params}")
    resp = client.getAll(enpoint, headers=headers, params=query_params)

    if expected_status == 200:
        assert_product_getted(resp, 200)
    else:
        assert_get_failure(resp, expected_status)
