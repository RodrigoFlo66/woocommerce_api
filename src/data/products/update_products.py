import pytest
from src.utils.faker_config import get600Caracteres, get_name_with_special_chars

def put_products_cases_payload():
    """Define casos parametrizados para POST /products."""
    return [
        pytest.param(None, None, 200, marks=[pytest.mark.positive, pytest.mark.smoke], id="valid_full"),
        pytest.param({"name": None}, "Producto", 200, marks=[pytest.mark.negative, pytest.mark.xfail(reason="Al enviar nombre de producto vacio, la api no genera el nombre predeterminado dejandolo vacio")], id="no_name"),
        pytest.param({"name": get600Caracteres()}, None, 400, marks=[pytest.mark.negative, pytest.mark.xfail(reason="Permite actualizar productos con nombres mayores a 600 caracteres")], id="name_600_chars"),
        pytest.param({"name": get_name_with_special_chars()}, None, 200, marks=[pytest.mark.negative, pytest.mark.xfail(reason="La respuesta modifica los caracteres especiales de un nombre")], id="name_special_chars"),
        pytest.param({"name": "  "}, "Producto", 200, marks=[pytest.mark.negative, pytest.mark.xfail(reason="Permite actualizar productos sin nombres al introducir espacios")], id="name_spaces_chars"),
        pytest.param({}, "Producto", 200, marks=pytest.mark.negative, id="empty_payload_expected_Producto"),
        pytest.param({"name": True}, None, 400, marks=pytest.mark.negative , id="name_boolean"),
        pytest.param({"regular_price": 19.9}, None, 400, marks=pytest.mark.negative, id="regular_price_double"),
        pytest.param({"regular_price": "19.9", "sale_price": "20"}, None, 200, marks=[pytest.mark.negative], id="sale_price_higher_than_regular"),
        pytest.param({"regular_price": "-12", "sale_price": "-16"}, None, 400, marks=[pytest.mark.negative, pytest.mark.xfail(reason="Permite actualizar productos con valores negativos en los precios")], id="sale_and_regular_price_negative"),
        pytest.param({"regular_price": "rt12.3xr"}, None, 200, marks=pytest.mark.negative, id="regular_price_malformed"),
        pytest.param({"ffffff": "qweq"}, None, 200, marks=pytest.mark.negative, id="campo_inexistente"),
    ]

def put_products_cases_params():
    """Devuelve una lista de pytest.param para parametrizar tests de params.
    """
    return [
        pytest.param(
            {"id": "USE_CREATED_PRODUCT"},
            200,
            marks=[pytest.mark.positive, pytest.mark.smoke],
            id="id_producto_valido",
        ),
        pytest.param(
            {"id": 9999999},
            400,
            marks=pytest.mark.negative,
            id="id_producto_invalido",
        ),
        pytest.param(
            {"id": "abc"},
            404,
            marks=pytest.mark.negative,
            id="id_producto_no_numerico",
        ),
        pytest.param(
            {"id": -1},
            404,
            marks=pytest.mark.negative,
            id="id_producto_negativo",
        ),
        pytest.param(
            {"id": ""},
            404,
            marks=pytest.mark.negative,
            id="id_producto_con_espacios",
        ),
        pytest.param(
            {"id": None},
            404,
            marks=pytest.mark.negative,
            id="id_producto_vacio",
        ),
        pytest.param(
            {"id": "()&$/&%"},
            404,
            marks=pytest.mark.negative,
            id="id_producto_special_chars",
        ),
        pytest.param(
            {"id": "?force=true&force=false"},
            200,
            marks=pytest.mark.negative,
            id="query_param_force_multiple_in_id",
        ),
        pytest.param(
            {"id": "?page=abc"},
            200,
            marks=pytest.mark.negative,
            id="query_param_page_in_id",
        ),
        pytest.param(
            {"id": "?force=true"},
            200,
            marks=pytest.mark.negative,
            id="query_param_force_in_id",
        ),
        pytest.param(
            {"id": "?force=false"},
            200,
            marks=pytest.mark.negative,
            id="guery_param_force_false",
        ),
    ]

def put_products_cases_headers():
    """Devuelve specs simples para parametrizar tests de headers.
    """
    return [
        pytest.param("no_headers", 401, marks=pytest.mark.negative, id="without_headers"),
        pytest.param("invalid_credentials", 401, marks=pytest.mark.negative, id="invalid_credentials"),
        pytest.param("expired_credentials", 401, marks=pytest.mark.negative, id="expired_credentials"),
        pytest.param("user_write", 200, marks=[pytest.mark.positive, pytest.mark.smoke], id="user_write"),
        pytest.param("user_read", 401, marks=[pytest.mark.negative, pytest.mark.xfail(reason= "EL sistema responde para un usuario sin permisos de escritura")], id="user_read"),
        pytest.param("user_admin", 200, marks=[pytest.mark.positive, pytest.mark.smoke], id="user_admin"),
        pytest.param("no_content_type", 200, marks=pytest.mark.positive, id="without_content_type"),
    ]