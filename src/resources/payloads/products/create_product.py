from src.utils.faker_config import product_payload


def build_create_product_payload(name: str | None = None) -> dict:
	"""Return a payload ready to send to the API for creating a product."""
	return product_payload(name=name)

def product_image_scenarios():
    """Return list of image scenarios for product creation tests."""
    return [
        {
            "title": "Imagen valida en linea",
            "images": [{"src": "https://media.istockphoto.com/id/458068097/es/foto/adidas-superstar.jpg?s=612x612&w=0&k=20&c=yDNrjCvCVD0ZT7Hf8bzR9sIXxRdbYmNTyWMG41ei3qc="}],
            "expected_status": 201,
        },
        {
            "title": "Imagen con ID existente en biblioteca",
            "images": [{"id": 286}], 
            "expected_status": 201,
        },
        {
            "title": "Multiples imagenes validas (id + src)",
            "images": [
                {"id": 289},
                {"src": "https://brand.assets.adidas.com/image/upload/f_auto,q_auto:best,fl_lossy/02_originals_ss25_the_original_introduce_plp_the_original_iwp_samba_d_b5c4eebc15.jpg"},
            ],
            "expected_status": 201,
        },
        {
            "title": "Imagen con ID inexistente",
            "images": [{"id": 999999}],
            "expected_status": 400,
        },
        {
            "title": "URL inexistente",
            "images": [{"src": "https://example.com/no-existe.png"}],
            "expected_status": 400,
        },
        {
            "title": "URL de GIF en vez de imagen estatica",
            "images": [{"src": "https://i.pinimg.com/originals/f8/9c/7a/f89c7afa37963067c7a90abb49ca72ed.gif"}],
            "expected_status": 201,
        },
        {
            "title": "Enlace de pagina web en vez de imagen",
            "images": [{"src": "https://ar.pinterest.com/pin/908742031052491072/"}],
            "expected_status": 400,
        },
        {
			"title": "Campo imagenes vacio",
			"images": [],
			"expected_status": 201,
		},
        {
			"title": "Enlace de video en vez de imagen",
			"images": [{"src": "https://www.w3schools.com/html/mov_bbb.mp4"}],
			"expected_status": 400,
		}
    ]
