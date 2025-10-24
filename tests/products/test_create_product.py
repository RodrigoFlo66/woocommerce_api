import pytest

from src.assertions.products.products_asserts import assert_product_created
from src.assertions.products.products_asserts import assert_product_failure


@pytest.mark.parametrize(
    "payload_overrides, expected_generated_name, expected_status",
    [
        pytest.param(None, None, 201, marks=pytest.mark.smoke, id="valid_full"),
        pytest.param({"name": None}, "Producto", 201, marks=pytest.mark.negative, id="no_name"),
        pytest.param({}, "Producto", 201, marks=pytest.mark.negative, id="empty_payload_expected_Producto"),
        pytest.param({"name": True}, None, 400, marks=pytest.mark.negative , id="name_boolean"),
        pytest.param({"regular_price": 19.9}, None, 400, marks=pytest.mark.negative, id="regular_price_double"),
    ],
)
def test_create_product_parametrized(create_product, payload_overrides, expected_generated_name, expected_status):
    """Test parametrizados.
    """
    resp, used_payload = create_product(payload_overrides=payload_overrides)

    if expected_status == 400:
        assert_product_failure(resp, expected_status=400)
    else:
    	assert_product_created(resp, used_payload)

@pytest.mark.negative
def test_create_product_HTTP_incorrect(create_product):
    """Intenta crear un producto con metodo HTTP incorrecto."""
    resp, used_payload = create_product(metod = "DELETE")
    assert_product_failure(resp, expected_status=404)

@pytest.mark.negative
def test_create_product_without_headers(create_product):
    """Intenta crear un producto sin headers de autenticación."""
    resp, _ = create_product(headers_overrides={})
    assert_product_failure(resp, expected_status=(401), expected_message_contains="Lo siento, no tienes permiso para crear recursos.")

