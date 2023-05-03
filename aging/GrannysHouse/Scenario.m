clc
clearvars
close all
dt = 230;%220; %Total distance (to granny*2)
vec1 = [20 95 135 210]; %Distances of charging stations
C1 = ones(1,length(vec1)); %Charging rate of stations
Co1 = [15 10 15 10]; %Cost of charging in stations
Cbattery = 3000; %Cost of a battery
vec2 = 100; %Speeds to test on
ncycles = 40; %number of cycles to test
confifactor = (1-(abs(vec2(1,1)-80)/80))*exp(-(vec2-80).^2/2200);
if length(vec1)>1
vec = vec1;
name = "Route ";
else
vec = vec2;
name = "V";
end
counter4 = 0;
for stays = 6:6
    counter4 = counter4+1;
    counter3 = 0;
for calendar = 0:2
counter3 = counter3+1;
counter = 0;
counter2 = 0;
for dc = vec1
    counter = counter+1;
for v = vec2
counter2 = counter2+1;
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
zi = 0.8; zc = 0.795; I0 = 1; T0 = 10; h0 = 1; c0 = 0;
tc = dc/v*3600; tgi = dt/2/v*3600; stay = 24*3600*(7-stays); home = 24*3600*stays; ti = 0; tg = tgi;
tvec = []; tzella = []; Sazella = []; Savec = []; Sbvec = []; Scvec = []; Sdvec = [];
if dc > dt/2
    check = 0;
else
    check = 1;
end
[tvec,Savec,Sbvec,Scvec,Sdvec,SOH_PER_TRIP,tzella,Sazella,tonce,Saonce]= First_Scenario(check,ncycles,C1(1,counter),Po,zi,zc,I0,T0,h0,c0,tc,tgi,stay,home,ti,tg,tvec,tzella,Sazella,Savec,Sbvec,Scvec,Sdvec,calendar,0.4);

tzellaplot(counter,1:length(tzella),counter3) = tzella;
Sazellaplot(counter,1:length(Sazella),counter3) = Sazella;
tplot(counter,1:length(tvec),counter3)=tvec;
Saplot(counter,1:length(tvec),counter3)= Savec;
Sbplot(counter,1:length(tvec),counter3)= Sbvec;
Scplot(counter,1:length(tvec),counter3)= Scvec;
Sdplot(counter,1:length(tvec),counter3)=Sdvec;
NickPlot1(counter, 1:length(SOH_PER_TRIP), counter3) = SOH_PER_TRIP(1, :);
NickPlot2(counter, 1:length(SOH_PER_TRIP), counter3) = SOH_PER_TRIP(2, :);
NickPlot3(counter,1:length(SOH_PER_TRIP),counter3) = SOH_PER_TRIP(3,:);
toncep(counter,1:length(tonce),counter3) = tonce;
Saoncep(counter,1:length(tonce),counter3)=Saonce;
end
end
end
Percentage(counter4,1)= mean((ones-nonzeros(Scplot(end,:,1)))./(ones-nonzeros(Scplot(end,:,2))))*100;
end

%% Plotting
%Legend
s = strings(1,length(vec));
for i = 1:length(vec)
s(1,i) = name+i;
end
%% Figures for both aging
figure
for i = 1:counter
%     plot(tplot(i,Scplot(i,:,2)~=0,1),nonzeros(Scplot(i,:,2)),'linewidth',1.2)
    x = linspace(0,40,length(NickPlot1(i, :, 2)));
    plot(x, NickPlot2(i, :, 2), 'linewidth', 1.2);
    hold on
end
legend(s(1:length(vec)))
title('Degradation Over Time')
xlabel('Visits','FontWeight','bold')
ylabel('State of Health','FontWeight','bold')
adjust

figure
subplot(1,3,1)
for i = 1:counter
if i == 1 || i == 4
    m1 = 'Red';
    if i == 1
        m2 = '-';
    else
        m2 = '--';
    end
else
    m1 = 'Blue';
    if i == 3
        m2 = '-';
    else
        m2 = '--';
    end
end
x = linspace(0,40,length(NickPlot1(i, :, 1)));
 plot(x, NickPlot2(i, :, 1), 'linewidth', 1.2,'Color',m1,'LineStyle',m2);
    hold on
end
legend(s(1:length(vec)),'location','southwest')
title('State of Health (Cycle Aging)')
xlabel('Visits','Fontweight','bold')
ylabel('State of Health','fontweight','bold')
axis square
ylim([0.9 1])
adjust
subplot(1,3,2)
for i = 1:counter
 if i == 1 || i == 4
    m1 = 'Red';
    if i == 1
        m2 = '-';
    else
        m2 = '--';
    end
else
    m1 = 'Blue';
    if i == 4
        m2 = '-';
    elseif i ==3
        m2 = '--';
    end
 end
 x = linspace(0,40,length(NickPlot1(i, :, 3)));
    plot(x, NickPlot2(i, :, 3), 'linewidth', 1.2,'LineStyle',m2,'Color',m1);
    hold on
end
legend(s(1:length(vec)),'location','southwest')
title('State of Health (Calendar Aging)')
xlabel('Visits','FontWeight','bold')
ylabel('State of Health','FontWeight','bold')
ylim([0.9 1])
adjust
subplot(1,3,3)
for i = 1:counter
 if i == 1 || i == 4
    m1 = 'Red';
    if i == 1
        m2 = '-';
    else
        m2 = '--';
    end
else
    m1 = 'Blue';
    if i == 4
        m2 = '-';
    elseif i ==3
        m2 = '--';
    end
 end
 x = linspace(0,40,length(NickPlot1(i, :, 2)));
    plot(x, NickPlot2(i, :, 2), 'linewidth', 1.2,'LineStyle',m2,'Color',m1);
    hold on
end
legend(s(1:length(vec)),'location','southwest')
title('State of Health')
xlabel('Visits','FontWeight','bold')
ylabel('State of Health','FontWeight','bold')
ylim([0.9 1])
adjust
%% One time fig

tnow2 = tzellaplot(2,Sazellaplot(2,:,3)~=0,3);
for i = 1:length(tnow2)-1
    if (tnow2(1,i+1,1)-tnow2(1,i,1))>stay*0.9
        tnow2(1,i+1:end,1) = tnow2(1,i+1:end,1)-(tnow2(1,i+1,1)-tnow2(1,i,1));
    end
end
tnow1 = tzellaplot(1,Sazellaplot(1,:,3)~=0,3);
for i = 1:length(tnow1)-1
    if (tnow1(1,i+1,1)-tnow1(1,i,1))>stay*0.9
        tnow1(1,i+1:end,1) = tnow1(1,i+1:end,1)-(tnow1(1,i+1,1)-tnow1(1,i,1));
    end
end
tnow3 = tzellaplot(3,Sazellaplot(3,:,3)~=0,3);
for i = 1:length(tnow3)-1
    if (tnow3(1,i+1,1)-tnow3(1,i,1))>stay*0.9
        tnow3(1,i+1:end,1) = tnow3(1,i+1:end,1)-(tnow3(1,i+1,1)-tnow3(1,i,1));
    end
end
tnow4 = tzellaplot(4,Sazellaplot(4,:,3)~=0,3);
for i = 1:length(tnow4)-1
    if (tnow4(1,i+1,1)-tnow4(1,i,1))>stay*0.9
        tnow4(1,i+1:end,1) = tnow4(1,i+1:end,1)-(tnow4(1,i+1,1)-tnow4(1,i,1));
    end
end
[y1valz,y2valz,~,y4valz,Error] = Compute_Mean(tnow1,tnow2,tnow3,tnow4,nonzeros(Sazellaplot(1,:,3)),nonzeros(Sazellaplot(2,:,3)),nonzeros(Sazellaplot(3,:,3)),nonzeros(Sazellaplot(4,:,3)));
[y1val,y2val,~,y4val,Error] = Compute_Mean(tplot(1,Saplot(1,:,3)~=0,3),tplot(2,Saplot(2,:,3)~=0,3),tplot(3,Saplot(3,:,3)~=0,3),tplot(4,Saplot(4,:,3)~=0,3),nonzeros(Saplot(1,:,3)),nonzeros(Saplot(2,:,3)),nonzeros(Saplot(3,:,3)),nonzeros(Saplot(4,:,3)));
% figure
% subplot(1,2,1)
% plot(tnow2,nonzeros(Sazellaplot(2,:,3)),'linewidth',2)
% hold on
% plot(tnow2,ones(1,length(tzellaplot(2,Sazellaplot(2,:,3)~=0,3)))*y2valz,'linewidth',2)
% xlim([-0.2*10^5 6.2*10^5])
% xlabel('Time')
% ylabel('SOC')
% title('Profile for route 2')
% ylim([0 1])
% subplot(1,2,2)
% plot(tnow4,nonzeros(Sazellaplot(4,:,3)),'linewidth',2)
% hold on
% plot(tnow4,ones(1,length(tzellaplot(4,Sazellaplot(4,:,3)~=0,3)))*y4valz,'linewidth',2)
% xlim([-0.2*10^5 6.2*10^5])
% xlabel('Time')
% ylabel('SOC')
% title('Profile for route 4')
% ylim([0 1])

figure
subplot(1,2,1)
plot(tplot(2,Saplot(2,:,3)~=0,3)/max(NickPlot1(2, :, 3))*ncycles,nonzeros(Saplot(2,:,3)),'linewidth',2)
hold on
xlim([min(tplot(2,Saplot(4,:,3)~=0,3))/max(NickPlot1(4, :, 3))*ncycles,1])
xlabel('Visits','FontWeight','bold')
ylabel('State of Charge','FontWeight','bold')
title('Route 2')
ylim([0 1])
adjust
subplot(1,2,2)
plot(tplot(4,Saplot(4,:,3)~=0,3)/max(NickPlot1(4, :, 3))*ncycles,nonzeros(Saplot(4,:,3)),'linewidth',2)
hold on
%plot(tplot(4,Saplot(4,:,3)~=0,3),ones(1,length(tplot(4,Saplot(4,:,3)~=0,3)))*y4val,'linewidth',2)
xlim([min(tplot(4,Saplot(4,:,3)~=0,3))/max(NickPlot1(4, :, 3))*ncycles,max(tplot(4,Saplot(4,:,3)~=0,3))/max(NickPlot1(4, :, 3))*ncycles])
xlabel('Visits','FontWeight','bold')
ylabel('State of Charge','FontWeight','bold')
title('Route 4')
ylim([0 1])
adjust
%% Figures for cycle aging
figure
for twice = 1:2
subplot(1,2,twice)
for i = 1:counter
%plot(tplot(i,Scplot(i,:,1)~=0,1),nonzeros(Scplot(i,:,1)),'linewidth',1.2)
if i == 1 || i == 4
    m1 = 'Red';
    if i == 1
        m2 = '-';
    else
        m2 = '--';
    end
else
    m1 = 'Blue';
    if i == 2
        m2 = '-';
    else
        m2 = '--';
    end
end
x = linspace(0,40,length(NickPlot1(i, :, 1)));
 plot(x, NickPlot2(i, :, 1), 'linewidth', 1.2,'Color',m1,'LineStyle',m2);
    hold on
end
legend(s(1:length(vec)))
if twice == 1
title('State of Health (Cycle Aging)')
else
title('State of Health (Zoomed)')
end
xlabel('Visits','Fontweight','bold')
ylabel('State of Health','fontweight','bold')
axis square
adjust
if twice == 1
rectangle('Position',[32 0.97 2 0.0012],'Linewidth',2)
else
xlim([32 34])
ylim([0.97 0.97+0.0012])
adjust
end
end

tnow2 = toncep(2,:,1);
for i = 1:length(tnow2)-1
    if (tnow2(1,i+1,1)-tnow2(1,i,1))>stay*0.9
        tnow2(1,i+1:end,1) = tnow2(1,i+1:end,1)-(tnow2(1,i+1,1)-tnow2(1,i,1));
    end
end

tnow4 = toncep(4,:,1);
for i = 1:length(tnow4)-1
    if (tnow4(1,i+1,1)-tnow4(1,i,1))>stay*0.9
        tnow4(1,i+1:end,1) = tnow4(1,i+1:end,1)-(tnow4(1,i+1,1)-tnow4(1,i,1));
    end
end
figure
tnow2 = tnow2/max(NickPlot1(2, :, 3))*40;
tnow4 = tnow4/max(NickPlot1(2, :, 3))*40;
plot(tnow2,nonzeros(Saoncep(2,:,1)),'linewidth',2,'Color','blue')
hold on
plot(tnow4,nonzeros(Saoncep(4,:,1)),'linewidth',2,'Color','red')
plot(tnow2,ones(1,length(tnow2))*y2valz,'linewidth',2,'Color','blue','LineStyle','--')
plot(tnow4,ones(1,length(tnow4))*y4valz,'linewidth',2,'Color','red','LineStyle','--')
xlabel('Visits','FontWeight','bold')
ylabel('State of Charge','FontWeight','bold')
title('State of Charge Profiles')
legend('Route 2','Route 4','','')
text(40/max(NickPlot1(2, :, 3))*40,y2valz-0.03,'Mean 2','Color','Blue','FontSize',20,'FontWeight','bold')
text(40/max(NickPlot1(2, :, 3))*40,y4valz-0.03,'Mean 4','Color','Red','FontSize',20,'FontWeight','bold')
ylim([0 1])
adjust

figure
subplot(1,2,1)
plot(tnow2,nonzeros(Saoncep(2,:,1)),'linewidth',2,'Color','blue')
hold on
plot(tnow4,nonzeros(Saoncep(4,:,1)),'linewidth',2,'Color','red')
plot(tnow2,ones(1,length(tnow2))*y2valz,'linewidth',2,'Color','blue','LineStyle','--')
plot(tnow4,ones(1,length(tnow4))*y4valz,'linewidth',2,'Color','red','LineStyle','--')
xlabel('Visits','FontWeight','bold')
ylabel('State of Charge','FontWeight','bold')
title('State of Charge Profiles')
legend('Route 2','Route 4','','')
text(40/max(NickPlot1(2, :, 3))*40,y2valz-0.03,'Mean 2','Color','Blue','FontSize',20,'FontWeight','bold')
text(40/max(NickPlot1(2, :, 3))*40,y4valz-0.03,'Mean 4','Color','Red','FontSize',20,'FontWeight','bold')
ylim([0 1])
adjust
subplot(1,2,2)
[~,~,~,~,~,~,~,Sa,~,~,~,V] = Power_Control (Po,1,0,0.2,0.8,1,10,1,0,"SOC",0,2);
plot(Sa,V,'linewidth',2,'Color','black')
xlabel('State of Charge','FontWeight','bold')
ylabel('Voltage','FontWeight','bold')
title('Voltage vs State of Charge Curve')
xlim([0.2 0.8])
rectangle('Position',[y4valz-0.025 3.69 0.05 0.02],'linewidth',2,'EdgeColor','Red')
rectangle('Position',[y2valz-0.025 3.74 0.05 0.02],'linewidth',2,'EdgeColor','Blue')
adjust

%% Figures for Calendar aging
figure
for twice = 1:2
subplot(1,2,twice)
for i = 1:counter
 if i == 1 || i == 4
    m1 = 'Red';
    if i == 1
        m2 = '-';
    else
        m2 = '--';
    end
else
    m1 = 'Blue';
    if i == 4
        m2 = '-';
    elseif i ==3
        m2 = '--';
    end
end
%     plot(tplot(i,Scplot(i,:,3)~=0,1),nonzeros(Scplot(i,:,3)),'linewidth',1.2)
    plot(NickPlot1(i, :, 3)/max(NickPlot1(i, :, 3))*ncycles, NickPlot2(i, :, 3), 'linewidth', 1.2,'LineStyle',m2,'Color',m1);
    hold on
end
legend(s(1:length(vec)))
if twice == 1
title('State of Health (Calendar Aging)')
else
title('Zoomed State of Health')
end
xlabel('Visits','FontWeight','bold')
ylabel('State of Health','FontWeight','bold')
adjust
if twice == 1
rectangle('Position',[5.5*10^6/max(NickPlot1(i, :, 3))*ncycles 0.99 2.5*10^6/max(NickPlot1(i, :, 3))*40 0.0035],'Linewidth',2)
else
xlim([5.5*10^6/max(NickPlot1(i, :, 3))*ncycles 8*10^6/max(NickPlot1(i, :, 3))*ncycles])
ylim([0.99 0.9935])
end
end

figure
subplot(1,3,1)
for i = 1:counter
 if i == 1 || i == 4
    m1 = 'Red';
    if i == 1
        m2 = '-';
    else
        m2 = '--';
    end
else
    m1 = 'Blue';
    if i == 2
        m2 = '-';
    else
        m2 = '--';
    end
end
%     plot(tplot(i,Scplot(i,:,3)~=0,1),nonzeros(Scplot(i,:,3)),'linewidth',1.2)
    plot(NickPlot1(i, :, 3)/max(NickPlot1(i, :, 3))*ncycles, NickPlot2(i, :, 3), 'linewidth', 1.2,'LineStyle',m2,'Color',m1);
    hold on
end
legend(s(1:length(vec)))
if twice == 1
title('SoH for Calendar Aging')
else
title('Zoomed State of Health')
end
xlabel('Visits','FontWeight','bold')
ylabel('State of Health','FontWeight','bold')
adjust
xlim([5.5*10^6/max(NickPlot1(i, :, 3))*ncycles 8*10^6/max(NickPlot1(i, :, 3))*ncycles])
ylim([0.99 0.9935])

subplot(1,3,2)
plot(tplot(2,Saplot(2,:,3)~=0,3)/max(NickPlot1(i, :, 3))*ncycles,nonzeros(Saplot(2,:,3)),'linewidth',2,'Color','Blue')
hold on
plot(tplot(2,Saplot(2,:,3)~=0,3)/max(NickPlot1(i, :, 3))*ncycles,ones(1,length(tplot(2,Saplot(2,:,3)~=0,3)))*y2val,'linewidth',1,'Color','Blue','LineStyle','--')
xlabel('Visits','FontWeight','bold')
ylabel('State of Charge','FontWeight','bold')
adjust
title('State of Charge - Route 2')
xlim([-0.01*10^5/max(NickPlot1(i, :, 3))*ncycles 6.2*10^5/max(NickPlot1(i, :, 3))*ncycles])
ylim([0 1])

subplot(1,3,3)
plot(tplot(4,Saplot(4,:,3)~=0,3)/max(NickPlot1(i, :, 3))*ncycles,nonzeros(Saplot(4,:,3)),'linewidth',2,'Color','Red')
hold on
plot(tplot(4,Saplot(4,:,3)~=0,3)/max(NickPlot1(i, :, 3))*ncycles,ones(1,length(tplot(4,Saplot(4,:,3)~=0,3)))*y4val,'linewidth',1,'Color','Red','LineStyle','--')
xlim([-0.2*10^5/max(NickPlot1(i, :, 3))*40 6.2*10^5/max(NickPlot1(i, :, 3))*40])
xlabel('Visits','FontWeight','bold')
ylabel('State of Charge','FontWeight','bold')
adjust
title('State of Charge - Route 4')
xlim([-0.01*10^5/max(NickPlot1(i, :, 3))*ncycles 6.2*10^5/max(NickPlot1(i, :, 3))*ncycles])
ylim([0 1])

figure
subplot(1,2,1)
for i = 1:counter
 if i == 1 || i == 4
    m1 = 'Red';
    if i == 1
        m2 = '-';
    else
        m2 = '--';
    end
else
    m1 = 'Blue';
    if i == 2
        m2 = '-';
    else
        m2 = '--';
    end
end
%     plot(tplot(i,Scplot(i,:,3)~=0,1),nonzeros(Scplot(i,:,3)),'linewidth',1.2)
    plot(NickPlot1(i, :, 3)/max(NickPlot1(i, :, 3))*ncycles, NickPlot2(i, :, 3), 'linewidth', 1.2,'LineStyle',m2,'Color',m1);
    hold on
end
legend(s(1:length(vec)))
title('State of Health (Calendar Aging)')
xlabel('Visits','FontWeight','bold')
ylabel('State of Health','FontWeight','bold')
adjust
subplot(1,2,2)
plot(tnow2,nonzeros(Saoncep(2,:,1)),'linewidth',2,'Color','blue')
hold on
plot(tnow4,nonzeros(Saoncep(4,:,1)),'linewidth',2,'Color','red')
plot(tnow2,ones(1,length(tnow2))*y2valz,'linewidth',2,'Color','blue','LineStyle','--')
plot(tnow4,ones(1,length(tnow4))*y4valz,'linewidth',2,'Color','red','LineStyle','--')
xlabel('Visits','FontWeight','bold')
ylabel('State of Charge','FontWeight','bold')
title('State of Charge Profiles')
legend('Route 2','Route 4','','')
text(40/max(NickPlot1(2, :, 3))*40,y2valz-0.03,'Mean 2','Color','Blue','FontSize',20,'FontWeight','bold')
text(40/max(NickPlot1(2, :, 3))*40,y4valz-0.03,'Mean 4','Color','Red','FontSize',20,'FontWeight','bold')
xlim([0 max(tnow2)])
ylim([0 1])
adjust
%% Plotting cost
%This part will only show up if different charging stations are compared!
% (i.e. not for velocities)
% if length(vec1)==50
%     counter = 0;
%     for l = 1:length(vec1)
%         counter = counter+1;
% Chealth = (1-Compare(counter,:))/0.2*Cbattery;
% Cost = Ccharging+Chealth;
%
% figure(4)
% hold on
% plot(tvec,Cost,'linewidth',2)
%     end
% figure(4)
% hold on
% s = strings(1,length(vec1)-1);
% for i = 2:length(vec1)
% s(1,i-1) = "dc = "+vec1(i);
% end
% legend(s,'location','southeast')
% xlabel('Time')
% ylabel('Cost')
% title("Comparing "+num2str(vec1(1,1)))
% elseif length(vec2)~=1
%     counter = 1; Cost = zeros(1,length(vec2)-1);
%     for l = 1:length(vec2)-1
%         counter = counter+1;
% Chealth = mean(-(Compare(1,:)-Compare(counter,:))/0.2*Cbattery)*confifactor(1,counter);
% Cost(1,counter-1) = Chealth;
%     end
% figure(4)
% bar(vec2(1,2:end),Cost)
% hold on
% s = strings(1,length(vec2)-1);
% for i = 2:length(vec2)
% s(1,i-1) = "V = "+vec2(i);
% end
% %legend(s,'location','southeast')
% xlabel('V')
% ylabel('Cost')
% title("Comparing V = "+num2str(vec2(1,1))+" for dc = "+num2str(vec1(1,1)))
% end
function [] = adjust()
axis square
set(gca,'FontSize',20)
ax = gca;
ax.TitleFontSizeMultiplier = 1;
end
