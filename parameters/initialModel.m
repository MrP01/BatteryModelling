function [stateOfCharge, iR1, voltageAB, r] = initialModel(samplingRate, ...
        capacity, current, eta, parameters, SOC0, iR10, initialVoltage, ...
        chargeData, dischargeData)

    r = generateOCV(chargeData, dischargeData, capacity, 5);

    R0 = parameters(1);
    R1 = parameters(2);
    C1 = parameters(3);
    stateOfCharge = [SOC0];
    iR1 = [iR10];
    voltageAB = [initialVoltage];

    capacity = getCapacity(capacity); % get capacity in amp seconds

    for i = 1:length(current)
        stateOfCharge(i + 1) = stateOfCharge(i) - (samplingRate / capacity) * eta(i) * current(i);
        iR1(i + 1) = exp(-samplingRate / (R1 * C1)) * iR1(i) + (1 - exp(- samplingRate / (R1 * C1))) * current(i);
        voltageAB(i) = polyval(r, stateOfCharge(i)) - R1 * iR1(i) - R0 * current(i); %might need to change polyval to OCV(SOC)
    end

end
