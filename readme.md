# University Parcel Service Routing Program

## Project Overview

This GitHub repository contains the source code for the University Parcel Service Routing Program, designed to optimize delivery routes for the University Parcel Service. The program ensures timely delivery of packages while minimizing travel distances, using advanced data structures and a custom implementation of the Nearest Neighbor algorithm.

## Files

- **Scripts**

  - `driver.py`: Main execution script that initiates the routing logic.
  - `hashmap.py`: Manages the hash table for efficient data storage and retrieval.
  - `package.py`: Defines the Package class with relevant delivery details.
  - `graph.py`: Handles the graph data structure for storing delivery routes and locations.
  - `truck.py`: Manages truck objects including loading and route assignment.
  - `vertex.py`: Represents delivery locations as vertices in the routing graph.
  - `main.py`: Coordinates the overall program logic and user interactions.
 
- **Data Files**
  - `addresses.csv`, `distances.csv`, `packages.csv` – Contain the logistical data essential for route planning and package management.

## Algorithm Overview

The Nearest Neighbor algorithm is used to find the most efficient route:

- **Start**: Select a starting location.
- **Find Nearest**: Locate the nearest unvisited location and travel there.
- **Repeat**: Check for any remaining unvisited locations and repeat the process.
- **Return**: Once all locations are visited, return to the starting point.

Reference: Nilsson, 2003, p.1

## Pseudocode

```plaintext
distance_traveled = 0

def nearest_neighbor_algorithm(current_location, locations_list):
    while len(locations_list) > 0:
        selected_starting_location = current_location
        locations_list.remove(current_location)
        distances_to_each_location = {}
        list_of_possible_distances = []

        for next_possible_location in locations_list:
            distance = distance_between(current_location, next_possible_location)
            distances_to_each_location[distance] = next_possible_location
            list_of_possible_distances.append(distance)

        list_of_possible_distances.sort()
        shortest_distance = list_of_possible_distances[0]
        next_location = distances_to_each_location.get(shortest_distance)
        distance_traveled += shortest_distance
        nearest_neighbor_algorithm(next_location, locations_list)

    return distance_traveled
```

## Data Structures

### Hash Map

A hash map is used extensively throughout the program for quick data retrieval and storage, optimizing both performance and maintainability.

### Graph

A graph data structure represents the network of delivery routes, with vertices as delivery locations and edges as possible routes between them.

## Features

- **Efficient Routing**: Ensures all packages are delivered within the constraints using the Nearest Neighbor algorithm.
- **Scalability**: Handles an increasing number of packages and delivery locations effectively.
- **User Interface**: Provides real-time updates on package status and truck locations.

## Usage

Run the `driver.py` file to start the program. Interact through the CLI to monitor delivery status or simulate different delivery scenarios.


## Future Improvements

- **Algorithm Enhancement**: Integrating more sophisticated routing algorithms to optimize delivery times and distances further.
- **Data Structure Optimization**: Improving the hash function to reduce the time complexity of hash map operations.

## References

- Nilsson, C. (2003). "Heuristics for the Traveling Salesman Problem."

## Author

Muhammad Siddiqi
