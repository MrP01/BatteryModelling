import math
import random

from simulator.simulation import Simulation


class Optimiser:
    def __init__(self, graph) -> None:
        self.simulator = Simulation(graph)
        self.testedRoutes = {}
        self.temperature = 1.0

    def initialise(self, source, destination) -> None:
        """Simulates (measures) the shortest possible route, ignoring charging stations, etc."""
        if not self.simulator.batgraph.has_node(source):
            source = int(source)
        if not self.simulator.batgraph.has_node(destination):
            destination = int(destination)
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

    def mcmcStep(self) -> None:
        """Perform a Monte-Carlo Markov-Chain, Metropolis-Hastings iteration step."""
        perturbationAttempt = 0
        while True:
            try:
                # print("Perturbing...")
                newRoute = self.simulator.batgraph.perturbRoute(self.route)
                if newRoute != self.route:
                    break
            except (KeyError, StopIteration):  # perturbRoute() was unsuccessful
                pass
            perturbationAttempt += 1
            if perturbationAttempt > 20:
                return

        # a negative delta is good!!
        newEnergy = self.measureRoute(newRoute) if newRoute not in self.testedRoutes else self.testedRoutes[newRoute]
        delta = newEnergy - self.testedRoutes[self.route]
        acceptanceProbability = min(1, math.exp(-delta / self.temperature))
        if random.random() < acceptanceProbability:
            self.route = newRoute
        else:
            pass
