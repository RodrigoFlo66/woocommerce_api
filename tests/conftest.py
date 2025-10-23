import os
import base64
import pytest

from src.api.client import APIClient
from src.utils.logger import get_logger
from dotenv import load_dotenv
load_dotenv()

BASE_URL = os.getenv("BASE_URL")

@pytest.fixture(scope="session")
def logger():
	return get_logger("woocommerce_tests")


@pytest.fixture(scope="session")
def client():
	base = BASE_URL
	return APIClient(base_url=base)


@pytest.fixture
def headers():
    key = os.getenv("API_KEY")
    secret = os.getenv("API_SECRET")

    credentials = f"{key}:{secret}".encode("utf-8")
    encoded_credentials = base64.b64encode(credentials).decode("utf-8")

    return {
        "Authorization": f"Basic {encoded_credentials}",
        "Content-Type": "application/json"
    }


@pytest.fixture
def create_product(client, headers, request, logger):
    """Factory fixture that returns a callable to create a product and ensures teardown.
    """
    created_ids = []

    def _create(payload=None, payload_overrides=None, headers_overrides=None):
        from src.resources.payloads.products.create_product import build_create_product_payload
        from src.api.endpoints import Endpoints

        if payload is None:
            base_payload = build_create_product_payload()
        else:
            base_payload = payload

        if payload_overrides is not None:
            if payload_overrides == {}:
                base_payload = payload_overrides
            else:
                base_payload.update(payload_overrides)

        if headers_overrides is not None:
            hdrs = headers_overrides
        else:
            hdrs = dict(headers) if headers else {}

        logger.info(f"Payload={base_payload} headers={hdrs}")
        resp = client.post(Endpoints.PRODUCTS.value, json=base_payload, headers=hdrs)
        try:
            pid = resp.json().get("id")
            if pid:
                created_ids.append(pid)
        except Exception:
            logger.error("Failed reading response JSON while creating product")

        return resp, base_payload

    def _teardown():
        from src.api.endpoints import Endpoints
        for pid in created_ids:
            endpoint = f"{Endpoints.PRODUCTS.value}/{pid}"
            logger.info(f"Tearing down product id={pid}")
            try:
                client.delete(endpoint, headers=headers)
            except Exception as exc:
                logger.error(f"Failed to delete product id={pid}: {exc}")

    request.addfinalizer(_teardown)
    return _create
