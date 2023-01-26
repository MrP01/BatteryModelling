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

## Repository Structure and Setup:

... to be defined

To use and sustain a Python virtual environment, install [poetry](https://python-poetry.org/), which works with the `pyproject.toml` file.
