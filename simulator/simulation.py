"""The main simulator class, representing the simulation layer.
At some point this should be runnable individually.

To run,

simulation = Simulation()
simulation.run(60)
"""
from typing import List

from simulator.batgraph import BatGraph
from simulator.batmobile import BatMobile


class Simulation:
    """A singleton simulation class that stores all state variables within its properties."""

    dt = 0.01

    def __init__(self):
        super().__init__()
        self.batgraph = BatGraph.exampleGraph()
        self.reset()

    def reset(self):
        self.batmobile = BatMobile()
        self.batmobile.sourceNode = "A"
        self.batmobile.destinationNode = "B"
        self.totalTimeElapsed = 0
        self.step = 0

    def iterate(self):
        """The main iteration representing a single time-step forwards.
        Passes further details on to batmobile and battery.
        """
        if self.batmobile.position >= self.batgraph.edges[self.currentEdge()]["distance"]:
            self.turnBatMobile()

        self.batmobile.iterate(self.dt)
        self.totalTimeElapsed += self.dt
        self.step += 1

    def run(self, stoppingTime):
        """Main function of the simulation, when used without an interface."""
        while self.totalTimeElapsed < stoppingTime:
            self.iterate()

    def runOnPath(self, destination: str, turningIndices: List[int], current):
        """Simulates the car driving on a given path.
        Can be used to obtain some goal metric (i.e. totalTimeElapsed) and minimise that over the inputs.
        Could in turn be used for a Monte Carlo simulation to find the optimal path
        over a subset of paths as predetermined by A-star.
        """
        self.chooseTurnIndex = lambda: turningIndices.pop(0)
        while self.batmobile.sourceNode != destination:
            self.batmobile.battery.current = current(self.totalTimeElapsed, self.batmobile.battery.soc)
            self.iterate()

    def chooseTurnIndex(self):
        print("Turned at the next best corner")
        return 0

    def getOnwardDestinations(self):
        connectedEdges = [edge[1] for edge in self.batgraph.edges(self.batmobile.destinationNode)]
        connectedEdges.remove(self.batmobile.sourceNode)
        return connectedEdges

    def turnBatMobile(self):
        destNode = self.batmobile.destinationNode
        self.batmobile.destinationNode = self.getOnwardDestinations()[self.chooseTurnIndex()]
        self.batmobile.sourceNode = destNode
        self.batmobile.position = 0
        if self.batgraph.nodes[destNode]["charger"]:
            self.batmobile.chargeUp()

    def currentEdge(self):
        return (self.batmobile.sourceNode, self.batmobile.destinationNode)
