class Package:
    def __init__(self, id, address, deadline, city, state, zipcode, weight, status):
        self.id = id
        self.address = address
        self.deadline = deadline
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.weight = weight
        self.status = status
        self.start_time = None
        self.end_time = None
        self.truck_id = None

    def __str__(self) -> str:
        return ("Package id: " + str(self.id)
                + "\nAddress: " + str(self.address)
                + ", Deadline: " + str(self.deadline)
                + ", City: " + str(self.city)
                + ", Zipcode: " + str(self.zipcode)
                + ", Weight: " + str(self.weight)
                + "\nStatus: " + str(self.status)
                + ", Departure at: " + str(self.start_time)
                + ", ETA: " + str(self.end_time))