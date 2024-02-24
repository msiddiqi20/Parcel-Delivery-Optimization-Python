from datetime import time, datetime, timedelta
from PDO_UPS.driver import Driver
from PDO_UPS.graph import Graph
from PDO_UPS.hashmap import Hashmap
from PDO_UPS.package import Package
from PDO_UPS.truck import Truck
from PDO_UPS.vertex import Vertex


def openfile(file_location):
    file = open(file_location, "r")
    return file


# Take addresses from the csv file and create vertices of each deliverable address.
def initialize_vertices(vertex_list):
    addresses_data = open("../data/addresses.csv")

    for line in addresses_data.readlines():
        vertex_id, name, address, city, state, zipcode = line.split(",")
        zipcode = zipcode.replace("\n", "")
        vertex_list.append(Vertex(vertex_id, name, address, city, state, zipcode))


# Create a graph representation of the deliverable addresses and use an adjacency matrix to represent the graph edges.
def initialize_graph(graph, vertex_list):
    for vertex in vertex_list:
        graph.add_vertex(vertex)

    edges_data = openfile("../data/distances.csv")
    row_pointer = 1

    for line in edges_data.readlines():

        distances = line.split(",")

        for column_number in range(row_pointer):
            distance = distances[column_number]
            column_pointer = column_number + 1
            graph.add_edge(row_pointer, column_pointer, distance)

        row_pointer = row_pointer + 1


# Initialize all packages that are to be delivered for the day.
def initialize_packages(packages):
    package_data = openfile("../data/packages.csv")

    for line in package_data.readlines():
        package_id, address, city, state, zipcode, delivery_deadline, mass, special_notes = line.split(",")
        special_notes = special_notes.replace("\n", "")

        if special_notes == "":
            special_notes = "None"

        packages.add(int(package_id),
                     Package(package_id, address, city, state, zipcode, delivery_deadline, mass, special_notes))


# Load the trucks with the packages assigned and update the packages status to "At the Hub"
def load_trucks(truck, truck_list, packages):
    for package_id in truck_list:
        truck.load_package(packages.get(package_id))
        packages.get(package_id).set_status("At the Hub", "08:00:00")


# Using the address of the packages loaded on the truck and the nearest neighbor algorithm to create a queue for
# today's deliveries.
def find_nearest_neighbor(truck, graph, mid_route_change=False):
    if truck.delivery_addresses:
        start_address = truck.current_location

        if not mid_route_change:
            truck.delivery_addresses.remove(truck.current_location)

        distances = []

        if truck.delivery_addresses:
            for next_possible_address in truck.delivery_addresses:
                distance = graph.check_distance(start_address, next_possible_address)
                distances.append((next_possible_address, float(distance)))

            distances.sort(key=lambda next_option: next_option[1])
            truck.queue.append(distances[0])

            truck.current_location = distances[0][0]
            find_nearest_neighbor(truck, graph, False)

        else:
            distance = graph.check_distance(start_address, "4001 South 700 East")
            truck.queue.append(("4001 South 700 East", float(distance)))
            truck.current_location = "4001 South 700 East"
    return


# Bind or assign the truck with a driver and update the status of all packages on the truck to "En Route"
def driver_truck_bind(driver, truck, packages, current_date_time):
    if driver.status == "Ready" and truck.packages_list:
        driver.status = "Working"

        for package in truck.packages_list:
            packages.get(package).set_status("En Route", current_date_time.time())


# Initialize all variables and use the above methods to prepare the trucks for delivery.
# Begin truck delivery and accommodate for all edge cases required for the day.
def main(final_time, total_mileage=False, single_package=0):
    # Initialize the deliverable addresses as vertices.
    vertices = []
    initialize_vertices(vertices)

    # Create a graph with all the vertices and edges.
    wgusps_graph = Graph()
    initialize_graph(wgusps_graph, vertices)

    # Initialize all the packages into a hashmap for storage.
    all_packages = Hashmap()
    initialize_packages(all_packages)

    # Initialize all the trucks that will be going out for delivery.
    truck1 = Truck(1)
    truck2 = Truck(2)
    truck3 = Truck(3)

    # Assign each truck a list of packages, and create a list of packages that are delayed on the flight.
    truck1_packages_list = [1, 4, 13, 14, 15, 16, 19, 20, 21, 27, 34, 35, 39, 40]
    truck2_packages_list = [3, 5, 8, 10, 11, 12, 18, 22, 23, 24, 29, 30, 36, 37, 38]
    truck3_packages_list = [2, 7, 9, 17, 26, 31, 33]
    delayed_packages_list = [6, 25, 28, 32]

    # Set the current time to 8:00 AM
    current_date_time = datetime.combine(datetime.now().date(), time(hour=8, minute=0, second=0))

    # Set the status of all delayed packages to delayed at 8:00 AM
    for delayed_package in delayed_packages_list:
        all_packages.get(delayed_package).set_status("Delayed", current_date_time.time())

    # Load the trucks with the packages assigned
    load_trucks(truck1, truck1_packages_list, all_packages)
    load_trucks(truck2, truck2_packages_list, all_packages)
    load_trucks(truck3, truck3_packages_list, all_packages)

    # Using the nearest neighbor algorithm to create a queue of addresses as a route for the truck to take.
    find_nearest_neighbor(truck1, wgusps_graph)
    find_nearest_neighbor(truck2, wgusps_graph)

    # Initialize the drivers working today.
    driver1 = Driver(1)
    driver2 = Driver(2)

    # Assign and bind the driver to his truck and set the status of all packages on that truck to "En Route".
    driver_truck_bind(driver1, truck1, all_packages, current_date_time)
    driver_truck_bind(driver2, truck2, all_packages, current_date_time)

    # Initialize conditions for delivery and edge cases.
    condition_not_met = True

    truck1_moving = True
    truck2_moving = True
    truck3_moving = False

    truck1_at_stop = True
    truck2_at_stop = True
    truck3_at_stop = True

    delayed_packages_arrived = False
    upcoming_address_correction = False

    # Using a while loop and conditions initialized above, start the truck delivery and end them when all
    # deliveries have been made or when the time has run out. Prints the status of a package or packages after.
    while condition_not_met:

        if str(current_date_time.time()) == "09:05:00":
            load_trucks(truck3, delayed_packages_list, all_packages)
            find_nearest_neighbor(truck3, wgusps_graph)
            delayed_packages_arrived = True
            upcoming_address_correction = True

        if truck1_moving:

            if truck1_at_stop and truck1.queue:
                if truck1.current_location != "4001 South 700 East":
                    packages_at_address = truck1.package_hashmap.get(truck1.current_location)

                    for packages in packages_at_address:
                        all_packages.get(packages).set_status("Delivered", current_date_time.time())

                truck1.next_location, traveling_distance = truck1.queue.popleft()
                truck1.traveling_distance = float(traveling_distance) + truck1.mileage
                truck1_at_stop = False

            if not truck1_at_stop and truck1.mileage >= truck1.traveling_distance:
                truck1.current_location = truck1.next_location

                if truck1.current_location != "4001 South 700 East":
                    packages_at_address = truck1.package_hashmap.get(truck1.current_location)

                    for packages in packages_at_address:
                        all_packages.get(packages).set_status("En Route", current_date_time.time())

                else:
                    truck1_moving = False

                # print(f"Truck 1: {truck1.current_location} | Mileage: {truck1.mileage} | Time: {current_date_time.time()}")
                truck1_at_stop = True

        if delayed_packages_arrived and not truck1_moving:
            driver1.status = "Ready"
            driver_truck_bind(driver1, truck3, all_packages, current_date_time)
            delayed_packages_arrived = False
            truck3_moving = True

        if truck2_moving:

            if truck2_at_stop and truck2.queue:
                if truck2.current_location != "4001 South 700 East":
                    packages_at_address = truck2.package_hashmap.get(truck2.current_location)

                    for packages in packages_at_address:
                        all_packages.get(packages).set_status("Delivered", current_date_time.time())

                truck2.next_location, traveling_distance = truck2.queue.popleft()
                truck2.traveling_distance = float(traveling_distance) + truck2.mileage
                truck2_at_stop = False

            if not truck2_at_stop and truck2.mileage >= truck2.traveling_distance:
                truck2.current_location = truck2.next_location

                if truck2.current_location != "4001 South 700 East":
                    packages_at_address = truck2.package_hashmap.get(truck2.current_location)

                    for packages in packages_at_address:
                        all_packages.get(packages).set_status("En Route", current_date_time.time())

                else:
                    truck2_moving = False

                # print(f"Truck 2: {truck2.current_location} | Mileage: {truck2.mileage} | Time: {current_date_time.time()}")
                truck2_at_stop = True

        if truck3_moving:

            if truck3_at_stop and upcoming_address_correction and current_date_time.time() >= datetime.strptime(
                    "10:20:00", "%H:%M:%S").time():
                current_location_of_truck3 = truck3.current_location
                wrong_address_package = all_packages.get(9)
                wrong_address_package.address = "410 S State St"
                wrong_address_package.city = "Salt Lake City"
                wrong_address_package.state = "UT"
                wrong_address_package.zipcode = "84111"

                truck3.package_hashmap.add("410 S State St", [9])

                packages_left = []

                while truck3.queue:
                    address, distance = truck3.queue.popleft()
                    if address != "4001 South 700 East":
                        packages_left = packages_left + truck3.package_hashmap.get(address)

                for package_id in packages_left:
                    package = all_packages.get(package_id)
                    truck3.delivery_addresses.add(package.address)

                find_nearest_neighbor(truck3, wgusps_graph, True)
                truck3.current_location = current_location_of_truck3
                upcoming_address_correction = False

            if truck3_at_stop and truck3.queue:
                if truck3.current_location != "4001 South 700 East":
                    packages_at_address = truck3.package_hashmap.get(truck3.current_location)

                    for packages in packages_at_address:
                        all_packages.get(packages).set_status("Delivered", current_date_time.time())

                truck3.next_location, traveling_distance = truck3.queue.popleft()
                truck3.traveling_distance = float(traveling_distance) + truck3.mileage
                truck3_at_stop = False

            if not truck3_at_stop and truck3.mileage >= truck3.traveling_distance:
                truck3.current_location = truck3.next_location

                if truck3.current_location != "4001 South 700 East":
                    packages_at_address = truck3.package_hashmap.get(truck3.current_location)

                    for packages in packages_at_address:
                        all_packages.get(packages).set_status("En Route", current_date_time.time())

                else:
                    truck3_moving = False

                # print(f"Truck 3: {truck3.current_location} | Mileage: {truck3.mileage} | Time: {current_date_time.time()}")
                truck3_at_stop = True

        if current_date_time >= final_time:
            condition_not_met = False

        if not truck1_moving and not truck2_moving and not truck3_moving:
            if total_mileage:
                return truck1.mileage + truck2.mileage + truck3.mileage
            condition_not_met = False

        current_date_time = current_date_time + timedelta(seconds=1)

        if truck1_moving:
            truck1.mileage = truck1.mileage + 0.005
        if truck2_moving:
            truck2.mileage = truck2.mileage + 0.005
        if truck3_moving:
            truck3.mileage = truck3.mileage + 0.005

    if not total_mileage:
        if single_package != 0:
            print(all_packages.get(single_package))
        else:
            for package_id in range(1, 41):
                print(all_packages.get(package_id))


# User interface to use the program.
def cli():
    end_date_time = datetime.combine(datetime.now().date(), time(hour=12, minute=0, second=0))
    total_distance = main(end_date_time, True)

    print("-" * 100)
    print(f"{'Western Governors University Postal Service':^100}")
    print(f"{f'The route was completed in: {total_distance:.2f} Miles':^100}")
    print("-" * 100)

    print(f"{'Please select an option below to begin:':^100}")
    print(f"{'  a) Information of all packages at a specified time':^100}")
    print(f"{'  b) Information of one package at a specified time':^100}")
    print(f"{'  q) Quit':^100}")

    print("\n")
    user_input = input(f"{'option: ':>50}")
    print("\n")

    while user_input not in "abq":
        print(f"{'The option you have entered is invalid! Please try again.':^100}")
        user_input = input(f"{'option: ':>50}")

    if user_input == "a":
        try:
            print("-" * 100)
            print(f"{'Please enter a time below to begin:':^100}")
            input_time = input(f"{'Time (HH:MM:SS): ':>50}")
            hours, minutes, seconds = input_time.split(":")
            selected_time = time(int(hours), int(minutes), int(seconds))
            selected_date_time = datetime.combine(datetime.now().date(), selected_time)
            print(f"\n{f'Time: {selected_time}':^100}")

            main(selected_date_time)

        except ValueError:
            print(f"{'The time you have entered is invalid! Please start again.':^100}")
            quit()

    elif user_input == "b":
        try:
            print("-" * 100)
            print(f"{'Please enter the desired package id:':^100}")
            input_package_id = int(input(f"{'Package ID: ':>50}"))
            print("\n")

            while input_package_id not in range(1, 41):
                print(f"{'The package id you have entered is invalid! Please try again.':^100}")
                input_package_id = int(input(f"{'Package ID: ':>50}"))

            print(f"{'Please enter the time to check:':^100}")
            input_time = input(f"{'Time (HH:MM:SS): ':>50}")
            hours, minutes, seconds = input_time.split(":")
            selected_time = time(int(hours), int(minutes), int(seconds))
            selected_date_time = datetime.combine(datetime.now().date(), selected_time)
            print(f"\n{f'Time: {selected_time}':^100}")

            main(selected_date_time, False, input_package_id)

        except IndexError:
            print(f"{'The time you have entered is invalid! Please start again.':^100}")
            quit()

    else:
        quit()


cli()
