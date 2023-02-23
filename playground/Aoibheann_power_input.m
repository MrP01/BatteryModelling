
% A constant, singular mass matrix
M = [1 0 0 0 0 0
   0 1 0 0 0 0
   0 0 0 0 0 0
   0 0 0 0 0 0
   0 0 0 0 0 0
   0 0 0 0 0 0];

% Use the LSODI example tolerances.  The 'MassSingular' property is
% left at its default 'maybe' to test the automatic detection of a DAE.
options = odeset('Mass',M,'RelTol',1e-4,'AbsTol',[1e-6 1e-10 1e-6 1e-6 1e-6 1e-6]);
z0=1; I0=1; T0=10; %wrong initial condition - ;
% Initialisation y(1)=z, y(2)=VC1(t), y(3)=v(t), y(4)=IR1(t), y(5)=T(t), y(6)=I(t),
% y(6) = P(t) power = I(t)v(t)
y0_1 = [z0,I0*R0(T0,z0),ocv(z0)-I0*R1(T0,z0)-P(0)./ocv(z0)*R0(T0,z0),I0, T0, P(0)/(ocv(z0))];
tspan_1 = linspace(0,7.2e3);
[t1,y1] = ode15s(@f,tspan_1,y0_1,options);

y0 = y1(end,:);
%Charging to zc=1
y0(1)=1;
tspan = linspace(7.2e3,1.6e4);
[t2,y2] = ode15s(@f2,tspan,y0,options);

%y0_2 = y2(end,:);
%tspan_2 = linspace(20,30);
%[t3,y3] = ode15s(@f,tspan_2,y0_2,options);

t = [t1;t2];
y = [y1;y2];







figure(1);
plot(t,y(:,1), 'r.-');
ylabel('z');
title('state of charge');
xlabel('t');

figure(2);
plot(t,y(:,2),'g.-');
ylabel('Vc1(t)');
title('capacitor voltage');
xlabel('t');

figure(3);
plot(t,y(:,3),'b.-');
ylabel('v(t)');
title('voltage');
xlabel('t');

figure(4);
plot(t,y(:,4),'k.-');
ylabel('IR1(t)');
title('current');
xlabel('t');

figure(5);
plot(t,y(:,5),'y.-');
ylabel('T(t)');
title('temperature');
xlabel('t');

figure(6);
plot(t,y(:,6),'y.-');
ylabel('I(t)');
title('Current');
xlabel('t');
% --------------------------------------------------------------------------



%figure(5)
%fplot(I, [0,0.6]);
%ylabel('I(t)');
%title('current');
%xlabel('t');


%h = @(t) (t-rem(t,6.048e5))./6.048e5;
%fplot(h,[0,2*6.048e5],'g.')


%Defining function for system of ODEs
function out = f(t,y)
out = [  -y(6)./Q(y(5),t)
    y(6)./C1(y(5),y(1))-y(4)./C1(y(5),y(1))
   y(3) - ocv(y(1))+ y(2)+y(6).*R0(y(5),y(1))
   y(4)-y(2)./R1(y(5),y(1))
   y(5)-10-1e-6*t
   y(6)-P(t)./y(3)];
end

function out = f2(t,y)
out = [  -y(6)./Q(y(5),t)
    y(6)./C1(y(5),y(1))-y(4)./C1(y(5),y(1))
   y(3) - ocv(y(1))+ y(2)+y(6).*R0(y(5),y(1))
   y(4)-y(2)./R1(y(5),y(1))
   y(5)-10-1e-6*t
   y(6)-P2(t)./y(3)];
end

%Function defining capacitance
function C = C1(T,z)
    C = 1.0888e3*T+2.672979e4*z+5.54102e3;
end

%Function defining R1
function R = R1(T,z)
    R = -8.51e-4*T-3.6102e-2*z+0.05847;
end

%Function defining R0
function R = R0(T,z)
    R = -1.297e-3*T-4.26e-3*z+6.4201e-2;
end

%Function defining Capacity using cycles
function q = Q(T,t)
    q = 2.9*(1-4.58e-4*cycle(t)-exp(5.07e-2*(cycle(t)-600)))*g(T,t);
end
%function T0 = T(t)
%    T0 = 10+10^(-6)*t;
%end

%Function defining cycles set to charge every 2 hours
function c = cycle(t)
    c = (t-mod(t,7.2e3))/7.2e3;
end

%Function called in capacity function
function fn = g(T,t)
    if T > 20
        fn = 1-0.2*t./(2.592e6);
    else
        fn = 1-0.2*t./(9.4608e8);
    end
end

%Power function
function ir = P(t)
    ir = 1e-3;
end
function ir = P2(t)
    ir = 1e-3;
end

%Function defining ocv voltage
function o = ocv(z)
    o = 10.8*z.^5-26.06*z.^4+22.74*z.^3-8.4*z.^2+1.6*z+3.47;
end
