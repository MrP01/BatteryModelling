clc
clearvars
dt = 220; d2 = 120; d1 = 80;
vec1 = 60:20:160;
C1 = ones(1,length(vec1));
vec2 = 80;
vec = vec1;
name = "dc";
counter = 0;
for dc = vec1%vec1%[d1 d2 d2+(dt/2-d2)*2 d1+(dt/2-d1)*2]
    counter = counter+1;
for v = vec2 %[60 80 100 120]
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
[tvec,Savec,Sbvec,Scvec]= First_Scenario(check,10,C1(1,counter),Po,zi,zc,I0,T0,h0,c0,tc,tgi,stay,home,ti,tg,tvec,Savec,Sbvec,Scvec);   

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

