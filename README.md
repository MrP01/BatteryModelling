# Case Study in Mathematical Modelling

This is a group project from the MSc in MMSC, focused on battery modelling.

## A Journal of the Journey

## Week 1:

- introductory meeting and presentation of available projects

## Week 2:

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

## Week 3:

### Repository Structure and Setup:

... to be defined

To use and sustain a Python virtual environment, install [poetry](https://python-poetry.org/), which works with the `pyproject.toml` file.

Wednesday meeting with Robert:

- How to find R, C from pulse data--window V vs. t data by state of charge in order to create plots for R vs. state of charge and C vs. state of charge. See picture of board. HPPC or GITT data?
- Make comparisons to PyBamm? Need to make sure that are comparing same battery parameters
- Robert's ideas:
- - Calendar aging --> Q (capacity) now a function of time inside integral for state of charge. Cycle aging --> Q a function of current (high currents mean that Q is lower?
- Can we use more than linear fits for parameter search? Compare to 2021 paper if we do quadratic fitting?
- Battery Genome Project? For good battery data
- Google "battery data and where to find it" paper from edinburgh with links to repositories with data. Ideally, we have small pulse tests at various temperatures and states of health.
- Possible end goal: if I throw different usage profiles at the model can I make recommendations about how the battery should be used? For example, if I have a weekly use profile for a car, when should I charge it? What can I optimize over?
- Can possibly break resistor up into cycle resistor and calendar resistor--one a function of time (long times) and other a function of "state of health"
- Robert's recommendation: use model to get different fits for various states of charge (R0, R1, C1 at different states of charge). Want a function that takes in parameters and outputs error difference between model and experimental values of Voltage for a specific current profile.

### Data Used

- [Dataset used](https://data.mendeley.com/datasets/wykht8y7tg/1) - Z (this has discharge pulses in case we don't find anything else that's more suitable)
