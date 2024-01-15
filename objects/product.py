class Product:
    id = 0
    name = ""
    price = 0.0
    vendor_ids = []

    def __init__(self, product_id, name):
        self.id = product_id
        self.name = name
