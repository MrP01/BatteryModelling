function [voltageAB] = getVoltageCurveConstOCV(samplingRate,capacity,current,eta,parameters, ...
                                        iR10, OCV) % OCV is a constant!

R0 = parameters(1);
R1 = parameters(2);
C1 = parameters(3);
iR1 = [iR10];
voltageAB = [OCV];


capacity = getCapacity(capacity); % get capacity in amp seconds

for i=1:length(current)
    iR1(i+1) = exp(-samplingRate/(R1*C1)) * iR1(i) + (1 - exp(- samplingRate/(R1*C1)))*current(i);
    voltageAB(i) = OCV - R1*iR1(i)- R0*current(i);
end

voltageAB = voltageAB'; % column vector
