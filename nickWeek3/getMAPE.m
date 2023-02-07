function [sumMAPE] = getMAPE(measuredVoltage,predictedVoltage)
%GETSSE
% Given two voltage curves, finds sum of squared errors
sumMAPE = sum(abs(measuredVoltage-predictedVoltage));
end