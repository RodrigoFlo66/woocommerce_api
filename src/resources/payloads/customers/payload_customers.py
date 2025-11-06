from src.utils.faker_config import fake


def build_create_customer_payload(email: str | None = None) -> dict:
	"""Return a payload for creating a customer. Only email is mandatory.
	"""
	email = email or fake.unique.email()
	first_name = fake.first_name()
	last_name = fake.last_name()
	username = email.split("@")[0]
	billing = {
		"first_name": first_name,
		"last_name": last_name,
		"company": "",
		"address_1": fake.street_address(),
		"address_2": "",
		"city": fake.city(),
		"state": fake.state_abbr(),
		"postcode": fake.postcode().split(" ")[0],
		"country": fake.country_code(),
		"email": email,
		"phone": fake.phone_number(),
	}
	shipping = {
		"first_name": first_name,
		"last_name": last_name,
		"company": "",
		"address_1": fake.street_address(),
		"address_2": "",
		"city": fake.city(),
		"state": fake.state_abbr(),
		"postcode": fake.postcode().split(" ")[0],
		"country": fake.country_code(),
	}

	return {
		"email": email,
		"first_name": first_name,
		"last_name": last_name,
		"username": username,
		"billing": billing,
		"shipping": shipping,
	}
