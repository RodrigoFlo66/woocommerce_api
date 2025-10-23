from jsonschema import validate
from src.utils.logger import get_logger
from typing import Iterable

logger = get_logger("api_assertions")


def assert_status_code(response, expected: int):
	try:
		assert response.status_code == expected, f"Expected {expected} but got {response.status_code}: {response.text}"
		logger.success(f"Status code esperado: {response.status_code} == {expected}")
	except AssertionError:
		logger.error(f"Status code check failed: expected {expected}, got {response.status_code}. Response: {response.text}")
		raise


def assert_schema(response_json: dict, schema: dict):
	try:
		validate(instance=response_json, schema=schema)
		logger.success("Validacion de schema exitoso")
	except Exception as exc:
		logger.error(f"Validacion de schema fallado: {exc}")
		raise


def assert_fields_equal(response_json: dict, fields: Iterable[str], request_payload: dict):
	"""Compare a set of fields between the response JSON and the original request payload.

	- Coerces both sides to str for lenient comparison (handles numeric vs string differences).
	- Logs successes and detailed mismatches, then raises AssertionError on any difference.
	"""
	mismatches = []
	for field in fields:
		expected = request_payload.get(field)
		actual = response_json.get(field)
		if expected is None and actual is None:
			continue
		if str(expected) != str(actual):
			mismatches.append((field, expected, actual))

	if mismatches:
		for field, expected, actual in mismatches:
			logger.error(f"Field mismatch for '{field}': expected={expected!r}, actual={actual!r}")
		raise AssertionError(f"Field mismatches: {[m[0] for m in mismatches]}")

	logger.success(f"Verificacion de campos iguales aprobado: {list(fields)}")
