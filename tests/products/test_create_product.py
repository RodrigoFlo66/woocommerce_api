import pytest

from src.assertions.products.products_asserts import assert_product_created
from src.assertions.products.products_asserts import assert_product_failure
from src.utils.logger import get_logger
from src.utils.faker_config import get600Caracteres, get_name_with_special_chars
from src.resources.payloads.products.create_product import product_image_scenarios

logger = get_logger("test_create_product")

@pytest.mark.parametrize(
    "payload_overrides, expected_generated_name, expected_status",
    [
        pytest.param(None, None, 201, marks=pytest.mark.smoke, id="valid_full"),
        pytest.param({"name": None}, "Producto", 201, marks=pytest.mark.negative, id="no_name"),
        pytest.param({"name": get600Caracteres()}, None, 400, marks=[pytest.mark.negative, pytest.mark.xfail(reason="Permite crear productos con nombres mayores a 600 caracteres")], id="name_600_chars"),
        pytest.param({"name": get_name_with_special_chars()}, None, 201, marks=[pytest.mark.negative, pytest.mark.xfail(reason="La respuesta modifica los caracteres especiales de un nombre")], id="name_special_chars"),
        pytest.param({"name": "  "}, "Producto", 201, marks=[pytest.mark.negative, pytest.mark.xfail(reason="Permite crear productos sin nombres al introducir espacios")], id="name_spaces_chars"),
        pytest.param({}, "Producto", 201, marks=pytest.mark.negative, id="empty_payload_expected_Producto"),
        pytest.param({"name": True}, None, 400, marks=pytest.mark.negative , id="name_boolean"),
        pytest.param({"regular_price": 19.9}, None, 400, marks=pytest.mark.negative, id="regular_price_double"),
        pytest.param({"regular_price": "19.9", "sale_price": "20"}, None, 400, marks=[pytest.mark.negative, pytest.mark.xfail(reason="Se crea el producto eliminando el valor de sale_price cuando este es mayor a regular_price")], id="sale_price_higher_than_regular"),
        pytest.param({"regular_price": "-12", "sale_price": "-16"}, None, 400, marks=[pytest.mark.negative, pytest.mark.xfail(reason="Permite crear productos con valores negativos en los precios")], id="sale_and_regular_price_negative"),
        pytest.param({"ffffff": "qweq"}, None, 201, marks=pytest.mark.negative, id="campo_inexistente"),
    ],
)
def test_create_product_parametrized(create_product, payload_overrides, expected_generated_name, expected_status):
    """Test con payload parametrizados.
    """
    if payload_overrides and isinstance(payload_overrides, dict) and "regular_price" in payload_overrides and "sale_price" in payload_overrides:
        resp, used_payload = create_product(payload_overrides=payload_overrides, merge=True)
        assert_product_failure(resp, expected_status=400)
        pytest.xfail("Known issue: sale_price greater than regular_price should be rejected — documented as xfail")
    else:
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

@pytest.mark.negative
def test_create_product_API_key_invalid(create_product):
    """Intenta crear un producto con una API Key inválida."""
    resp, used_payload = create_product(headers_overrides={"Authorization": "Basic abm90X2FjdHVhbF9rZXk="})
    assert_product_failure(resp, expected_status=(401), expected_message_contains="Lo siento, no tienes permiso para crear recursos.")

@pytest.mark.negative
def test_create_product_without_content_type(create_product):
    """Intenta crear un producto sin el header Content-Type."""
    resp, used_payload = create_product(headers_overrides={"Content-Type": None})
    assert_product_failure(resp, expected_status=(401), expected_message_contains="Lo siento, no tienes permiso para crear recursos.")

@pytest.mark.negative
def test_create_product_API_secret_expired(create_product, headers_factory):
    """Intenta crear un producto con un API Secret expirado"""
    hdrs = headers_factory(expired=True)
    resp, used_payload = create_product(headers_overrides=hdrs)
    assert_product_failure(resp, expected_status=(401), expected_message_contains="Lo siento, no tienes permiso para crear recursos.")

@pytest.mark.negative
@pytest.mark.xfail(reason="Las credenciales de solo lectura permiten crear productos, aunque no deberían")
def test_create_product_user_read(create_product, headers_factory):
    """Intenta crear un producto con las credenciales de un usuario con permisos de solo lectura."""
    hdrs = headers_factory(role='read')
    resp, used_payload = create_product(headers_overrides=hdrs)
    assert_product_failure(resp, expected_status=(401), expected_message_contains="Lo siento, no tienes permiso para crear recursos.")

@pytest.mark.positive
def test_create_product_user_write(create_product, headers_factory):
    """Intenta crear un producto con las credenciales de un usuario con permisos de solo escritura."""
    hdrs = headers_factory(role='write')
    resp, used_payload = create_product(headers_overrides=hdrs)
    assert_product_created(resp, used_payload)

@pytest.mark.positive
def test_create_product_user_admin(create_product, headers_factory):
    """Intenta crear un producto con las credenciales de un usuario administrador(lectura y escritura)."""
    hdrs = headers_factory()
    resp, used_payload = create_product(headers_overrides=hdrs)
    assert_product_created(resp, used_payload)

@pytest.mark.parametrize("scenario",
    [
    pytest.param(s, marks=[pytest.mark.positive], id=s["title"]) if s.get("expected_status") == 201
    else pytest.param(s, marks=[pytest.mark.negative], id=s["title"]) for s in product_image_scenarios()
    ])
def test_create_product_with_images(create_product, scenario):
    """Prueba la creación de productos con distintas configuraciones de imagenes.
    """
    payload_overrides = {"images": scenario["images"]}
    resp, used_payload = create_product(payload_overrides=payload_overrides)

    expected = scenario.get("expected_status")
    if expected == 201:
        assert_product_created(resp, used_payload)
    else:
        assert_product_failure(resp, expected_status=expected)