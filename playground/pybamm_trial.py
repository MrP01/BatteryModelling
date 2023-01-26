import matplotlib.pyplot as plt
import pybamm
import pybamm.models.full_battery_models.lithium_ion as lithium_ion

plt.switch_backend("tkagg")

model = lithium_ion.DFN()
simulation = pybamm.Simulation(model)
simulation.solve([0, 3600])
simulation.plot()
