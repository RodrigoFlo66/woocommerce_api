from enum import Enum


class Endpoints(str, Enum):
	PRODUCTS = "/wp-json/wc/v3/products"
	PRODUCT = "/wp-json/wc/v3/products/{}"
	CUSTOMERS = "/wp-json/wc/v3/customers"
	CUSTOMER = "/wp-json/wc/v3/customers/{}"


__all__ = ["Endpoints"]
