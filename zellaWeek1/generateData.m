chargeData = importdata('c2.mat'); % load data
dischargeData = importdata('dc2.mat');

samplingRate = 30; % 10s sampling
capacity = 2.9; % 2.9Ah cell
current = -(dischargeData.Current); % data given with reversed sign
current(1:20) = 0; % create artificial initial 0 current
current(21:343) = 1;

stateOfChargeInit = 0.5;
iR1Init = 0;
voltageABInit = 4.2;
R0 = 45e-3;
R1 = 89e-3;
C1 = 35e1;
circuitParameters = [R0,R1,C1]; % R0, R1, C1

eta = ones(length(current),1); % TODO: better model

[stateOfCharge,iR1,voltageAB,r] = initialModel(samplingRate,capacity,...
                        current,eta,circuitParameters,stateOfChargeInit,...
                        iR1Init,voltageABInit,chargeData,dischargeData);
figure
plot((0:length(voltageAB)-1)*samplingRate,voltageAB,'r')
title('V_{AB} against Time, Panasonic 18650PF Dataset')
xlabel('Time (s)')
ylabel('V_{AB} (V)')
hold off
