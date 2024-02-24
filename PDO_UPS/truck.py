from collections import deque
from PDO_UPS.hashmap import Hashmap


class Truck:

    def __init__(self, truck_id):
        self.truck_id = int(truck_id)
        self.packages_list = []
        self.delivery_addresses = {"4001 South 700 East"}
        self.package_hashmap = Hashmap()
        self.queue = deque([])
        self.current_location = "4001 South 700 East"
        self.next_location = ""
        self.mileage = 0
        self.average_speed = 18
        self.maximum_capacity = 16

    def load_package(self, package):
        self.packages_list.append(package.package_id)
        self.delivery_addresses.add(package.address)

        if self.package_hashmap.get(package.address) is None:
            self.package_hashmap.add(package.address, [package.package_id])
        else:
            package_id_list = self.package_hashmap.get(package.address)
            package_id_list.append(package.package_id)
            self.package_hashmap.add(package.address, package_id_list)
