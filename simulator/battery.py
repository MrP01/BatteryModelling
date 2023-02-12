import numpy as np
import dataclasses


@dataclasses.dataclass()
class BatteryMeasurement:
    time: float
    voltage: float
    current: float
    soc: float


class Battery:
    """Class representing the battery in the BatMobile. Keeps track of parameters and does the core simulation."""

    ocvPolynomial = (10.7950, -26.0626, 22.7642, -8.3793, 1.5987, 3.4686)
    capacity = 2.9 * 3600  # Ampere seconds of 2.9Ah battery

    def __init__(self):
        self.voltage: float = 0  # total (AB) voltage of the battery / ECM Model
        self.current: float = 0  # current through the battery (positive <=> discharging)
        self.soc: float = 1
        self.soh: float = 1
        self.temperature: float = 20  # °C

        # Auxiliary "internal" values
        self.iR1: float = 0

    def iterate(self):
        """Does the numerical integration step in time."""
        eta = 1
        samplingRate = 30
        self.soc = self.soc - (samplingRate / self.capacity) * eta * self.current
        self.iR1 = self.current - np.exp(-samplingRate / (self.R1() * self.C1())) * (self.current - self.iR1)
        self.voltage = self.ocv() - self.R0() * self.current - self.R1() * self.iR1

    def ocv(self):
        """Returns an estimate of the OCV voltage based on a polynomial model."""
        return np.polyval(self.ocvPolynomial, self.soc)

    def R0(self):
        """Return this based on SOC, SOH and temperature. Can depend on anything!"""
        return 45e-3

    def R1(self):
        """Return this based on SOC, SOH and temperature. Can depend on anything!"""
        return 89e-3

    def C1(self):
        """Return this based on SOC, SOH and temperature. Can depend on anything!"""
        return 35e1

    def measurement(self) -> BatteryMeasurement:
        return BatteryMeasurement(0, self.voltage, self.current, self.soc)
