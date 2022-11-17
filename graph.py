from queue import PriorityQueue
from polygon import Point, Line, Polygon
from typing import List


class Graph:
    def __init__(self, num_of_verticles, edges):
        self.v = num_of_verticles
        self.edges = [[-1 for i in range(num_of_verticles)] for j in range(num_of_verticles)]
        for edge in edges:
            self.edges[edge[0]][edge[1]] = edge[2]
        self.visited = []

    def add_edge(self, point1, point2, weight):
        self.edges[point1][point2] = weight
        self.edges[point2][point1] = weight

    def dijkstra(self, start_vertex):
        D = {v:float('inf') for v in range(self.v)}
        D[start_vertex] = 0

        pq = PriorityQueue()
        pq.put((0, start_vertex))

        while not pq.empty():
            (dist, current_vertex) = pq.get()
            self.visited.append(current_vertex)

            for neighbor in range(self.v):
                if self.edges[current_vertex][neighbor] != -1:
                    distance = self.edges[current_vertex][neighbor]
                    if neighbor not in self.visited:
                        old_cost = D[neighbor]
                        new_cost = D[current_vertex] + distance
                        if new_cost < old_cost:
                            pq.put((new_cost, neighbor))
                            D[neighbor] = new_cost
        return D


# Class GraphBuilder find edges of our future graph
class GraphBuilder:
    def __init__(self, start: Point, end: Point, lines: List[Line]):
        self.start = start
        self.end = end
        self.lines = lines
        self.points = []
        self.edges = []
        self._get_all_points()
        self._get_graphs_edges()

    def _get_all_points(self):
        self.points.append(self.start)
        for line in self.lines:
            self.points.append(line.start)
        self.points.append(self.end)

    def _get_graphs_edges(self):
        # base line - line between two our main points
        indexes_of_points_on_base_line = []

        # Check if there are two points on base line
        for i in range(len(self.points[1: -1])):
            if Point.isOnTheSameLine(self.points[0], self.points[i+1], self.points[-1]):
                indexes_of_points_on_base_line.append(i+1)

        # Get all pairs of our points
        for i in range(len(self.points)):
            for j in range(len(self.points)):
                flag = False

                point_1 = self.points[i]
                point_2 = self.points[j]

                # Our points will be connected in graph if this conditions are false:
                # Two points are same
                # Two points not on the same edge of polygon
                # Line created through points intersect edges of polygon

                # Corner case: Line, connected start and end goes through two vertices of polygon
                # Corner case: Line goes through one of edges of polygon

                if point_1 == point_2:
                    flag = True

                # Check if line between two points intersect some edge
                for line in self.lines:

                    if line.is_intersect_with(Line(point_1, point_2)) and \
                       Line(point_1, point_2).is_intersect_with(line):
                        flag = True

                # Two points of polygon which not on same edge shouldn't be connected
                if (point_1 in self.points[1: -1] and point_2 in self.points[1: -1]) \
                        and Line(point_1, point_2) not in self.lines:
                    flag = True

                # if two points connected through third point, and not include some edge of polygon, don't connect them
                for point in self.points[1:-1]:
                    if (point_1, point_2) != (self.points[0], self.points[-1]) and \
                       Point.isOnTheSameLine(point_1, point, point_2) and Line(point_1, point) not in self.lines \
                       and Line(point, point_2) not in self.lines:
                        flag = True

                if len(indexes_of_points_on_base_line) == 2:
                    if (point_1, point_2) == (self.points[0], self.points[-1]) and \
                       Line(self.points[indexes_of_points_on_base_line[0]], self.points[indexes_of_points_on_base_line[1]]) not in self.lines:
                        flag = True

                # If there are no challenges - make connection
                if not flag:
                    self.edges.append([i, j, Line(point_1, point_2).length()])


class ShortestPathFinder:
    def __init__(self, start: Point, end: Point, lines: List[Line]):
        self.start = start
        self.end = end
        self.lines = lines

    def find_shortest_distance(self):
        graphBuilder = GraphBuilder(self.start, self.end, self.lines)
        graph = Graph(len(graphBuilder.points), graphBuilder.edges)
        return graph.dijkstra(0)


