from simulator.batgraph import BatGraph
from simulator.batmobile import BatMobile


class Simulation:
    dt = 1e-5

    def __init__(self) -> None:
        super().__init__()
        self.batgraph = BatGraph()
        self.batmobile = BatMobile()
        self.totalTimeElapsed = 0

    def iterate(self):
        self.totalTimeElapsed += self.dt
