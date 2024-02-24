from PDO_UPS.hashmap import Hashmap
from PDO_UPS.vertex import Vertex


class Graph:

    def __init__(self):
        self.adjacency_matrix = [[]]
        self.vertex_address_hashmap = Hashmap()
        self.vertex_id_hashmap = Hashmap()
        self.rows = 1
        self.columns = 1

    def add_vertex(self, vertex):

        if isinstance(vertex, Vertex):

            if self.vertex_id_hashmap.get(vertex.vertex_id) is None:
                self.vertex_id_hashmap.add(vertex.vertex_id, vertex)
                self.vertex_address_hashmap.add(vertex.address, vertex.vertex_id)

                for each_row in self.adjacency_matrix:
                    each_row.append(0)

                self.columns += 1

                self.adjacency_matrix.append([0] * self.columns)

                self.rows += 1

    def add_edge(self, start_id, end_id, distance):
        row_index = int(start_id) - 1
        column_index = int(end_id) - 1
        distance = float(distance)

        self.adjacency_matrix[row_index][column_index] = distance
        self.adjacency_matrix[column_index][row_index] = distance

    def check_distance(self, start_address, end_address):
        row_index = self.vertex_address_hashmap.get(start_address) - 1
        column_index = self.vertex_address_hashmap.get(end_address) - 1

        return self.adjacency_matrix[row_index][column_index]
