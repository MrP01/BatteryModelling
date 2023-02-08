class BatMobile:
    def __init__(self) -> None:
        self.position = 0  # x
        self.velocity = 0  # v
        self.acceleration = 0  # a

    def accelerate(self, amount):
        self.acceleration += amount
