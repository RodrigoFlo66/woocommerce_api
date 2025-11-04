import pytest

def delete_products_cases_params():
    """Devuelve una lista de pytest.param para parametrizar tests de params.
    """
    return [
        pytest.param(
            {"id": "USE_CREATED_PRODUCT"},
            200,
            marks=pytest.mark.positive,
            id="id_producto_valido",
        ),
        pytest.param(
            {"id": 9999999},
            404,
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
        pytest.param(
            {"id": "1 OR 1=1"},
            404,
            marks=pytest.mark.negative,
            id="param_sql_injection",
        ),
    ]