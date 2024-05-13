class Address:
    def __init__ (self, id, name, address):
        self.id = id
        self.address = address
        self.name = name

    def __str__(self) -> str:
        return "Address: " + str(self.id) + "," + str(self.name) + "," + str(self.address)