import pytest

from src.api.endpoints import Endpoints
from src.resources.payloads.products.create_product import build_create_product_payload
from src.assertions.products.products_asserts import assert_product_created


@pytest.mark.smoke
def test_create_product_basic(client, headers):
	"""Basic example test creating a product using client, payloads, endpoints and assertions.
	"""
	payload = build_create_product_payload()
	endpoint = Endpoints.PRODUCTS.value

	resp = client.post(endpoint, json=payload, headers=headers)
	assert_product_created(resp, payload)
