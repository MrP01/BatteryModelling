from simulator.batgraph import BatGraph
from simulator.batmobile import BatMobile


class Simulation:
    dt = 1e-2

    def __init__(self):
        super().__init__()
        self.batgraph = BatGraph.exampleGraph()
        self.batmobile = BatMobile()
        self.batmobile.sourceNode = "A"
        self.batmobile.destinationNode = "B"
        self.step = 0
        self.totalTimeElapsed = 0

    def iterate(self):
        self.batmobile.iterate(self.dt)
        self.totalTimeElapsed += self.dt
        self.step += 1
