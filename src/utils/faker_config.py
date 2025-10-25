from faker import Faker

fake = Faker()


def product_payload(name: str | None = None) -> dict:
	"""Generate a minimal create-product payload using Faker."""
	name = name or fake.unique.word().capitalize() + " " + fake.word()
	return {
		"name": name,
		"type": "simple",
		"regular_price": str(round(fake.pyfloat(right_digits=2, positive=True, min_value=1, max_value=100), 2)),
		"description": fake.sentence(nb_words=10),
		"short_description": fake.sentence(nb_words=6),
	}


def get600Caracteres() -> str:
	"""Return a deterministic string of 600 characters for edge-case tests."""
	base = "ProductoLargo"
	s = (base * ((600 // len(base)) + 1))[:600]
	return s


def get_name_with_special_chars() -> str:
	"""Return a short name containing special characters and non-ascii letters."""
	return "Prueba-ñ-á-Ö-#-$-%-&-()/\\"
