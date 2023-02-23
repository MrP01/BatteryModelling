import sys

import invoke
import matplotlib.pyplot as plt
import numpy as np

from simulator.simulation import Simulation


@invoke.task()
def run_trial(ctx, model="lithium-ion"):
    """Runs pybamm."""
    ctx.run(f"{sys.executable} playground/pybamm_trial.py {model}")


@invoke.task()
def run_simulation(ctx, name="constant-current-1.5A", T_max=6.0):
    """Runs the simulation for some given test setting."""
    simulation = Simulation()
    simulation.batmobile.battery.current = 1.5  # set the current
    simulation.chooseTurnIndex = lambda: 0
    log = []
    while simulation.totalTimeElapsed < T_max:
        simulation.iterate()
        log.append(
            (
                simulation.batmobile.position,
                simulation.batmobile.velocity,
                simulation.batmobile.acceleration,
                simulation.batmobile.battery.voltage,
                simulation.batmobile.battery.current,
                simulation.batmobile.battery.soc,
            )
        )
    log = np.array(log)
    t = np.linspace(0, T_max, log.shape[0])
    plt.title(f"Running with current control I = {simulation.batmobile.battery.current} A.")
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
