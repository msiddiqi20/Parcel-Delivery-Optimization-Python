# University Parcel Service (UPS) Routing Program

## Project Overview

This project aims to optimize the delivery routes for the University Parcel Service (UPS) in Salt Lake City. The program ensures timely delivery of 40 packages while minimizing travel distances, using advanced data structures and a custom implementation of the Nearest Neighbor algorithm.

## Files

### Scripts
- **driver.py**: Defines the `Driver` class, managing driver information and status.
- **hashmap.py**: Implements a custom hash table for efficient data storage and retrieval.
- **package.py**: Defines the `Package` class, containing delivery details for each package.
- **graph.py**: Manages the graph data structure for storing delivery routes and locations.
- **truck.py**: Defines the `Truck` class, handling package loading and route assignment.
- **vertex.py**: Represents delivery locations as vertices in the routing graph.
- **main.py**: Coordinates the overall program logic and user interactions.

### Data Files
- **addresses.csv**: Contains delivery addresses and location details.
- **distances.csv**: Represents the distance matrix between delivery points.
- **packages.csv**: Lists package details including ID, address, deadline, and weight.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/msiddiqi20/Parcel-Delivery-Optimization-Python.git
   ```
2. Navigate to the project directory:
   ```bash
   cd UPS-routing-program
   ```
3. Ensure you have Python 3 installed.

## Usage

1. Prepare the data files (`addresses.csv`, `distances.csv`, `packages.csv`) and place them in the project directory.
2. Run the main script to start the program:
   ```bash
   python main.py
   ```

## Program Overview

### Algorithm

The Nearest Neighbor algorithm is used to find the most efficient route:

- **Start**: Select a starting location.
- **Find Nearest**: Locate the nearest unvisited location and travel there.
- **Repeat**: Check for any remaining unvisited locations and repeat the process.
- **Return**: Once all locations are visited, return to the starting point.

Reference: Nilsson, 2003, p.1

### Data Structures
- **Custom Hash Table**: Efficiently stores and retrieves package data.
- **Graph**: Represents delivery routes and locations, facilitating the Nearest Neighbor algorithm.

### Features
- **Route Optimization**: Ensures all 40 packages are delivered on time.
- **Custom Data Structures**: Efficient storage and retrieval of package and delivery data.
- **User Interface**: Allows monitoring of package status, delivery times, and overall truck mileage.

## Screenshots

### Package Status
- Between 8:35 a.m. and 9:25 a.m.
- Between 9:35 a.m. and 10:25 a.m.
- Between 12:03 p.m. and 1:12 p.m.

### Completion
- Total mileage traveled by all trucks.

## Justification

### Algorithm
- **Strengths**: Efficient route optimization, adaptable to various cities.
- **Alternative Algorithms**: Greedy algorithm, Genetic algorithm.
- **Potential Improvements**: Explore more advanced algorithms, implement real-time tracking.

### Data Structures
- **Efficiency**: Hash table provides constant time look-up (O(1)), suitable for large datasets.
- **Scalability**: Space usage scales linearly with the number of packages.
- **Impact of Changes**: Increasing trucks or cities affects look-up time and space usage.

## Future Improvements

- **Algorithm Enhancement**: Integrating more sophisticated routing algorithms to optimize delivery times and distances further.
- **Data Structure Optimization**: Improving the hash function to reduce the time complexity of hash map operations.

## References

Nilsson, C. (2003). "Heuristics for the Traveling Salesman Problem."
