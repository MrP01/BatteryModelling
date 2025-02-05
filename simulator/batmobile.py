from typing import Optional

from simulator.battery import Battery


class BatMobile:
    """Represents the battery car ("Bat-Mobile") driving on an edge of the BatGraph. Models everything."""

    accelerationPerWatt = 100
    friction = -120.0
    currentJump = 0.1

    def __init__(self) -> None:
        self.battery = Battery()

        self.position: float = 0  # meters
        self.velocity: float = 0  # meters / second
        self.acceleration: float = 0  # true acceleration that determines velocity. in meters / second².
        self.motorAcceleration: float = 0  # goal acceleration, positively affects the true acceleration
        self.dragAcceleration: float = self.friction  # acceleration caused by drag, negatively affects the true accel,

        self.P_motor: float = 0

        self.sourceNode: Optional[str] = None  # one of the nodes of the BatGraph
        self.destinationNode: Optional[str] = None  # another node of the BatGraph

    def iterate(self, dt) -> None:
        self.battery.iterate(dt)

        self.motorAcceleration = self.accelerationPerWatt * self.battery.voltage * self.battery.current
        self.simulateDrag()

        self.P_motor = self.battery.voltage * self.battery.current

        self.acceleration = self.motorAcceleration + self.dragAcceleration
        self.velocity += self.acceleration * dt
        self.velocity = max(self.velocity, 0)  # velocity is at least 0..
        self.position += self.velocity * dt

    def accelerate(self, currentIncrease) -> None:
        """Increases the current through the motor by the given amount in Amps,
        therefore accelerating the car based on battery output.
        """
        self.battery.current += currentIncrease

    def simulateDrag(self) -> None:
        """Computes the drag acceleration which increases with v²."""
        self.dragAcceleration = -6e-3 * self.velocity**2 + self.friction

    def halt(self) -> None:
        self.battery.current = 0
        self.velocity = 0

    def chargeUp(self) -> None:
        self.battery.soc = 1
