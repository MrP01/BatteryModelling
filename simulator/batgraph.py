import networkx
import networkx.classes.graph


class BatGraph(networkx.classes.graph.Graph):
    @staticmethod
    def justASingleLine():
        graph = BatGraph()
        graph.add_node("A")
        graph.add_node("B")
        graph.add_edge("A", "B")
        return graph
