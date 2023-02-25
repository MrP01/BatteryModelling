function [ze,Ie,Te] = Power_Control (Pow,check,ti,fval,z0,I0,T0,s)

%Pow specifies either current or power
%Check is 1 for power control and 0 for current control
%ti is the initial time
%tf is either final time or final SOC, this is determined by s = "Time" for
%the first and SOC for the latter
%All other entries are intial conditions, the function outputs are final
%conditions which will be used as initial conditions in the next simulation

%Note: for calendar aging only, specify current = 0 with current control!

% A constant, singular mass matrix
M = @(t,y)[1 0 0 0 0 0 0 0%SOC 
   0 1 0 0 0 0 0 0
   0 0 0 0 0 0 0 0
   0 0 0 0 0 0 0 0
   0 0 0 0 0 0 0 0
   0 0 0 0 0 0 0 0
   2.9*0.2*Temp_C(y(5))*t*(8*y(1)-4*1.3) 0 0 0 0 varyM1(y(6),y(8)/3600,check,Pow)  1 varyM2(y(6),check,Pow)
   0 0 0 0 0 0 0 1];

% Use the LSODI example tolerances.  The 'MassSingular' property is
% left at its default 'maybe' to test the automatic detection of a DAE.
if s == "Time"
tf = fval;
options = odeset('Mass',M,'RelTol',1e-4,'AbsTol',[1e-6 1e-10 1e-6 1e-6 1e-6 1e-6 1e-6 1e-6],'MStateDependence','strong');
elseif s == "SOC"
tf = 100000;
options = odeset('Mass',M,'RelTol',1e-4,'AbsTol',[1e-6 1e-10 1e-6 1e-6 1e-6 1e-6 1e-6 1e-6],'MStateDependence','strong','Events',@myEvent);
else
    error('Wrong string inserted')
end
%I0=1; T0=10; %wrong initial condition - ;
% Initialisation y(1)=z, y(2)=VC1(t), y(3)=v(t), y(4)=IR1(t), y(5)=T(t), y(6)=I(t),
if check == 1
IC = Pow./ocv(z0);
else
IC = Pow;
end
y0_1 = [z0,I0*R0(T0,z0),ocv(z0)-I0*R1(T0,z0)-Pow./ocv(z0)*R0(T0,z0),I0, T0, IC,2.9,0];

tspan_1 = linspace(ti,tf);
[t1,y1] = ode15s(@f,tspan_1,y0_1,options);
ze = y1(end,1); Ie = y1(end,4); Te = y1(end,5);

% figure(1);
% plot(t1,y1(:,1), 'r.-');
% ylabel('z');
% title('state of charge');
% xlabel('t');
% % 
% figure(2);
% plot(t1,y1(:,2),'g.-');
% ylabel('Vc1(t)');
% title('capacitor voltage');
% xlabel('t');
% 
% figure(3);
% plot(t1,y1(:,3),'b.-');
% ylabel('v(t)');
% title('voltage');
% xlabel('t');
% 
% figure(4);
% plot(t1,y1(:,4),'k.-');
% ylabel('IR1(t)');
% title('current');
% xlabel('t');
% 
% figure(5);
% plot(t1,y1(:,5),'y.-');
% ylabel('T(t)');
% title('temperature');
% xlabel('t');
% % 
% figure(6);
% plot(t1,y1(:,6),'y.-');
% ylabel('I(t)');
% title('Current');
% xlabel('t');
% 
% figure(7);
% plot(t1,y1(:,7),'y.-');
% ylabel('Q(t)');
% title('Capacity');
% xlabel('t');
% 
% figure(8);
% plot(t1,y1(:,8)/3600,'y.-');
% ylabel('C');
% title('Cycle');
% xlabel('t');
%--------------------------------------------------------------------------





% h = @(t) (t-rem(t,6.048e5))./6.048e5;
% fplot(h,[0,2*6.048e5],'g.')


function out = f(~,y)
out = [  -y(6)./y(7)/3600
    y(6)./C1(y(5),y(1))-y(4)./C1(y(5),y(1))
   y(3) - ocv(y(1))+ y(2)+y(6).*R0(y(5),y(1)) 
   y(4)-y(2)./R1(y(5),y(1))
   y(5)-10
   equ(Pow,y(6),y(3),check)
   -2.9*0.2*Temp_C(y(5))*(4*y(1).^2-4*1.3*y(1)+1.3^2+1)
   0.5*abs(y(6))./y(7)];
end

function [m] = equ (Pow,x1,x2,check)
    if check == 1 
    m = x1-Pow/x2;
    else
    m = x1-Pow;
    end
end

function C = C1(T,z)
    C = 1.0888e3*T+2.672979e4*z+5.54102e3;
end

function R = R1(T,z)
    R = -8.51e-4*T-3.6102e-2*z+0.05847;
end

function R = R0(T,z)
    R = -1.297e-3*T-4.26e-3*z+6.4201e-2;
end

function o = ocv(z)
    o = 10.8*z.^5-26.06*z.^4+22.74*z.^3-8.4*z.^2+1.6*z+3.47;
end

function [m] = varyM1 (y6,y8,check,Pow)
    if check == 0 && Pow == 0
     m = 0;
    else
     m =  DCSF(y6)*2.9*4.58*10^-4*y8/CSF(y6);
    end
end

function [m] = varyM2 (y6,check,Pow)
    if check == 0 && Pow == 0
     m = 0;
    else
     m =  2.9*4.58*10^-4/3600/CSF(y6);
    end
end

function [m] = CSF(I)
    m = 1.01576599-exp(0.88279821*I/2.9-5.06803394);
    if m>1
        m = 1;
    elseif m <0
        m = 0;
    end
end

function [m] = DCSF(I) %Derivative of CSF
m = 0.8827982/2.9*exp(0.88279821*I/2.9-5.06893394);
if CSF(I)>1
    m = 0;
elseif CSF(I)<0
    m = 0;
end
end

function [m] = Temp_C (T)
    if T>20
        m = 3.805*10^-7;
    else
        m = 3.171*10^-8;
    end
end

function [value, isterminal, direction] = myEvent(~, Y)
value      = abs((Y(1) - fval))<=0.005;
isterminal = 1;   % Stop the integration
direction  = 0;
end
end