from src.utils.faker_config import product_payload


def build_create_product_payload(name: str | None = None) -> dict:
	"""Return a payload ready to send to the API for creating a product."""
	return product_payload(name=name)
