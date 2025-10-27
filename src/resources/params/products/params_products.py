import pytest
from src.utils.faker_config import get600Caracteres


def get_all_products_cases():
    """Devuelve una lista de pytest.param para parametrizar tests de GET /products.

    Cada elemento es pytest.param(query_params_dict, expected_status, marks=..., id=...)
    """
    return [
        pytest.param(
            {"per_page": 5, "page": 2},
            200,
            marks=pytest.mark.positive,
            id="per_page_5_page_2",
        ),
        pytest.param(
            {"orderby": "price", "order": "asc"},
            200,
            marks=pytest.mark.positive,
            id="orderby_price_asc",
        ),
        pytest.param(
            {"per_page": 5, "orderby": "price"},
            200,
            marks=pytest.mark.positive,
            id="multiple_filters",
        ),
        pytest.param(
            {"invalidParam": "true"},
            200,
            marks=pytest.mark.negative,
            id="invalid_query_param_name",
        ),
        pytest.param(
            {"per_page": 1000},
            400,
            marks=pytest.mark.negative,
            id="excessive_per_page_value",
        ),
        pytest.param(
            {"page": "abc"},
            400,
            marks=pytest.mark.negative,
            id="non_numeric_page",
        ),
        pytest.param(
            {"page": ""},
            400,
            marks=pytest.mark.negative,
            id="empty_query_value",
        ),
        pytest.param(
            {"search": get600Caracteres()},
            200,
            marks=[pytest.mark.positive],
            id="search_600_chars",
        ),
    ]