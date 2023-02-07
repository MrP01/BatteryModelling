function polynomialFit = generateOCV(chargeData,dischargeData,capacity,order)
%% Fits a polynomial to given charging and discharging data
% Get SOC data for charging and discharging
SOCcharge= (chargeData.Ah/capacity);

%xDischarge represents the SOC values for the discharge curve
xDischarge = flip((abs(min(dischargeData.Ah)) + dischargeData.Ah) /capacity);
xDischarge = xDischarge(end - length(nonzeros(xDischarge)) +1:end); % gets rid of nonzeros
yDischarge = flip(dischargeData.Voltage); % yDischarge is the voltage for discharging data
yDischarge = yDischarge(end - length(nonzeros(xDischarge)) +1:end);

% now repeat this process for xCharge
xCharge = nonzeros(SOCcharge);
numZeros = length(SOCcharge) - length(xCharge);
yCharge = chargeData.Voltage(numZeros+1:end);

p = polyfit(xDischarge,yDischarge,order); % fit discharging data
q = polyfit(xCharge,yCharge,order); % fit charging data

% generate synthetic polynomial data over [0,1]
xFittedDischarging = linspace(1,0,length(xDischarge));
yFittedDischarging = polyval(p,xFittedDischarging);
yFittedCharging = polyval(q,xFittedDischarging);

% generate averaged curve
meanCurve = [0];
for i=1:length(xFittedDischarging)
    meanCurve(i) = (1-xFittedDischarging(i))*yFittedCharging(i)+xFittedDischarging(i)*yFittedDischarging(i);
end

% fit polynomial to averaged curve, generate synthetic data over [0,1]
polynomialFit = polyfit(xFittedDischarging,meanCurve,order);

xFittedMean = linspace(1,0,length(xFittedDischarging));
yFittedMean = polyval(polynomialFit,xFittedMean);

% plot data
% plot(xFittedDischarging,yFittedDischarging,'b')
% hold on
% plot(xFittedDischarging,yFittedCharging,'r')
% hold on
% plot(xFittedMean,yFittedMean,'g')
% legend('Discharging','Charging','Averaged')
% xlabel('SOC')
% title('OCV against SOC Comparison')
% ylabel('OCV (V)')
end
