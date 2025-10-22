from jsonschema import validate
from src.utils.logger import get_logger

logger = get_logger("api_assertions")


def assert_status_code(response, expected: int):
	try:
		assert response.status_code == expected, f"Expected {expected} but got {response.status_code}: {response.text}"
		logger.success(f"Status code check passed: {response.status_code} == {expected}")
	except AssertionError:
		logger.error(f"Status code check failed: expected {expected}, got {response.status_code}. Response: {response.text}")
		raise


def assert_schema(response_json: dict, schema: dict):
	try:
		validate(instance=response_json, schema=schema)
		logger.success("Schema validation passed")
	except Exception as exc:
		logger.error(f"Schema validation failed: {exc}")
		raise
