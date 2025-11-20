import os
import base64
import pytest

from src.api.client import APIClient
from src.utils.logger import get_logger
from dotenv import load_dotenv
from src.resources.payloads.products.payload_products import build_create_product_payload
from src.resources.payloads.customers.payload_customers import build_create_customer_payload
from src.api.endpoints import Endpoints
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
def headers_factory():
    """Factory to build headers for different user types and edge cases.

    Usage in tests:
        hdrs = headers_factory()  # default (uses API_KEY/API_SECRET)
        hdrs = headers_factory(role='read')  # uses API_KEY_READ/API_SECRET_READ if available
        hdrs = headers_factory(role='write')  # uses API_KEY_WRITE/API_SECRET_WRITE if available
        hdrs = headers_factory(omit_key=True)  # returns headers without Authorization
        hdrs = headers_factory(expired=True)  # use API_SECRET_EXPIRED or append '_expired'
        hdrs = headers_factory(key='explicit', secret='explicit')  # explicit credentials
    """
    def _build(role: str | None = None, key: str | None = None, secret: str | None = None, *, expired: bool = False, omit_key: bool = False, omit_secret: bool = False):
        if key is None:
            if role in ("read", "user_lectura"):
                key = os.getenv("API_KEY_READ")
            elif role in ("write", "user_escritura"):
                key = os.getenv("API_KEY_WRITE")
            else:
                key = os.getenv("API_KEY")

        if secret is None:
            if role in ("read", "user_lectura"):
                secret = os.getenv("API_SECRET_READ")
            elif role in ("write", "user_escritura"):
                secret = os.getenv("API_SECRET_WRITE")
            else:
                secret = os.getenv("API_SECRET")

        if expired:
            secret = os.getenv("API_SECRET_EXPIRED") or (secret + "_expired" if secret else None)

        if omit_key:
            key = None
        if omit_secret:
            secret = None

        if not key or not secret:
            return {"Content-Type": "application/json"}

        credentials = f"{key}:{secret}".encode("utf-8")
        encoded_credentials = base64.b64encode(credentials).decode("utf-8")
        return {
            "Authorization": f"Basic {encoded_credentials}",
            "Content-Type": "application/json",
        }

    return _build

@pytest.fixture
def payload():
    """Fixture that returns a default product creation payload.
    """
    return build_create_product_payload()

@pytest.fixture
def create_product(client, headers, request, logger):
    """Factory fixture that returns a callable to create a product and ensures teardown.
    """
    created_ids = []

    def _create(payload=None, payload_overrides=None, headers_overrides=None, metod=None, merge: bool = False, update: bool = False):
        if merge:
            base_payload = build_create_product_payload() if payload is None else dict(payload)
            if payload_overrides is not None:
                base_payload.update(payload_overrides)
        else:
            if payload is None:
                base_payload = build_create_product_payload()
            else:
                base_payload = dict(payload)

            if payload_overrides is not None:
                if payload_overrides == {}:
                    base_payload = payload_overrides
                else:
                    base_payload.update(payload_overrides)

        if headers_overrides is not None:
            hdrs = headers_overrides
        else:
            hdrs = dict(headers) if headers else {}

        if update == False:
            logger.info(f"Payload={base_payload} headers={hdrs}")
        if metod is not None:
            resp = client.delete(Endpoints.PRODUCTS.value, json=base_payload, headers=hdrs)
        else:
            resp = client.post(Endpoints.PRODUCTS.value, json=base_payload, headers=hdrs)
        try:
            pid = resp.json().get("id")
            if pid:
                created_ids.append(pid)
                if update == True:
                    logger.info(f"Producto creado, id={pid}, payload={base_payload}")            
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

@pytest.fixture
def payload_customer():
    """Fixture that returns a default customer creation payload.
    """
    return build_create_customer_payload()

@pytest.fixture
def create_customer(client, headers, request, logger):
    """Factory fixture that returns a callable to create a customer and ensures teardown.
    """
    created_ids = []

    def _create(payload=None, payload_overrides=None, headers_overrides=None, metod=None, merge: bool = False, update: bool = False):
        if isinstance(payload, str):
            base_payload = payload
        else:
            if merge:
                base_payload = build_create_customer_payload() if payload is None else dict(payload)
                if payload_overrides is not None:
                    base_payload.update(payload_overrides)
            else:
                if payload is None:
                    base_payload = build_create_customer_payload()
                else:
                    base_payload = dict(payload)

                if payload_overrides is not None:
                    if payload_overrides == {}:
                        base_payload = payload_overrides
                    else:
                        base_payload.update(payload_overrides)

        if headers_overrides is not None:
            hdrs = headers_overrides
        else:
            hdrs = dict(headers) if headers else {}

        if update == False:
            logger.info(f"Customer payload={base_payload} headers={hdrs}")

        if metod is not None:
            if isinstance(base_payload, str):
                resp = client.delete(Endpoints.CUSTOMERS.value, data=base_payload, headers=hdrs)
            else:
                resp = client.delete(Endpoints.CUSTOMERS.value, json=base_payload, headers=hdrs)
        else:
            if isinstance(base_payload, str):
                resp = client.post(Endpoints.CUSTOMERS.value, data=base_payload, headers=hdrs)
            else:
                resp = client.post(Endpoints.CUSTOMERS.value, json=base_payload, headers=hdrs)

        try:
            cid = resp.json().get("id")
            if cid:
                created_ids.append(cid)
                if update == True:
                    logger.info(f"Customer created, id={cid}, payload={base_payload}")
        except Exception:
            logger.error("Failed reading response JSON while creating customer")

        return resp, base_payload

    def _teardown():
        from src.api.endpoints import Endpoints
        for cid in created_ids:
            endpoint = f"{Endpoints.CUSTOMERS.value}/{cid}?force=true"
            logger.info(f"Tearing down customer id={cid}")
            try:
                client.delete(endpoint, headers=headers)
            except Exception as exc:
                logger.error(f"Failed to delete customer id={cid}: {exc}")

    request.addfinalizer(_teardown)
    return _create
