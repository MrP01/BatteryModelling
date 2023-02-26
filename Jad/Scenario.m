clc
clearvars
close all
dt = 220; %Total distance (to granny*2)
vec1 = 150; %Distances of charging stations 
C1 = ones(1,length(vec1)); %Charging rate of stations
Co1 = [10 20 20 30 30]; %Cost of charging in stations
Cbattery = 3000; %Cost of a battery
vec2 = 80; %Speeds to test on
ncycles = 20; %number of cycles to test

if length(vec1)>1
vec = vec1;
name = "dc";
else
vec = vec2;
name = "V";
end

counter = 0;
for dc = vec1
    counter = counter+1;
for v = vec2 
%% Required Power from velocity
r = 0.135;
N = 25/(3*pi)/r*v;
Pgrid = 0:1000:7000;
Pdata = [0  24.9  49 73.5 91 95 90 82];
p1 = polyfit(Pgrid,Pdata,2);
%figure
P = @(v) p1(1,1)*v^2+p1(1,2)*v+p1(1,3);
%fplot(P,[0 7000])
Po = P(N)/50;

%% Model
zi = 0.8; zc = 0.9; I0 = 1; T0 = 10; h0 = 1; c0 = 0;
tc = dc/v*3600; tgi = dt/2/v*3600; stay = 48*3600; home = 24*3600*5; ti = 0; tg = tgi;
tvec = []; Savec = []; Sbvec = []; Scvec = []; 
if dc > dt/2
    check = 0;
else
    check = 1;
end
[tvec,Savec,Sbvec,Scvec]= First_Scenario(check,ncycles,C1(1,counter),Po,zi,zc,I0,T0,h0,c0,tc,tgi,stay,home,ti,tg,tvec,Savec,Sbvec,Scvec);   
t_1_cycle = tvec(end,1)/ncycles;
figure(1)
hold on
plot(tvec,Savec,'linewidth',2)
hold off

figure (2)
hold on
plot(tvec,Sbvec,'linewidth',2)
hold off
figure (3)
hold on
plot(tvec,Scvec,'linewidth',2)
if counter == 1
Ccharging = zeros(1,length(tvec));
Compare = zeros(2,length(tvec));
end
Compare(counter,:) = Scvec;
hold off
end
end


s = strings(1,length(vec));
for i = 1:length(vec)
s(1,i) = name+" = "+vec(i);
end
figure(1)
legend(s(1:length(vec)))
figure(2)
legend(s(1:length(vec)))
figure(3)
legend(s(1:length(vec)))

%% Plotting cost
%This part will only show up if different charging stations are compared! 
% (i.e. not for velocities)
if length(vec1)~=1
    counter = 1;
    for l = 1:length(vec1)-1
        counter = counter+1;
for z = 1:ncycles
        tcomp = (t_1_cycle*z)+1;
        idx = find(abs(tvec-tcomp)== min(abs(tvec-tcomp)));
        Ccharging(1,idx(1,1):end) = Ccharging(1,idx(1,1):end)+(Co1(1,1)-Co1(1,counter));
end
Cost = Ccharging-(Compare(1,:)-Compare(counter,:))/0.4*Cbattery;
figure(4)
hold on
plot(tvec,Cost,'linewidth',2)
    end
figure(4)
hold on
s = strings(1,length(vec1)-1);
for i = 2:length(vec1)
s(1,i-1) = "dc = "+vec1(i);
end
legend(s,'location','southeast')
title("Comparing "+num2str(vec1(1,1)))
end