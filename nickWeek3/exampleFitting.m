%% Load data (current profile, voltage profile, initial state of charge
chargeData = importdata('c2.mat'); % load data
dischargeData = importdata('dc2.mat');

%% Calculate SOC curve ?? Need to do this more generally probably... might
% depend on temperature and stuff
capacity = 2.9; % 2.9Ahr cell
%OCV = generateOCV(chargeData,dischargeData,capacity,5);

%% Load specific current and voltage profile.
dataDir ="/home/sulch/BatteryModelling/cleanData/10c/cleanData10C/";
filename = "run26_10C.csv";
runData = readtable(dataDir + filename);
measuredVoltage = runData.voltage;
% OCV = mean(measuredVoltage([1:3 length(measuredVoltage)-3:length(measuredVoltage)]))
OCV = mean(measuredVoltage([1:5]))
%OCV = mean(measuredVoltage(1:10));
current = runData.current;
stateOfCharge = runData.SOC;

%% Calculate R0, R1, C1 through fitting process
typicalR0 = 8.2e-3;
typicalR1 = 15.8e-3;
typicalC1 = 38e3;
% % initialParameters = [typicalR0 typicalR1 typicalC1, OCV];
initialParameters = [typicalR0 typicalR1 typicalC1];
samplingRate = 10; % 10s sampling
capacity = 2.9; % 2.9Ah cell
eta = ones(length(current), 1);
iR10 = 0;

% %  errorOfPrediction = @(params) getSSE(measuredVoltage, ...
% %                                       getVoltageCurve(samplingRate, ...
% %                                                       capacity, ...
% %                                                       current, ...
% %                                                       eta, ...
% %                                                       params, ...
% %                                                       stateOfCharge, ...
% %                                                       iR10, ...
% %                                                       OCV));
errorOfPrediction = @(params) getSSE(measuredVoltage, ...
getVoltageCurveConstOCV(samplingRate, ...
    capacity, ...
    current, ...
    eta, ...
    params, ...
    iR10, ...
    OCV));

%%
X = fminsearch(errorOfPrediction, initialParameters)
R0 = X(1); R1 = X(2); C1 = X(3);

predictedVoltage = getVoltageCurveConstOCV(samplingRate, ...
    capacity, ...
    current, ...
    eta, ...
    [R0 R1 C1], ...
    iR10, ...
    OCV);
% figure(1)
% plot(predictedVoltage, "b--");
% hold on
% plot(measuredVoltage, "r");
% hold off
% shg
% 
% figure(2)
% plot(current)
% shg
x = 0.01.*[1:length(measuredVoltage)];
ECMMotivation = figure(1);
p1 = subplot(2, 1, 1);
plot(x, measuredVoltage)
title("Battery Voltage vs Time")
ylabel("Voltage (V)")
xlabel("Time (s)")
p2 = subplot(2,1,2);
plot(x, current);
title("Current vs Time")
ylabel("Current (A)")
xlabel("Time (s)")
saveas(ECMMotivation, "ECMMotivation.png")
fontsize(ECMMotivation, "increase")
fontsize(ECMMotivation, "increase")
fontsize(ECMMotivation, "increase")


ECMModellingExample = figure(2);
p3 = subplot(2, 1, 1);
hold on
plot(x, measuredVoltage, "b")
plot(x, predictedVoltage, "r--")
title("Battery Voltage vs Time")
ylabel("Voltage (V)")
xlabel("Time (s)")
legend("Measured Voltage", "ECM Model")
hold off
p4 = subplot(2, 1, 2);
plot(x, current);
title("Current vs Time")
ylabel("Current (A)")
xlabel("Time (s)")
fontsize(ECMModellingExample, "increase")
fontsize(ECMModellingExample, "increase")
fontsize(ECMModellingExample, "increase")

saveas(ECMModellingExample, "ECMModellingExample.png")
%%
csvwrite('measuredVoltage.csv', measuredVoltage);
csvwrite('predictedVoltage.csv', predictedVoltage);
csvwrite('times.csv', x);
csvwrite('measuredCurrent.csv', current);
