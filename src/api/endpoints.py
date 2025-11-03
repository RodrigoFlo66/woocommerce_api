from enum import Enum


class Endpoints(str, Enum):
	PRODUCTS = "/wp-json/wc/v3/products"
	PRODUCT = "/wp-json/wc/v3/products/{}"


__all__ = ["Endpoints"]
