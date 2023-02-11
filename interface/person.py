class Animal:
    def __init__(self, name, height, mass, colour):
        self.name = name
        self.height = height
        self.mass = mass
        self.colour = colour

    def shoutLoudly(self):
        print(f"Hi!!! I am {self.name} and my colour is {self.colour}, I am shouting!!")

    def grow(self, dh):
        self.height = self.height + dh
        print("I grew a bit")

    def __mul__(self, other: float):
        print("I am being multiplied.")
        new = Animal(
            name=f"{other} * {self.name}",
            height=self.height * other,
            mass=self.mass * other,
            colour=self.colour,
        )
        return new


class Bear(Animal):
    def __init__(self, name, height, mass):
        super().__init__(name, height, mass, colour="brown")

    def bearNoise(self):
        print("Peter you have beutiful eyes Ö.")


class IceBear(Bear):
    def __init__(self, name, height, mass):
        super().__init__(name, height, mass)
        self.colour = "white"

    def shoutLoudly(self):
        print("Does a jump")
        return super().shoutLoudly()


chloe = Animal("Chloe", 1.5, 50, "green")
kylie = Bear("Kylie", 1.1, 4)
hanna = IceBear("Hanna", 1.2, 20)
