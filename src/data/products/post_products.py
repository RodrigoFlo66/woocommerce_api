import pytest
from src.utils.faker_config import get600Caracteres, get_name_with_special_chars

def post_products_cases_params():
    """Define casos parametrizados para POST /products."""
    return [
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
        pytest.param({"regular_price": "rt12.3xr"}, None, 200, marks=pytest.mark.negative, id="regular_price_malformed"),
        pytest.param({"ffffff": "qweq"}, None, 201, marks=pytest.mark.negative, id="campo_inexistente"),
    ]