import os
import requests


class APIClient:
	"""Small wrapper around requests to keep tests using a client instead of calling requests directly.

	The client uses a base_url from environment variable BASE_URL or a provided value.
	"""

	def __init__(self, base_url: str | None = None, timeout: int = 10):
		self.base_url = base_url
		self.timeout = timeout

	def _build_url(self, endpoint: str) -> str:
		return f"{self.base_url.rstrip('/')}{endpoint}"

	def post(self, endpoint: str, json: dict | None = None, data: object | None = None, headers: dict | None = None, params: dict | None = None):
		url = self._build_url(endpoint)
		return requests.post(url, json=json, data=data, headers=headers, params=params, timeout=self.timeout)

	def delete(self, endpoint: str, json: dict | None = None, data: object | None = None, headers: dict | None = None, params: dict | None = None):
		url = self._build_url(endpoint)
		return requests.delete(url, json=json, data=data, headers=headers, params=params, timeout=self.timeout)
	
	def getAll(self, endpoint: str, json: dict | None = None, data: object | None = None, headers: dict | None = None, params: dict | None = None):
		url = self._build_url(endpoint)
		return requests.get(url, json=json, data=data, headers=headers, params=params, timeout=self.timeout)
	
	def get(self, endpoint: str, json: dict | None = None, data: object | None = None, headers: dict | None = None, params: dict | None = None):
		url = self._build_url(endpoint)
		return requests.get(url, json=json, data=data, headers=headers, params=params, timeout=self.timeout)

	def put(self, endpoint: str, json: dict | None = None, data: object | None = None, headers: dict | None = None, params: dict | None = None):
		url = self._build_url(endpoint)
		return requests.put(url, json=json, data=data, headers=headers, params=params, timeout=self.timeout)

	def patch(self, endpoint: str, json: dict | None = None, data: object | None = None, headers: dict | None = None, params: dict | None = None):
		url = self._build_url(endpoint)
		return requests.patch(url, json=json, data=data, headers=headers, params=params, timeout=self.timeout)
