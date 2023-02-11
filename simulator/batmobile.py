class BatMobile:
    def __init__(self):
        self.position = 0  # x
        self.velocity = 0  # v
        self.acceleration = 0  # a

    def accelerate(self, amount):
        print("Accelerating BatMobile by", amount)
        self.acceleration += amount

    def halt(self):
        self.acceleration = 0
        self.velocity = 0

    def iterate(self):
        self.velocity += self.acceleration
        self.position += self.velocity
