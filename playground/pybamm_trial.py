import sys

import matplotlib.pyplot as plt
import pybamm
import pybamm.models.full_battery_models.equivalent_circuit.thevenin as thevenin
import pybamm.models.full_battery_models.lithium_ion as lithium_ion

plt.switch_backend("tkagg")

if sys.argv[-1] == "lithium-ion":
    model = lithium_ion.DFN()
    simulation = pybamm.Simulation(model)
    simulation.solve([0, 3600])
    simulation.plot()
else:
    model = thevenin.Thevenin()
    simulation = pybamm.Simulation(model)
    simulation.solve([0, 3600])
    simulation.plot()

plt.show()
