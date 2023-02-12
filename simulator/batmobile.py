from typing import Optional

from simulator.battery import Battery


class BatMobile:
    """Represents the battery car ("Bat-Mobile") driving on an edge of the BatGraph. Models everything."""

    def __init__(self):
        self.battery = Battery()

        self.position: float = 0  # meters
        self.velocity: float = 0.1  # meters / second
        self.acceleration: float = 0  # true acceleration that determines velocity. in meters / second².
        self.motorAcceleration: float = 0  # goal acceleration, positively affects the true acceleration
        self.dragAcceleration: float = 0  # acceleration caused by drag, it negatively affects the true acceleration

        self.P_motor: float = 0

        self.sourceNode: Optional[str] = None  # one of the nodes of the BatGraph
        self.destinationNode: Optional[str] = None  # another node of the BatGraph

    def iterate(self, dt):
        self.battery.iterate(dt)

        dP_motor = self.battery.voltage * self.battery.current - self.P_motor
        self.motorAcceleration = (3 / (0.01 + self.velocity)) * (dP_motor / dt)
        self.simulateDrag()

        self.acceleration = self.motorAcceleration + self.dragAcceleration
        self.velocity += self.acceleration * dt
        self.velocity = max(self.velocity, 0)  # velocity is at least 0..
        self.position += self.velocity * dt

    def accelerate(self, currentIncrease):
        """Increases the current through the motor by the given amount in Amps,
        therefore accelerating the car based on battery output.
        """
        self.battery.current += currentIncrease

    def simulateDrag(self):
        """Computes the drag acceleration which increases with v²."""
        self.dragAcceleration = -1e-5 * self.velocity**2

    def halt(self):
        self.battery.current = 0
        self.velocity = 0
