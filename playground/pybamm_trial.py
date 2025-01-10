# type: ignore
import sys

import matplotlib.pyplot as plt
import pybamm
from pybamm.models.full_battery_models import lithium_ion
from pybamm.models.full_battery_models.equivalent_circuit import thevenin

plt.switch_backend("tkagg")

model_name = sys.argv[-1]
model = lithium_ion.DFN() if model_name == "lithium-ion" else thevenin.Thevenin()
model.print_parameter_info()

simulation = pybamm.Simulation(model)
simulation.solve([0, 3600])
simulation.plot()

plt.show()
