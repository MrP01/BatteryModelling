from typing import Optional


class BatMobile:
    def __init__(self):
        self.position: float = 0  # x
        self.velocity: float = 0  # v
        self.acceleration: float = 0  # a
        self.sourceNode: Optional[str] = None
        self.destinationNode: Optional[str] = None

    def accelerate(self, amount):
        print("Accelerating BatMobile by", amount)
        self.acceleration += amount

    def halt(self):
        self.acceleration = 0
        self.velocity = 0

    def iterate(self):
        self.velocity += self.acceleration
        self.position += self.velocity
