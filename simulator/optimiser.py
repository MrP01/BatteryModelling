import math
import random
from simulator.simulation import Simulation


class Optimiser:
    def __init__(self, locality="Jericho, Oxfordshire, England, United Kingdom") -> None:
        self.simulator = Simulation(locality)
        self.testedRoutes = {}
        self.temperature = 1.0

    def initialise(self, source, destination):
        """Simulates (measures) the shortest possible route, ignoring charging stations, etc."""
        self.route = self.simulator.batgraph.findShortestPath(source, destination)
        self.measureRoute(self.route)

    def metric(self):
        """Metric to minimise for."""
        return self.simulator.totalTimeElapsed

    def measureRoute(self, route):
        """Test out a given route in the simulator."""
        self.simulator.reset()
        self.simulator.runOnPath(route, lambda t, soc: 1)
        self.testedRoutes[route] = self.metric()
        return self.testedRoutes[route]

    def mcmcStep(self):
        """Perform a Monte-Carlo Markov-Chain, Metropolis-Hastings iteration step."""
        perturbationAttempt = 0
        while True:
            try:
                # print("Perturbing...")
                newRoute = self.simulator.batgraph.perturbRoute(self.route)
                if newRoute not in self.testedRoutes:
                    break
            except KeyError:  # perturbRoute() was unsuccessful
                pass
            perturbationAttempt += 1
            if perturbationAttempt > 20:
                print("Giving up perturbation.")
                return

        # negative delta is good!!
        delta = self.measureRoute(newRoute) - self.testedRoutes[self.route]
        acceptanceProbability = min(1, math.exp(-delta / self.temperature))
        if random.random() < acceptanceProbability:
            self.route = newRoute
            print(f"Accepted new route {newRoute} with delta: {delta:.2f}. Total: {self.testedRoutes[newRoute]:.2f}.")
        else:
            print(f"Rejected route {newRoute} with delta: {delta:.2f}.")
