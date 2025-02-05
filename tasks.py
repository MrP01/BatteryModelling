import random
import sys

import invoke
import matplotlib.pyplot as plt
import numpy as np

from simulator.batgraph import BatGraph
from simulator.optimiser import Optimiser
from simulator.simulation import Simulation


@invoke.task()
def run_trial(ctx, model="lithium-ion") -> None:
    """Runs pybamm."""
    ctx.run(f"{sys.executable} playground/pybamm_trial.py {model}")


@invoke.task()
def run_simulation(ctx, name="current-bump-1.5A", T_max=6.0) -> None:
    """Runs the simulation for some given test setting."""
    simulation = Simulation()
    log = []
    while simulation.totalTimeElapsed < T_max:
        simulation.batmobile.battery.current = (
            8 * simulation.totalTimeElapsed**2 * np.exp(-1.4 * simulation.totalTimeElapsed)
        )
        simulation.iterate()
        log.append(
            (
                simulation.batmobile.position,
                simulation.batmobile.velocity,
                simulation.batmobile.acceleration,
                simulation.batmobile.battery.voltage,
                simulation.batmobile.battery.current,
                simulation.batmobile.battery.soc,
            ),
        )
    log = np.array(log)
    t = np.linspace(0, T_max, log.shape[0])
    plt.title("Running with current control")
    plt.plot(t, log[:, 0], label="Position")
    plt.plot(t, log[:, 1], label="Velocity")
    plt.plot(t, log[:, 2], label="Acceleration")
    plt.legend()
    plt.savefig(f"results/{name}-car-stats.png")
    plt.figure()
    plt.subplot(2, 1, 1)
    plt.plot(t, log[:, 3], label="Battery Voltage")
    plt.plot(t, log[:, 4], label="Battery Current")
    plt.legend()
    plt.subplot(2, 1, 2)
    plt.plot(t, log[:, 5], label="Battery SOC")
    plt.legend()
    plt.savefig(f"results/{name}-battery-stats.png")
    plt.show()


@invoke.task()
def optimise(ctx, locality: str = "Jericho, Oxfordshire, England, United Kingdom", start=None, end=None, N=20) -> None:
    """Optimise the route."""
    optimiser = Optimiser(graph=BatGraph.fromName(locality))
    nodes = list(optimiser.simulator.batgraph.nodes())
    optimiser.initialise(start or random.choice(nodes), end or random.choice(nodes))
    for _i in range(N):
        optimiser.mcmcStep()


@invoke.task()
def mitja_is_a_bit_silly_sometimes(ctx) -> None:
    """CTX is a variable which stands for context."""
    ctx.run("echo 'Hi Mitja! This is Bash!'")
