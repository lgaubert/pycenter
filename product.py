class Product:
    def __init__(self, name, price, display_id, location):
        self.name = name
        self.price = price
        self.display_id = display_id
        self.location = location

    def display_info(self):
        print(f"Name: {self.name}")
        print(f"Price: {self.price}")
        print(f"Display ID: {self.display_id}")
        print(f"Location: {self.location}")