
% A constant, singular mass matrix
M = [1 0 0 0
   0 1 0 0
   0 0 0 0
   0 0 0 0];

% Use the LSODI example tolerances.  The 'MassSingular' property is
% left at its default 'maybe' to test the automatic detection of a DAE.
options = odeset('Mass',M,'RelTol',1e-4,'AbsTol',[1e-6 1e-10 1e-6 1e-6]);
z0=1; I0=1;
% Initialisation y(1)=z, y(2)=IR1(t), y(3)=v(t)
y0_1 = [z0,I0*R0(z0),ocv(z0)-I0*R1(z0)-I(z0)*R0(z0),I0];
tspan_1 = linspace(0,0.6);
[t1,y1] = ode15s(@f,tspan_1,y0_1,options);

y0 = y1(end,:);
tspan = linspace(0.6,1.2);
[t2,y2] = ode15s(@f2,tspan,y0,options);

%y0_2 = y2(end,:);
%tspan_2 = linspace(0.4,0.6);
%[t3,y3] = ode15s(@f,tspan_2,y0_2,options);

t = [t1;t2];
y = [y1;y2];







figure(1);
plot(t,y(:,1), 'r.');
ylabel('z');
title('state of charge');
xlabel('t');

figure(2);
plot(t,y(:,2),'g.');
ylabel('Vc1(t)');
title('capacitor voltage');
xlabel('t');

figure(3);
plot(t,y(:,3),'b.');
ylabel('v(t)');
title('voltage');
xlabel('t');

figure(4);
plot(t,y(:,4),'k.');
ylabel('IR1(t)');
title('current');
xlabel('t');
% --------------------------------------------------------------------------



%figure(5)
%fplot(I, [0,0.6]);
%ylabel('I(t)');
%title('current');
%xlabel('t');





function out = f(t,y)
out = [  -I(t)./Q(t)
    I(t)./C1(y(1))-y(4)./C1(y(1))
   y(3) - ocv(y(1))+ y(2)+I(y(1)).*R0(y(1)) 
   y(4)-y(2)./R1(y(1))];
end

function out = f2(t,y)
out = [  -I2(t)./Q(t)
    I2(t)./C1(y(1))-y(4)./C1(y(1))
   y(3) - ocv(y(1))+ y(2)+I2(y(1)).*R0(y(1)) 
   y(4)-y(2)./R1(y(1))];
end

function C = C1(z)
    C = 38*10^(3)*z.^2;
%    C = 38*10^(3);
end
function R = R1(z)
    R = 15.8*10^(-3)*z.^2;
%    R = 15.8*10^(-3);

end
function R = R0(z)
    R = 26*10^(-3)*z.^2;
%    R = 26*10^(-3);

end
function q = Q(t)
    q = 2.9-10^(-6)*t;
%    q = 2.9/60;

end


function ir = I(t)
    if t < 0.2
        ir = 2.9;
    elseif (t>=0.2 & t<0.4)
        ir = 0;
    else
        ir=2.9;
    end
end

function ir = I2(t)
    if t<0.65
        ir=2.9;
    elseif (t < 0.8 & t>=0.65)
        ir = 0;
    elseif (t>=0.8 & t<1)
        ir = 2.9;
    else
        ir=0;
    end
end




function o = ocv(z)
    o = 10.8*z.^5-26.06*z.^4+22.74*z.^3-8.4*z.^2+1.6*z+3.47;
end