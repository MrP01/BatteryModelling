function [sumSquaredErrors] = getSSE(measuredVoltage,predictedVoltage)
%GETSSE
% Given two voltage curves, finds sum of squared errors
sumSquaredErrors = sum((measuredVoltage-predictedVoltage).^2);
end
