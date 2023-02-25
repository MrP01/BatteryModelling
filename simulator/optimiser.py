import math
import random
from simulator.simulation import Simulation


class Optimiser:
    def __init__(self) -> None:
        self.simulator = Simulation()
        self.testedRoutes = {}
        self.temperature = 1.0
        self.route = self.simulator.batgraph.findShortestPath("A", "F")
        self.measureRoute(self.route)

    def metric(self):
        """Metric to minimise for."""
        return self.simulator.totalTimeElapsed

    def measureRoute(self, route):
        self.simulator.reset()
        self.simulator.runOnPath(route, lambda t, soc: 1)
        self.testedRoutes[route] = self.metric()
        return self.testedRoutes[route]

    def mcmcStep(self):
        """Perform a Monte-Carlo Markov-Chain, Metropolis-Hastings iteration step."""
        while True:
            try:
                newRoute = self.simulator.batgraph.perturbRoute(self.route)
                if newRoute not in self.testedRoutes:
                    break
            except KeyError:  # perturbRoute() was unsuccessful
                continue

        delta = self.measureRoute(newRoute) - self.testedRoutes[self.route]
        acceptanceProbability = min(1, math.exp(-delta / self.temperature))
        if random.random() < acceptanceProbability:
            self.route = newRoute
            print(f"Accepted new route {newRoute} with delta: {delta}.")
        else:
            print(f"Rejected route {newRoute} with delta: {delta}.")
