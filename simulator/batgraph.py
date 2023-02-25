import math

import networkx
import networkx.classes.graph


class BatGraph(networkx.classes.graph.Graph):
    @staticmethod
    def justASingleLine():
        graph = BatGraph()
        graph.add_node("A", lat=60, long=200, charger=False)
        graph.add_node("B", lat=900, long=300, charger=False)
        graph.add_edge("A", "B")
        graph.storeEdgeAirlineDistances()
        return graph

    @staticmethod
    def exampleGraph():
        graph = BatGraph()
        graph.add_node("A", lat=60, long=100, charger=False)
        graph.add_node("B", lat=380, long=60, charger=False)
        graph.add_node("C", lat=150, long=360, charger=True)
        graph.add_node("D", lat=650, long=150, charger=False)
        graph.add_node("E", lat=400, long=470, charger=False)
        graph.add_node("F", lat=700, long=500, charger=False)
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

    def airlineDistance(self, A, B):
        """Returns airline distance (heuristic) between A and B."""
        dx = self.nodes[A]["lat"] - self.nodes[B]["lat"]
        dy = self.nodes[A]["long"] - self.nodes[B]["long"]
        return math.hypot(dx, dy)

    def storeEdgeAirlineDistances(self):
        """Computes airline distances and stores them."""
        for A, B in self.edges():
            self.edges[A, B]["distance"] = self.airlineDistance(A, B)

    def findShortestPath(self, source, destination):
        """Determine the literal shortest path from source to target, in terms of distance."""
        return networkx.algorithms.shortest_paths.astar_path(self, source, destination, heuristic=self.airlineDistance)
