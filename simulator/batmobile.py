from typing import Optional

from simulator.battery import Battery


class BatMobile:
    """Represents the battery car driving on an edge of the BatGraph. Models everything."""

    def __init__(self):
        self.position: float = 0  # meters
        self.velocity: float = 0  # meters
        self.acceleration: float = 0  # meters

        self.battery = Battery()

        self.sourceNode: Optional[str] = None
        self.destinationNode: Optional[str] = None

    def iterate(self):
        self.velocity += self.acceleration
        self.position += self.velocity
        self.battery.iterate()

    def accelerate(self, amount):
        self.acceleration += amount

    def halt(self):
        self.acceleration = 0
        self.velocity = 0
