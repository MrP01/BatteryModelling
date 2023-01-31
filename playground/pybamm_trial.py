import sys

import matplotlib.pyplot as plt
import pybamm
import pybamm.models.full_battery_models.equivalent_circuit.thevenin as thevenin
import pybamm.models.full_battery_models.lithium_ion as lithium_ion

plt.switch_backend("tkagg")

model_name = sys.argv[-1]
model = lithium_ion.DFN() if model_name == "lithium-ion" else thevenin.Thevenin()
print(model.name)
model.print_parameter_info()

simulation = pybamm.Simulation(model)
simulation.solve([0, 3600])
simulation.plot()

plt.show()
