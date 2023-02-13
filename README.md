# Case Study in Mathematical Modelling

This is a group project from the MSc in MMSC, focused on battery modelling.

## A Journal of the Journey

### Week 1:

- introductory meeting and presentation of available projects

### Week 2:

- Tuesday: first meeting with Robert
- Write code to solve the ODE with a current profile as input
- Derive equations (fitting or approximate functions) for all variables to be included in the code later
- write the exact solution of the equation by hand (check if code solution is similar)
- find out how usually input is given and find a few input profiles that are interesting to examine

Status updates:

- Zella/Nick MATLAB code takes in current input and outputs Voltage over time for ECM. Zella uses polynomial fit to find Voc as a function of state of charge [U(s)]
- Need to model efficiency
- Peter looking at PyBamm--does everything. Could we get our model to do the same thing? Compare our results to PyBamm's results? Also--LTSpice circuits might be helpful for checking results/simulating behavior
- Aoibheann has looked into analytic solution--not too complicated to derive.
- Jad has looked into temperature, charge, and state of health dependence of R0, R1, and C1. 2021 paper--Jad looked at extending parameter fits from linear models to higher order models

Q's for Robert:

- How do we extend the model to incorporate varying parameters such as R0 R1 C1 etc.
- Are linear fits sufficient for parameter finding in 2021 paper? What about quadratic?
- PyBamm comparison?

### Week 3:

Monday: meeting cancelled.

Wednesday meeting with Robert:

- How to find R, C from pulse data--window V vs. t data by state of charge in order to create plots for R vs. state of charge and C vs. state of charge. See picture of board. HPPC or GITT data?
- Make comparisons to PyBamm? Need to make sure that are comparing same battery parameters
- Robert's ideas:
  - Calendar aging --> Q (capacity) now a function of time inside integral for state of charge. Cycle aging --> Q a function of current (high currents mean that Q is lower?
- Can we use more than linear fits for parameter search? Compare to 2021 paper if we do quadratic fitting?
- Battery Genome Project? For good battery data
- Google "battery data and where to find it" paper from edinburgh with links to repositories with data. Ideally, we have small pulse tests at various temperatures and states of health.
- Possible end goal: if I throw different usage profiles at the model can I make recommendations about how the battery should be used? For example, if I have a weekly use profile for a car, when should I charge it? What can I optimize over?
- Can possibly break resistor up into cycle resistor and calendar resistor--one a function of time (long times) and other a function of "state of health"
- Robert's recommendation: use model to get different fits for various states of charge (R0, R1, C1 at different states of charge). Want a function that takes in parameters and outputs error difference between model and experimental values of Voltage for a specific current profile.

Thursday:

- Trying to figure out a short-term, medium-term and long-term goals.
- Much going on in general, 2 hour meeting.
- Find "surfaces" R0(s, h, T), R1(s, h, T) and C1(s, h, T) from data.
- Find optimal charging of electric car on a graph?
- Estimate SOC, SOH from V(t), I(t), etc.
- Game?

### Week 4 Feb 7:

Meeting with Robert

- Parameter vs SOC curves are nice.
- Hinch Perturbation Methods for multiple timescale analysis -- maybe can say something about how we get a speedup for our computations?
- Heating of the battery may be an interesting question
- Looking at optimization on a graph could be an interesting avenue--where to charge, how fast, etc. (performance)
- Can also look at questions about battery death (from modeling capacity)

Big Recommendations:

- Should also look at generating different controls (i.e. what if we have voltage instead of current, or have power instead of current/voltage, and should be able to generate each of these)
- Look at continuous time version and solve in matlab
- Look at modeling capacity (linearly as a function of time and cycle use?)

### Week 5:

Meeting on Monday:

## Repository Structure and Setup:

To use and sustain a Python virtual environment, install [poetry](https://python-poetry.org/), which works with the `pyproject.toml` file.
After installing poetry (and subsequently after pulling, each time), run

```bash
poetry install
```

in the project folder.
To install PyBamm as well (which has 1/epsilon number of dependencies), run

```bash
poetry install --with=pybamm
```

instead or additionally. This sadly requires Python 3.8 based on a pybamm restriction. Without pybamm, 3.11 should be fine too.

Having all dependencies installed, the main interface may be launched up by

```bash
python3 main.py
```

which starts a graphical user interface (with looks depending on your operating system).

The relevant code structure is:

- The folder `simulator/` is responsible for the (numerical) simulation itself, which may be invoked without any interface at all.
  - `simulation.py` features the Simulation class with an `iterate()` method that represents a numerical integration step in time by an amount of `dt`.
  - `batgraph.py` exports a class `BatGraph` that represents a graph (a tuple of sets of edges and vertices) that the car will drive on.
  - `batmobile.py` contains the `BatMobile` class that represents our battery mobile i.e. car. **Much of the simulation takes place in this file!**
  - `battery.py` is the central file for our battery modelling project, which exports a `Battery` class, also featuring an `iterate()` method. **Most of the battery simulation takes place in this file!**
- The interface code is contained within the `interface/` folder.
  - `mainwindow.py` defines the general layout and actions in the user interface.
  - `batmap.py` exports the central widget that renders / animates the BatMobile car on the BatGraph.
  - `graphs.py` handles the connection of the interface and (live) plots. The plots are handled by `matplotlib` and are very intuitive to use, further almost all commands are the same as they are in MatLab.
- `main.py` creates a `MainWindow` and runs the simulator GUI.

### Data Used

- [Dataset used](https://data.mendeley.com/datasets/wykht8y7tg/1) - Z (this has discharge pulses in case we don't find anything else that's more suitable)
