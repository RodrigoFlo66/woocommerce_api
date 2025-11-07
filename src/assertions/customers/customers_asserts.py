import json
from typing import Iterable

from src.assertions.api_assertions import assert_status_code, assert_schema, assert_fields_equal
from src.utils.logger import get_logger

logger = get_logger("customer_asserts")


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


def assert_customer_created(response, request_payload, status_code=201, equal=True, validate_request_schema: bool = True):
    """Assert a successful customer creation.
    """
    req_payload = _ensure_payload_dict(request_payload)

    if validate_request_schema:
        try:
            body_schema = json.loads(open("src/resources/schemas/customers/customer_body_schema.json").read())
            assert_schema(req_payload, body_schema)
        except AssertionError:
            logger.error("Request payload failed schema validation")
            raise
        except Exception:
            logger.warning("Could not read/validate customer body schema; continuing without request-schema check")

    assert_status_code(response, status_code)
    try:
        body = response.json()
    except Exception:
        logger.error("Response body is not valid JSON")
        raise

    logger.info(f"Response body: {body}")

    cmp_req = dict(req_payload) if isinstance(req_payload, dict) else {}
    if "role" not in cmp_req:
        cmp_req["role"] = "customer"

    fields_to_check = ["email", "first_name", "last_name", "username", "role"]
    try:
        if validate_request_schema:
            if request_payload != {}:
                uname = cmp_req.get("username")
                if not uname:
                    email_val = cmp_req.get("email") or ""
                    derived = email_val.split("@", 1)[0] if "@" in email_val else email_val
                    cmp_req["username"] = derived

                assert_fields_equal(body, fields_to_check, cmp_req, equal)
    except AssertionError:
        logger.error("Uno o más campos no coinciden en la creación del cliente")
        raise

    try:
        resp_schema = json.loads(open("src/resources/schemas/customers/customer_response_schema.json").read())
        assert_schema(body, resp_schema)
    except AssertionError:
        logger.error("Response schema validation failed for created customer")
        raise
    except Exception:
        logger.warning("Could not read/validate customer response schema; skipping response-schema check")

    logger.success(f"Cliente creado exitosamente id={body.get('id')}")


def assert_customer_failure(response, expected_status=None, expected_message_contains: str | None = None, expected_field_errors: dict | None = None):
    """Assert that customer creation failed with expected properties (similar to product failure helper)."""
    logger.info(f"Status code recibido: {response.status_code}, Esperado: {expected_status}")
    logger.info(f"Response body: {response.json()}")
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

    if status == 201:
        logger.error(f"success (201). Response body: {body_text}")
        return

    if status == 400:
        logger.error(f"Bad Request (400). Response body: {body_text}")
        if expected_field_errors:
            for field, substr in expected_field_errors.items():
                logger.error(f"Campo no válido '{field}': {substr}")
        return

    if status == 401:
        logger.error(f"Unauthorized (401). Response body: {body_text}")
        logger.info(f"Status code recibido: {status}, Esperado: {expected_status}")
        logger.info("Falta de headers de autenticación")
        return

    if status == 404:
        logger.error(f"Not Found (404). Response body: {body_text}")
        logger.info(f"Status code recibido: {status}, Esperado: {expected_status}")
        logger.info("Not Found (404)")
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

    logger.info("Error no específico manejado")


def assert_customer_getted(response, status_code: int = 200, single_customer: bool = False):
    """Assert that a customer (or list) was successfully retrieved and validate schema."""
    try:
        logger.info(f"Response Body: {response.json()}")
    except Exception:
        logger.warning("[GET Customer] Response body could not be parsed as JSON.")

    assert_status_code(response, expected=status_code)

    resp_schema = json.loads(open("src/resources/schemas/customers/customer_response_schema.json").read())
    if single_customer:
        assert_schema(response.json(), resp_schema)
    else:
        arr = response.json()
        if isinstance(arr, list):
            for item in arr:
                assert_schema(item, resp_schema)
        else:
            assert_schema(arr, resp_schema)


def assert_get_failure(response, expected_status: int):
    logger.info(f"Expected Failure Status: {response.status_code}")
    try:
        logger.info(f"Expected Failure Body: {response.json()}")
    except Exception:
        logger.warning("Expected Failure Response body not in JSON format.")

    assert_status_code(response, expected=expected_status)


__all__ = [
    "assert_customer_created",
    "assert_customer_failure",
    "assert_customer_getted",
    "assert_get_failure",
]


def assert_customer_updated(response, request_payload, status_code=200, equal=True, validate_request_schema: bool = True):
    """Assert a successful customer update and that key fields match the request payload.
    """
    req_payload = _ensure_payload_dict(request_payload)

    if validate_request_schema:
        try:
            body_schema = json.loads(open("src/resources/schemas/customers/customer_body_schema.json").read())
            assert_schema(req_payload, body_schema)
        except AssertionError:
            logger.error("Request payload failed schema validation")
            raise
        except Exception:
            logger.warning("Could not read/validate customer body schema; continuing without request-schema check")

    assert_status_code(response, status_code)
    try:
        body = response.json()
    except Exception:
        logger.error("Response body is not valid JSON")
        raise

    logger.info(f"Response body: {body}")

    cmp_req = dict(req_payload) if isinstance(req_payload, dict) else {}
    if "role" not in cmp_req:
        cmp_req["role"] = "customer"

    fields_to_check = ["email", "first_name", "last_name", "role"]
    try:
        if request_payload != {}:
            uname = cmp_req.get("username")
            if not uname:
                email_val = cmp_req.get("email") or ""
                derived = email_val.split("@", 1)[0] if "@" in email_val else email_val
                cmp_req["username"] = derived

            assert_fields_equal(body, fields_to_check, cmp_req, equal)
    except AssertionError:
        logger.error("One or more field comparisons failed for customer update")
        raise

    try:
        resp_schema = json.loads(open("src/resources/schemas/customers/customer_response_schema.json").read())
        assert_schema(body, resp_schema)
    except AssertionError:
        logger.error("Response schema validation failed for updated customer")
        raise
    except Exception:
        logger.warning("Could not read/validate customer response schema; skipping response-schema check")

    logger.success(f"Cliente actualizado exitosamente id={body.get('id')}")
