class Truck:
    def __init__(self, id, packages, mileage, start_time):
        self.id = id
        self.packages = packages
        self.mileage = mileage
        self.start_time = start_time
        self.end_time = start_time

    def __str__(self):
        return "Truck id: " + str(self.id)