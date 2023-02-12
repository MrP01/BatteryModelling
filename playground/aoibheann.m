% A constant, singular mass matrix
M = [1 0 0
   0 1 0
   0 0 0];

% Use the LSODI example tolerances.  The 'MassSingular' property is
% left at its default 'maybe' to test the automatic detection of a DAE.
options = odeset('Mass',M,'RelTol',1e-4,'AbsTol',[1e-6 1e-10 1e-6]);

% Initialisation y(1)=z, y(2)=IR1(t), y(3)=v(t)
y0_1 = [1,1,4.11];
tspan_1 = linspace(0,2);
[t,y] = ode15s(@f,tspan_1,y0_1,options);

%y0 = y1(end,:)
%tspan = linspace(0.1,0.2)



%[t2,y2] = ode15s(@f,tspan,y0,options);
%t = [t1;t2];
%y = [y1;y2];







figure(1);
plot(t,y(:,1), 'bo');
ylabel('z');
title('state of charge');
xlabel('t');

figure(2);
plot(t,y(:,2));
ylabel('I(t)');
title('current');
xlabel('t');

figure(3);
plot(t,y(:,3));
ylabel('v(t)');
title('voltage');
xlabel('t');
% --------------------------------------------------------------------------


%iR2 = @(t) 1+square(t);
%fplot(iR2)




function out = f(t,y)
out = [  -I(t).\Q(t)
    -1\(R1(y(1)).*C1(y(1))).*y(2)+1\(R1(y(1)).*C1(y(1))).*I(t)
   y(3) - ocv(y(1))+ y(2).*R1(y(1))+I(y(1)).*R0(y(1))  ];
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
    q = 2.9/60-10^(-6)*t;
%    q = 2.9/60;

end


function ir = I(t)
    ir = 1;
end



function o = ocv(z)
    o = 10.8*z.^5-26.06*z.^4+22.74*z.^3-8.4*z.^2+1.6*z+3.47;
end