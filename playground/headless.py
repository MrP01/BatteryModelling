import numpy as np
from simulator.batmobile import BatMobile


class headless:
    dt = 0.01

    def __init__(self):
        super().__init__()
        self.totalTimeElapsed = 0
        self.step = 0
        self.batmobile = BatMobile()
        self.totalTimeElapsed = 0
        self.step = 0

    def iterate(self):
        """The main iteration representing a single time-step forwards.
        Passes further details on to batmobile and battery.
        """
        self.batmobile.iterate(self.dt)
        print(self.batmobile.battery.measurement().soc)
        # print(self.batmobile.battery.soc)
        # print(self.batmobile.battery.t)
        self.totalTimeElapsed += self.dt
        self.step += 1

    def runMe(self, stoppingTime):
        """Main function of the simulation, when used without an interface."""
        while self.totalTimeElapsed < stoppingTime:
            print(self.totalTimeElapsed)
            if 0 < self.totalTimeElapsed < 1:
                self.batmobile.accelerate(self.batmobile.currentJump)
            self.iterate()


h = headless()
h.runMe(len(currentJumps) * h.dt)
##
currentProfile = np.arange(1, 10)
currentJumps = np.ediff1d(currentProfile)
