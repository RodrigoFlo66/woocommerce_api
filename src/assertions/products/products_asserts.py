import json

from src.assertions.api_assertions import assert_status_code, assert_schema
from src.utils.logger import get_logger

logger = get_logger("product_asserts")


def assert_product_created(response, request_payload: dict):
    logger.info(f"Payload: {request_payload}")
    assert_status_code(response, 201)
    body = response.json()
    logger.info(f"Response body: {body}")
    # basic content checks
    if body.get("name") != request_payload.get("name"):
        logger.error(f"Product name mismatch. Expected {request_payload.get('name')}, got {body.get('name')}")
        raise AssertionError("Product name mismatch")
    schema = json.loads(open("src/resources/schemas/products/product_post_response_schema.json").read())
    assert_schema(body, schema)
    logger.success(f"Product created successfully with id={body.get('id')}")


__all__ = ["assert_product_created"]