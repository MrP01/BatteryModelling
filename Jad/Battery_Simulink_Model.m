clc
for v = 112:112
%% Required Power from velocity
r = 0.135;
N = 25/(3*pi)/r*v;
Pgrid = 0:1000:7000;
Pdata = [0  24.9  49 73.5 91 95 90 82];
p1 = polyfit(Pgrid,Pdata,2);
figure
P = @(v) p1(1,1)*v^2+p1(1,2)*v+p1(1,3);
fplot(P,[0 7000])
Po = P(N);

%% Model
[SOC0,SOCb,SOCa,SOCh]= Aoibheann(P);
%% System Parameters specified by us
%In order
Ccharge = 1;
Chome = 1;
Cost_1 = 5; %dollars for 0 -- 1
Cost_2 = 10; %Dollars for 0 -- 1
%% SIMULINK
%% Parameters
SOC_vec = [0, .1, .25, .5, .75, .9, 1]; % Vector of state-of-charge values, SOC
T_vec   = [278, 293, 313];              % Vector of temperatures, T, (K)
AH      = 27;                           % Cell capacity, AH, (A*hr) [40 120]
thermal_mass = 100;                     % Thermal mass (J/K)
initialSOC = 0.65;                       % Battery initial SOC
V0_mat  = [3.49, 3.5, 3.51; 3.55, 3.57, 3.56; 3.62, 3.63, 3.64;3.71, 3.71, 3.72; 3.91, 3.93, 3.94; 4.07, 4.08, 4.08;4.19, 4.19, 4.19];% Open-circuit voltage, V0(SOC,T), (V)
R0_mat  = [.0117, .0085, .009; .011, .0085, .009;...
    .0114, .0087, .0092; .0107, .0082, .0088; .0107, .0083, .0091;...
    .0113, .0085, .0089; .0116, .0085, .0089];  % Terminal resistance, R0(SOC,T), (ohm)
R1_mat  = [.0109, .0029, .0013; .0069, .0024, .0012;...
    .0047, .0026, .0013; .0034, .0016, .001; .0033, .0023, .0014;...
    .0033, .0018, .0011; .0028, .0017, .0011];  % First polarization resistance, R1(SOC,T), (ohm)
tau1_mat = [20, 36, 39; 31, 45, 39; 109, 105, 61;36, 29, 26; 59, 77, 67; 40, 33, 29; 25, 39, 33]; % First time constant, tau1(SOC,T), (s)
cell_area = 0.1019; % Cell area (m^2)
h_conv    = 5;      % Heat transfer coefficient (W/(K*m^2))
%% Kalman Filter
Q    = [1e-4 0 0;0 1e-4 0;0 0 1e-4]; % Covariance of the process noise, Q
R    = 0.05;                         % Covariance of the measurement noise, R
P0   = [1e-5 0 0; 0 1 0; 0 0 1e-5];  % Initial state error covariance, P0
R00  = 0.008;                        % Estimator initial R0
Ts   = 1;                            % Sample time (s)
n_cycles = 39;
Tstop = 10*36000;
%% Open system
%open_system('BatterySOHEstimationJad')
sim('BatterySOHEstimationJad')
%% Extracting SOH from simulink
S = zeros(1,length(SOH));
for z = 1:length(SOH)
S(1,z)=SOH(1,1,z);
end
% figure
% plot(1:length(S),S,'LineWidth',2)
Z = zeros(1,length(SOC));
for z = 1:length(SOC)
Z(1,z)=SOC(1,1,z);
end
% figure
% plot(1:length(Z),Z,'LineWidth',2)
% figure
% plot(1:length(Cu),Cu,'LineWidth',2)
p = polyfit(1:length(S),S,1);
A=0.2*n_cycles/(1-(p(1,1)*length(S)+p(1,2)))/10;
t_change = A;
disp(t_change)
% fsoh = @(x) (1 - 4.54*10^-4*x -exp(5.07*10^-2 * (x - (A+100))));
% figure
% idx=inf;
% for i =0:A+100
%     if fsoh(i)<0
%         idx = i;
%     end
% end
% fplot(fsoh,[0 idx],'linewidth',2)

%% Cost estimation
C = 1:52*10; %(10 years in weeks)
C_charging = @(C) C*Cost_1; %(or Cost_2)
C_change = t_change/2;
counter = 1;
C_SOH = @(C) 0;
for N = C(rem(C,round(C_change))==0)
    C_SOH = @(C) C_SOH(C) + heaviside(C-N)*3000;
end
Ct = @(C) C_charging(C)+C_SOH(C);
figure
fplot(Ct,[C(1,1) C(1,end)])
end


function [SOC0,SOCb,SOCa,SOCh]=Aoibheann(P)
SOC0 = 0.65;
SOCb = 0.1;
SOCa = 0.8;
SOCh = 0.3;
end
