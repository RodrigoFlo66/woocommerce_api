import pytest
from src.utils.faker_config import get600Caracteres
from src.utils.logger import get_logger
logger = get_logger("get_products_cases")

def get_all_products_cases_params():
    """Devuelve una lista de pytest.param para parametrizar tests de params.
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
        # Casos para path params (usar la clave 'id' en el dict)
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
            {"id": "USE_CREATED_PRODUCT"},
            200,
            marks=pytest.mark.negative,
            id="id_producto_malformed",
        ),
        pytest.param(
            {"id": "()&$/&%"},
            404,
            marks=pytest.mark.negative,
            id="id_producto_special_chars",
        ),
    ]

def get_all_products_cases_headers_specs():
    """Devuelve specs simples para parametrizar tests de headers.
    """
    return [
        pytest.param("no_headers", 401, marks=pytest.mark.negative, id="get_all_without_headers"),
        pytest.param("invalid_credentials", 401, marks=pytest.mark.negative, id="get_all_invalid_credentials"),
        pytest.param("expired_credentials", 401, marks=pytest.mark.negative, id="get_all_expired_credentials"),
        pytest.param("user_read", 200, marks=pytest.mark.positive, id="get_all_user_read"),
        pytest.param("user_write", 401, marks=[pytest.mark.negative, pytest.mark.xfail(reason= "EL sistema responde para un usuario sin permisos de lectura")], id="get_all_user_write"),
        pytest.param("user_admin", 200, marks=pytest.mark.positive, id="get_all_user_admin"),
        pytest.param("no_content_type", 200, marks=pytest.mark.positive, id="get_all_without_content_type"),
    ]

def get_headers(headers, headers_factory, case_id):
    """Test parametrizado para validar múltiples escenarios de headers en GET /products."""
    if case_id == "no_headers":
        case_headers = {}
    elif case_id == "invalid_credentials":
        case_headers = dict(headers)
        case_headers["Authorization"] = "Basic abm90X2FjdHVhbF9rZXk="
    elif case_id == "expired_credentials":
        case_headers = headers_factory(expired=True)
    elif case_id == "user_read":
        case_headers = headers_factory(role="read")
    elif case_id == "user_write":
        case_headers = headers_factory(role="write")
    elif case_id == "user_admin":
        case_headers = headers_factory()
    elif case_id == "no_content_type":
        case_headers = dict(headers)
        case_headers.pop("Content-Type", None)
    else:
        logger.warning(f"Caso desconocido recibido: {case_id}, usando headers por defecto")
        case_headers = dict(headers)

    logger.info(f"Ejecutando caso '{case_id}' con headers: {case_headers}")
    
    return case_headers