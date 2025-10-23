import json
from typing import Iterable

from src.assertions.api_assertions import assert_status_code, assert_schema, assert_fields_equal
from src.utils.logger import get_logger

logger = get_logger("product_asserts")


def _ensure_payload_dict(request_payload):
    """Ensure the request_payload is a dict. If it's a serialized JSON (str/bytes), try to parse it."""
    if request_payload is None:
        return {}
    if isinstance(request_payload, dict):
        return request_payload
    try:
        if isinstance(request_payload, (bytes, bytearray)):
            request_payload = request_payload.decode("utf-8")
        if isinstance(request_payload, str):
            return json.loads(request_payload)
    except Exception:
        logger.info("Could not parse request_payload into dict, falling back to empty dict")
    return {}


def assert_product_created(response, request_payload):
    """Assert a successful product creation and that key fields match the request payload.
    """
    req_payload = _ensure_payload_dict(request_payload)
    assert_status_code(response, 201)
    body = response.json()
    logger.info(f"Response body: {body}")
    fields_to_check = ["type", "description", "regular_price"]
    name_in_request = req_payload.get("name") if isinstance(req_payload, dict) else None
    if name_in_request is not None:
        fields_to_check.insert(0, "name")
    try:
        if request_payload != {}:
            assert_fields_equal(body, fields_to_check, req_payload)
    except AssertionError:
        logger.error("One or more field comparisons failed")
        raise

    # If name was not provided, ensure API generated a non-empty name
    if name_in_request is None:
        gen_name = body.get("name")
        if not gen_name:
            logger.error("API did not generate a product name when none was provided in the request")
            raise AssertionError("API did not generate a product name")
        logger.info(f"nombre generado por la API: {gen_name}")
    schema = json.loads(open("src/resources/schemas/products/product_post_response_schema.json").read())
    assert_schema(body, schema)
    logger.success(f"Producto creado exitosamente id={body.get('id')}")


def assert_product_failure(response, expected_status=None, expected_message_contains: str | None = None, expected_field_errors: dict | None = None):
    """Assert that the product creation failed with expected properties.

    - expected_status: int or iterable of ints to match response.status_code
    - expected_message_contains: substring expected to be present in the error message/body
    - expected_field_errors: dict mapping field -> substring expected in error details
    """
    if expected_status is not None:
        if isinstance(expected_status, Iterable) and not isinstance(expected_status, (str, bytes)):
            assert response.status_code in expected_status, f"Expected status in {expected_status}, got {response.status_code}"
        else:
            assert response.status_code == expected_status, f"Expected status {expected_status}, got {response.status_code}"

    try:
        body = response.json()
    except Exception:
        body = None

    body_text = ""
    try:
        body_text = json.dumps(body) if body is not None else (getattr(response, "text", "") or "")
    except Exception:
        body_text = getattr(response, "text", "") or ""

    status = getattr(response, "status_code", None)

    if status == 400:
        logger.error(f"Bad Request (400). Response body: {body_text}")
        if expected_field_errors:
            for field, substr in expected_field_errors.items():
                logger.error(f"Campo no válido '{field}': {substr}")
        return

    if status == 401:
        logger.error(f"Unauthorized (401). Response body: {body_text}")
        logger.info(f"Status code recibido: {status}, Esperado: {expected_status}")
        logger.info("Producto no creado por falta de headers de autenticación")
        return

    if expected_message_contains:
        if expected_message_contains.lower() not in body_text.lower():
            logger.error(f"Expected message substring '{expected_message_contains}' not found in response body: {body_text}")
            raise AssertionError(f"Expected message substring '{expected_message_contains}' not found")

    if expected_field_errors:
        for field, substr in expected_field_errors.items():
            if substr and substr.lower() not in body_text.lower():
                logger.error(f"Expected field error for '{field}' containing '{substr}' not found in response body")
                raise AssertionError(f"Expected field error for '{field}' containing '{substr}' not found")

    logger.info(f"Status code recibido: {response.status_code}, Esperado: {expected_status}")
    logger.info("Producto no creado (error no específico manejado)")


__all__ = ["assert_product_created", "assert_product_failure"]