import math
import random

import networkx
import networkx.algorithms.shortest_paths as shortest_paths
import networkx.classes.graph
import osmnx


class BatGraph(networkx.classes.graph.Graph):
    @staticmethod
    def justASingleLine():
        graph = BatGraph()
        graph.add_node("A", x=60, y=200, charger=False)
        graph.add_node("B", x=900, y=300, charger=False)
        graph.add_edge("A", "B")
        graph.storeEdgeAirlineDistances()
        return graph

    @staticmethod
    def exampleGraph():
        graph = BatGraph()
        graph.add_node("A", x=60, y=100, charger=False)
        graph.add_node("B", x=380, y=60, charger=False)
        graph.add_node("C", x=150, y=360, charger=True)
        graph.add_node("D", x=650, y=150, charger=False)
        graph.add_node("E", x=400, y=470, charger=False)
        graph.add_node("F", x=700, y=500, charger=False)
        graph.add_edge("A", "B")
        graph.add_edge("A", "C")
        graph.add_edge("B", "C")
        graph.add_edge("B", "D")
        graph.add_edge("C", "D")
        graph.add_edge("C", "E")
        graph.add_edge("D", "E")
        graph.add_edge("D", "F")
        graph.add_edge("E", "F")
        graph.storeEdgeAirlineDistances()
        return graph

    @staticmethod
    def fetch(locality="Oxford, Oxfordshire, England, United Kingdom"):
        """Using the OpenStreetMap API, fetch some real-world street data."""
        graph = osmnx.graph_from_place(locality, network_type="drive")
        return graph

    def airlineDistance(self, A, B):
        """Returns airline distance (heuristic) between A and B."""
        dx = self.nodes[A]["x"] - self.nodes[B]["x"]
        dy = self.nodes[A]["y"] - self.nodes[B]["y"]
        return math.hypot(dx, dy)

    def storeEdgeAirlineDistances(self):
        """Computes airline distances and stores them."""
        for A, B in self.edges():
            self.edges[A, B]["distance"] = self.airlineDistance(A, B)

    def findShortestPath(self, source, destination) -> tuple:
        """Determine the literal shortest path from source to target, in terms of distance."""
        return tuple(shortest_paths.astar_path(self, source, destination, heuristic=self.airlineDistance))

    def perturbRoute(self, route: tuple) -> tuple:
        """Return a type-1, type-2 or type-3 perturbation of a given path.
        type-1: turn one edge into two edges -> route length increases by one
        type-2: replace one node along the route with another adjacent one -> route length stays the same
        type-3: the destination becomes part of the perturbation so the route is shortened
        """
        i = random.randrange(0, len(route))
        j = random.choice([x for x in (i + 1, i + 2, i - 1, i - 2) if 0 <= x < len(route)])
        indexA, indexB = min(i, j), max(i, j)
        nodeA, nodeB = route[indexA], route[indexB]
        sharedNeighbours = set(self.neighbors(nodeA)).intersection(self.neighbors(nodeB))
        if indexB - indexA == 2:  # type-2 perturbation
            inbetween = route[indexA + 1]
            sharedNeighbours.remove(inbetween)  # ignore the element that is already part of the route
        middle = sharedNeighbours.pop()
        if middle == route[-1]:  # type-3 perturbation, destination is perturbed in
            return route[: indexA + 1] + (middle,)  # so ignore the remaining route (which will be a loop)
        return route[: indexA + 1] + (middle,) + route[indexB:]  # choose any shared neighbour
