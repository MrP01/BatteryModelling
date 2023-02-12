clc
%% Battery State-of-Health Estimation
% This example shows how to estimate the battery internal resistance and 
% state-of-health (SOH) by using an adaptive Kalman filter. The initial 
% state-of-charge (SOC) of the battery is equal to 0.6. The estimator uses 
% an initial condition for the SOC equal to 0.65. The battery keeps 
% charging and discharging for 10 hours. The unscented Kalman filter
% estimator converges to the real value of the SOC while also estimating 
% the internal resistance. To use a different Kalman filter implementation, 
% in the SOC Estimator (Kalman Filter) block, set the Filter type parameter 
% to the desired value.

% Copyright 2022 The MathWorks, Inc.

%% Model

%openExample('simscapebattery/BatterySOHEstimationExample')

open_system('BatterySOHEstimation')

set_param(find_system('BatterySOHEstimation','FindAll', 'on','type','annotation','Tag','ModelFeatures'),'Interpreter','off')

%% Defining DATA in Simulink
SOC_vec = [0 0.1 0.25 0.5 0.75 0.9 1]; %SOC Lookup values
T_vec = [278 293 313]; %Temperature Lookup Values
V0_mat = [3.49,3.5,3.51;3.55,3.57,3.56;3.62,3.63,3.64;3.71,3.71,3.72;3.91,3.93,3.94;4.07,4.08,4.08;4.19,4.19,4.19]; %Voc(f(SOC,T))
R0_mat = [0.0117 0.0085 0.009;0.011 0.0085 0.009;0.0114 0.0087 0.0092;0.0107 0.0082 0.0088;0.0107 0.0083 0.0091;0.0113 0.0085 0.0089;0.01166 0.0085 0.0089]; %R0(f(SOC,T))
AH = 27; %cell capacity in AH
R1_mat = [0.0109 0.0029 0.0013;0.0069 0.0024 0.0012;0.0047 0.0026 0.0013;0.0034 0.0016 0.001;0.0033 0.0023 0.0014;0.0033 0.0018 0.0011;0.0028 0.0017 0.0011];%R1(f(SOC,T))
tau1_mat = [20 36 39;31 45 39;109 105 61;36 29 26;59 77 67;40 33 29;25 39 33];

%% Extracting SOH from simulink
J = zeros(1,length(simout));
for z = 1:length(simout)
J(1,z)=simout(1,1,z);
end
plot(1:length(J),J)