ocv = @(z) 10.8 * z.^5 - 26.06 * z.^4 + 22.74 * z.^3 - 8.4 * z.^2 + 1.6 * z + 3.47;
iR1 = @(t) 2.899 * square(2 * pi * t / (60 * 60)) * pulse(t - 5 * 60) * pulse(20 * 60 - t);
iR1(6 * 60)
%%

figure(1)
fplot(iR1, [0, 3600]);
title('Input Current vs time');
xlabel('t');
ylabel('iR1(t)')
%%

%R1=4197*10^(-6); C1=1099; R0=3701*10^(-6); z0=1; Q=2.9/60;
R1 = 15.8 * 10^(-3); C1 = 38 * 10^(3); R0 = 26 * 10^(-3); z0 = 1; Q = 2.9/3600; %Q=2.9/3600;

%z = @(t) z0-1/Q*sin(t);
z = @(t) z0 - 1 / Q * 2.899 * (t - 5 * 60) * pulse(t - 5 * 60) * pulse(20 * 60 - t);

[t, itot] = ode45(@vdp1, [0 3600], 1);
zeval = zeros(1, length(t));

for i = 1:length(t)
    zeval(i) = z(t(i));
end

figure(1)
plot(t, itot);
title('Total current vs time');
xlabel('t');
ylabel('i(t)')
%%
% Voltage

v = zeros(1, length(t));

for i = 1:length(t)
    v(i) = ocv(z(t(i))) - R1 * iR1(t(i)) - R0 * itot(i);
end

figure(2)
plot(t, v);
title('Total voltage vs time');
xlabel('t');
ylabel('v(t)');
%%
figure(3)
plot(t, zeval, 'g');
title('SOC vs time')

xlabel('t');
ylabel('z(t)')
%%
function didt = vdp1(t, itot)
    R1 = 15.8 * 10^(-3); C1 = 38 * 10^(3); R0 = 26 * 10^(-3); z0 = 1; Q = 2.9/3600; %Q=2.9/3600;

    iR1 = @(t) 2.899 * square(2 * pi * t / (60 * 60)) * pulse(t - 5 * 60) * pulse(20 * 60 - t);
    didt = -1 / (R1 * C1) * iR1(t) + 1 / (R1 * C1) * itot;
end

function x = pulse(t)

    if t >= 0
        x = 1;
    else
        x = 0;
    end

end
