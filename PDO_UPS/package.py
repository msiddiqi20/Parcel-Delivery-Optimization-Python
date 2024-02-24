class Package:

    def __init__(self, package_id, address, city, state, zipcode, delivery_deadline, mass, special_notes):
        self.package_id = int(package_id)
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.delivery_deadline = delivery_deadline
        self.mass = mass
        self.special_notes = special_notes
        self.current_status = ""
        self.status_time = ""

    def set_status(self, status, time):
        self.current_status = status
        self.status_time = str(time)

    def __str__(self):
        return f"""
        Package: {self.package_id} 
    
        Delivery Address: {self.address} | City: {self.city} | State: {self.state} | Zipcode: {self.zipcode}
        Delivery Deadline: {self.delivery_deadline} | Mass: {self.mass} | Special Notes: {self.special_notes}
        Satus: {self.current_status} at {self.status_time}
        """
