"""The main simulator class, representing the simulation layer.
At some point this should be runnable individually.

To run,

simulation = Simulation()
simulation.runMe(60)
"""
from simulator.batgraph import BatGraph
from simulator.batmobile import BatMobile


class Simulation:
    """A singleton simulation class that stores all state variables within its properties."""

    dt = 0.01

    def __init__(self):
        super().__init__()
        self.batgraph = BatGraph.exampleGraph()
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
            print("Simulator also recognised...")
            self.turnBatMobile()

        self.batmobile.iterate(self.dt)
        self.totalTimeElapsed += self.dt
        self.step += 1

    def runMe(self, stoppingTime):
        """Main function of the simulation, when used without an interface."""
        while self.totalTimeElapsed < stoppingTime:
            self.iterate()

    def chooseTurnIndex(self):
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

    def currentEdge(self):
        return (self.batmobile.sourceNode, self.batmobile.destinationNode)
