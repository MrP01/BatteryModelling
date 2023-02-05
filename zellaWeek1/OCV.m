function openCurrentVoltage = OCV(stateOfChargeValue)
    % fits a 5th order polynomial to the discharging plot to get the OCV
    % as a function of SOC
    dischargeData = importdata('dc2.mat');
    capacity = 2.9; %Ah
    x = flip((abs(min(dischargeData.Ah)) + dischargeData.Ah) /capacity);
    x = x(end - length(nonzeros(x)) +1:end);
    y = flip(dischargeData.Voltage);
    y = y(end - length(nonzeros(x)) +1:end);
    p = polyfit(x,y,5);
    openCurrentVoltage = polyval(p,stateOfChargeValue);
end
