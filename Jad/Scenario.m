clc;
clearvars;
close all;
dt = 220; % Total distance (to granny*2)
vec1 = [40 80 140]; % Distances of charging stations
C1 = ones(1, length(vec1)); % Charging rate of stations
Co1 = [15 10 15 10]; % Cost of charging in stations
Cbattery = 3000; % Cost of a battery
vec2 = 80; % Speeds to test on
ncycles = 5; % number of cycles to test
confifactor = (1 - (abs(vec2(1, 1) - 80) / 80)) * exp(-(vec2 - 80).^2 / 2200);
if length(vec1) > 1
    vec = vec1;
    name = "dc";
else
    vec = vec2;
    name = "V";
end
counter4 = 0;
for stays = 3:3
    counter4 = counter4 + 1;
    counter3 = 0;
    for calendar = 0:2
        counter3 = counter3 + 1;
        counter = 0;
        counter2 = 0;
        for dc = vec1
            counter = counter + 1;
            for v = vec2
                counter2 = counter2 + 1;
                %% Required Power from velocity
                r = 0.135;
                N = 25 / (3 * pi) / r * v;
                Pgrid = 0:1000:7000;
                Pdata = [0  24.9  49 73.5 91 95 90 82];
                p1 = polyfit(Pgrid, Pdata, 2);
                % figure
                P = @(v) p1(1, 1) * v^2 + p1(1, 2) * v + p1(1, 3);
                % fplot(P,[0 7000])
                Po = P(N) / 60;

                %% Model
                zi = 0.8;
                zc = 0.9;
                I0 = 1;
                T0 = 10;
                h0 = 1;
                c0 = 0;
                tc = dc / v * 3600;
                tgi = dt / 2 / v * 3600;
                stay = 24 * 3600 * (7 - stays);
                home = 24 * 3600 * stays;
                ti = 0;
                tg = tgi;
                tvec = [];
                Savec = [];
                Sbvec = [];
                Scvec = [];
                Sdvec = [];
                if dc > dt / 2
                    check = 0;
                else
                    check = 1;
                end
                [tvec, Savec, Sbvec, Scvec, Sdvec] = First_Scenario(check, ncycles, C1(1, counter), Po, zi, zc, I0, T0, h0, c0, tc, tgi, stay, home, ti, tg, tvec, Savec, Sbvec, Scvec, Sdvec, calendar, 0.6);

                tplot(counter, 1:length(tvec), counter3) = tvec;
                Saplot(counter, 1:length(tvec), counter3) = Savec;
                Sbplot(counter, 1:length(tvec), counter3) = Sbvec;
                Scplot(counter, 1:length(tvec), counter3) = Scvec;
                Sdplot(counter, 1:length(tvec), counter3) = Sdvec;

            end
        end
    end
    Percentage(counter4, 1) = mean((ones - nonzeros(Scplot(1, :, 1))) ./ (ones - nonzeros(Scplot(1, :, 2)))) * 100;
end

%% Plotting

for num = 1:3
    figure;
    if num == 1 || num == 2
        subplot(1, 2, 1);
    elseif num == 3
        subplot(1, 3, 1);
    end

    for i = 1:counter
        plot(tplot(i, Scplot(i, :, 1) ~= 0, 1), nonzeros(Scplot(i, :, num)));
        hold on;
    end
    s = strings(1, length(vec));
    for i = 1:length(vec)
        s(1, i) = name + " = " + vec(i);
    end
    legend(s(1:length(vec)));
    if num == 1
        title('Cycle Aging');
    elseif num == 2
        title('Both Aging');
    else
        title('Calendar Aging');
    end
    xlabel('Time');
    ylabel('SOH');
    if num == 1 || num == 2
        subplot(1, 2, 2);
        for i = 1:counter
            plot(tplot(i, Sbplot(i, :, 1) ~= 0, 1), nonzeros(Sbplot(i, :, num)));
            hold on;
        end
        s = strings(1, length(vec));
        for i = 1:length(vec)
            s(1, i) = name + " = " + vec(i);
        end
        legend(s(1:length(vec)));
        if num == 1
            title('Cycle Aging');
        elseif num == 2
            title('Both Aging');
        end
        xlabel('Time');
        ylabel('Cycles');
    elseif num == 3
        subplot(1, 3, 2);
        plot(tplot(1, Saplot(1, :, 3) ~= 0, 3), nonzeros(Saplot(1, :, 3)));
        hold on;
        [y1val, y2val, Error] = Compute_Mean(tplot(1, Saplot(1, :, 3) ~= 0, 3), tplot(end, Saplot(end, :, 3) ~= 0, 3), nonzeros(Saplot(1, :, 3)), nonzeros(Saplot(end, :, 3)));
        plot(tplot(1, Saplot(1, :, 3) ~= 0, 3), ones(1, length(tplot(1, Saplot(1, :, 3) ~= 0, 3))) * y1val);
        ylim([0 1]);
        xlabel('Time');
        ylabel('SOC');
        title("dc = " + num2str(vec1(1, 1)) + " Calendar Aging");
        subplot(1, 3, 3);
        plot(tplot(end, Saplot(end, :, 3) ~= 0, 3), nonzeros(Saplot(end, :, 3)));
        hold on;
        plot(tplot(end, Saplot(end, :, 3) ~= 0, 3), ones(1, length(tplot(end, Saplot(end, :, 3) ~= 0, 3))) * y2val);
        xlabel('Time');
        ylabel('SOC');
        title("dc = " + num2str(vec1(1, end)) + " Calendar Aging");
        ylim([0 1]);
    end
end

%% Plotting cost
% This part will only show up if different charging stations are compared!
% (i.e. not for velocities)
if length(vec1) == 50
    counter = 0;
    for l = 1:length(vec1)
        counter = counter + 1;
        Chealth = (1 - Compare(counter, :)) / 0.2 * Cbattery;
        Cost = Ccharging + Chealth;

        figure(4);
        hold on;
        plot(tvec, Cost, 'linewidth', 2);
    end
    figure(4);
    hold on;
    s = strings(1, length(vec1) - 1);
    for i = 2:length(vec1)
        s(1, i - 1) = "dc = " + vec1(i);
    end
    legend(s, 'location', 'southeast');
    xlabel('Time');
    ylabel('Cost');
    title("Comparing " + num2str(vec1(1, 1)));
elseif length(vec2) ~= 1
    counter = 1;
    Cost = zeros(1, length(vec2) - 1);
    for l = 1:length(vec2) - 1
        counter = counter + 1;
        Chealth = mean(-(Compare(1, :) - Compare(counter, :)) / 0.2 * Cbattery) * confifactor(1, counter);
        Cost(1, counter - 1) = Chealth;
    end
    figure(4);
    bar(vec2(1, 2:end), Cost);
    hold on;
    s = strings(1, length(vec2) - 1);
    for i = 2:length(vec2)
        s(1, i - 1) = "V = " + vec2(i);
    end
    % legend(s,'location','southeast')
    xlabel('V');
    ylabel('Cost');
    title("Comparing V = " + num2str(vec2(1, 1)) + " for dc = " + num2str(vec1(1, 1)));
end
%%
for num = 3
    figure;
    if num == 1 || num == 2
        subplot(1, 2, 1);
    elseif num == 3
        subplot(1, 3, 1);
    end

    for i = 1:counter
        plot(tplot(i, Scplot(i, :, 1) ~= 0, 1), nonzeros(Scplot(i, :, num)));
        hold on;
    end
    s = strings(1, length(vec));
    for i = 1:length(vec)
        s(1, i) = name + " = " + vec(i);
    end
    legend(s(1:length(vec)));
    if num == 1
        title('Cycle Aging');
    elseif num == 2
        title('Both Aging');
    else
        title('Calendar Aging');
    end
    xlabel('Time');
    ylabel('SOH');
end
