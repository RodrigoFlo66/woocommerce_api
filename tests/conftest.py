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
