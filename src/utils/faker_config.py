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
