import pytest

def delete_customers_headers():
    """Header scenarios specifically for DELETE /customers.
    """
    return [
        pytest.param("no_headers", 401, [pytest.mark.negative, pytest.mark.smoke], id="no_headers"),
        pytest.param("no_content_type", 200, marks=pytest.mark.negative, id="no_content_type"),
        pytest.param("content_type_incorrect", 200, marks=pytest.mark.negative, id="content_type_incorrect"),
        pytest.param("invalid_credentials", 401, marks=pytest.mark.negative, id="invalid_credentials"),
        pytest.param("expired_credentials", 401, marks=pytest.mark.negative, id="expired_credentials"),
        pytest.param("user_read", 401, marks=[pytest.mark.negative, pytest.mark.xfail(reason="Permite eliminar cleintes con un usuario con credenciales de solo lectura")], id="user_read"),
        pytest.param("user_write", 200, marks=[pytest.mark.positive, pytest.mark.smoke], id="user_write"),
        pytest.param("user_admin", 200, marks=[pytest.mark.positive, pytest.mark.smoke], id="user_admin"),
    ]

def delete_customers_cases_params():
    """Devuelve una lista de pytest.param para parametrizar tests de params.
    """
    return [
        pytest.param({"id": "USE_CREATED?force=true"}, 200, marks=[pytest.mark.positive, pytest.mark.smoke], id="delete_existing_force_true"),
        pytest.param({"id": "USE_CREATED"}, 501, marks=[pytest.mark.positive, pytest.mark.smoke], id="delete_existing_no_force"),
        pytest.param({"id": 9999999}, 404, marks=pytest.mark.negative, id="delete_nonexistent"),
        pytest.param({"id": "abc"}, 404, marks=pytest.mark.negative, id="delete_non_numeric"),
        pytest.param({"id": -1}, 404, marks=pytest.mark.negative, id="delete_negative"),
        pytest.param({"id": "!@#"}, 404, marks=pytest.mark.negative, id="delete_special_chars"),
        pytest.param({"id": ""}, 404, marks=[pytest.mark.negative, pytest.mark.smoke], id="delete_empty_id"),
        pytest.param({"id": "USE_CREATED?force=true&reassign=12"}, 400, marks=pytest.mark.positive, id="delete_with_extra_queryparams"),
        pytest.param({"id": "USE_CREATED?unknown_param=1"}, 501, marks=pytest.mark.positive, id="delete_unknown_queryparam"),
        pytest.param({"id": "USE_CREATED?page=abc"}, 501, marks=pytest.mark.positive, id="delete_with_malformed_queryparam"),
        pytest.param({"id": "USE_CREATED?force=true&force=false"}, 501, marks=pytest.mark.positive, id="delete_redundant_queryparams"),
        pytest.param({"id": "USE_CREATED?force=false"}, 501, marks=pytest.mark.positive, id="delete_force_false"),
        pytest.param({"id": "USE_CREATED?force=true&page=abc"}, 200, marks=pytest.mark.positive, id="delete_force_and_malformed"),
        pytest.param({"id": "1' OR '1'='1"}, 404, marks=pytest.mark.negative, id="delete_sql_injection"),
        pytest.param({"id": "1,2,3"}, 404, marks=pytest.mark.negative, id="delete_multiple_ids_malformed"),
    ]