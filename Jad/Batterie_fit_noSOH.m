clearvars;
%% INFO
% Output of the code: Error with cross terms is printed in command window,
% error for all aproximations is also printed in a table in the command
% window. The best approximation is drawn and the corresponding coefficients
% are printed last in the command window.

% How to provide data
%-----------------------------------------
%    T  |   SOC  |   R0  |   R1   |  C   |
%    5  |   10   |  5910 |  7850  | 5075 |
%    5  |   20   |  5810 |  6360  | 5981 |
%    .       .       .       .        .
%    .       .       .       .        .
%    .       .       .       .        .
%    5  |   90   |  5850 |  6300  | 5810 |
%   15  |   10   |  ...  |  ....  | .... |
%   15  |   20   |  ...  |  ....  | .... |
%-----------------------------------------
% etc.. (for fixed T, all SOC, then change T, all SOH ...)

%% Required Input
%Provide Data as mentioned above:
Data = [5 10 5910 7850 5075;5 20 5810 6360 5981;5 30 5710 5390 6665;5 40 5610 4480 7207;5 50 5520 3830 7781;5 60 5540 3680 8293;5 70 5360 3770 8476;5 80 5280 4370 8025;5 90 5170 4070 8942;15 10 3490 6220 7823;15 20 3440 4740 9129;15 30 3380 3800 10123;15 40 3310 3190 10653;15 50 3280 3170 11140;15 60 3230 2780 11686;15 70 3220 3520 11726;15 80 3160 3670 10933;15 90 3110 2980 12001;25 10 2880 5360 10126;25 20 2840 3830 11778;25 30 2820 3190 12992;25 40 2760 2400 13689;25 50 2760 2430 14049;25 60 2720 2080 14361;25 70 2700 2810 14406;25 80 2660 2400 13780;25 90 2610 2150 15140;35 10 2466 4613 12573;35 20 2445 3136 14746;35 30 2412 2711 16276;35 40 2347 1886 17081;35 50 2337 1913 17221;35 60 2321 2011 17762;35 70 2318 2368 17727;35 80 2301 2399 16837;35 90 2270 1654 18445;45 10 2340 4010 14846;45 20 2330 3220 17382;45 30 2290 1850 19457;45 40 2290 2140 20348;45 50 2250 1520 20685;45 60 2270 1720 21595;45 70 2230 1600 21373;45 80 2240 1880 20064; 45 90 2230 1900 21977;5 10 6240 10560 4206;5 20 6100 7570 4975;5 30 6020 6500 5515;5 40 5960 5950 6018;5 50 5890 5070 6396;5 60 5870 5250 6835; 5 70 5850 5450 7048;5 80 5780 6520 6508;5 90 5700 5130 7100;15 10 3960 8410 6312;15 20 3860 5550 7496;15 30 3850 5010 8204; 15 40 3860 5110 8607;15 50 3820 4110 9013;15 60 3820 3810 9389;15 70 3840 4330 9430;15 80 3870 5240 8421;15 90 3860 4400 9374;25 10 2870 6134 8350;25 20 2849 4702 9693;25 30 2834 3438 10543;25 40 2842 3266 11006;25 50 2873 3529 11246;25 60 2886 3383 11682;25 70 2907 3792 11577;25 80 2910 3868 10541;25 90 2908 3286 11770;35 10 2065 5861 9925;35 20 2033 3543 11925;35 30 2042 3314 13101;35 40 2044 3122 13513;35 50 2048 2766 13924;35 60 2030 2214 14185;35 70 2062 2800 14134;35 80 2086 3318 13148;35 90 2076 2368 14536;45 10 1834 4711 11914;45 20 1849 3728 13869;45 30 1845 2778 15770;45 40 1855 2901 16178;45 50 1839 2022 16568;45 60 1875 2429 16839;45 70 1905 2737 16783;45 80 1884 2152 15771;45 90 1901 1678 17107;5 10 9224 13033 3641;5 20 8984 8576 4413;5 30 8920 7866 4814;5 40 8871 6588 5246; 5 50 8850 6071 5572;5 60 8867 6166 5879;5 70 8855 5559 6107;5 80 8918 7272 5593; 5 90 8914 6694 5944; 15 10 5692 11605 5084; 15 20 5557 7398 6257; 15 30 5521 6010 6820; 15 40 5510 4860 7292;15 50 5539 4547 7697; 15 60 5595 4268 7958;15 70 5655 4254 8103;15 80 5776 5861 7083;15 90 5835 4597 7728;25 10 3532 10086 6220;25 20 3454 6060 7761;25 30 3453 4894 8417;25 40 3462 3804 9051;25 50 3497 3367 9262;25 60 3566 3339 9532;25 70 3651 3214 9645;25 80 3822 5843 8181;25 90 3879 3609 9097;35 10 2752 7957 7527;35 20 2664 4190 9426;35 30 2599 3211 10161;35 40 2623 2938 10747;35 50 2656 3271 11024;35 60 2604 2576 11212;35 70 2592 2756 11328;35 80 2658 4495 9875;35 90 2686 2864 11224;45 10 1962 7408 8440;45 20 1933 444 10807;45 30 1949 3675 11876;45 40 1871 2588 12585;45 50 1890 2518 12911;45 60 1841 1988 12944;45 70 1932 2491 13521;45 80 1906 2918 12021;45 90 1935 2050 13093];
Data = Data(1:45,:);
%Provide the SOC values (even though they were mentioned in DATA)
SOCvals = [10 20 30 40 50 60 70 80 90];
%Provide the T values (even though they were mentioned in DATA)
Tvals = [5 15 25 35 45];
%This specifies what we want to approximate (3 for R0, 4 for R1, 5 for C1)
Which_Data = 5;
%Pvec shows the order of approximation (i.e. [1 1] means first order in T,
% first order in SOC), I only included up to order 4 but feel free to add
% more if you want.
pvec = [1 1;1 2;2 1;2 2;1 3;2 3;3 1;3 2;3 3;1 4;2 4;3 4;4 1;4 2;4 3;4 4];


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%        You shouldn't have to change anything after this point          %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%% Creating X,Y (grid for T and SOC values) and Z(R values)
ls = length(SOCvals);
lt = length(Tvals);
X = ones(ls,lt);
for i = 1:lt
X(:,i) = X(:,i)*Tvals(1,i);
end
Y = ones(ls,lt);
for i = 1:ls
Y(i,:) = Y(i,:)*SOCvals(1,i);
end
Z1 = zeros(ls,lt);
for i =1:lt
Z1(:,i) = Data(1+ls*(i-1):ls+ls*(i-1),Which_Data);
end

%% Fitting
result = zeros(max(max(pvec)),1); %This will store the error's norm
X_p = [Data(:,1:2)];
Y_p = Data(:,Which_Data);

nomin = inf;
cb = 0;
check = 0;

for z = 1:length(pvec)+1
    if z == length(pvec)+1
        z = 4; %The value Z = 4 is done twice because the second time we consider croos-terms
        check = 1;
    end
pl = pvec(z,:);
p1 = pl(1,1);
p2 = pl(1,2);
[f,fm] = cr_f(p1,p2,check); %Crf creates the function used to aproximate the fitting
fn = @(b,x) 0;
fmn = @(b,X,Y) 0;
for m = 1:length(f)
 fn = @(b,x) fn(b,x)+f{m}(b,x);
 fmn = @(b,X,Y) fmn(b,X,Y)+fm{m}(b,X,Y);
end
I = ones(p1+p2+1+check,1)*0.1;
[Beta,r]=nlinfit(X_p,Y_p,fn,I); %Fitting with number of coefficients specified
no = norm(fmn(Beta,X,Y)-Z1)/mean(Data(:,Which_Data)); %Error/mean
if no<nomin %Getting the one with the least error
    nomin = no;
    Bmin = Beta;
    rmin = r;
    fmnmin = fmn;
    pmin = [p1 p2];
end
if check == 0
result(z,1) = no;
else
result_cross = no;
clc
fprintf('With cross terms error is: %f\n',no)
end
if check == 1
    break
end
end

%% Plotting
surf(X,Y,Z1,'FaceColor',[1 0 0])
hold on
surf(X,Y,fmnmin(Bmin,X,Y),'FaceColor',[0 1 0])
view([1 1 1])
xlabel('Temperature')
ylabel('SOC')
zlabel('Resistance')
str = "Approximation ("+num2str(pmin(1,1))+" in T and "+num2str(pmin(1,2))+" in SOC)";
legend('Exact',str);
T_order = pvec(:,1);
SOC_order = pvec(:,2);
error = result;
T = table(T_order,SOC_order,error)
fprintf("Best approximation is "+num2str(pmin(1,1))+" in T and "+num2str(pmin(1,2))+" in SOC\n")
fprintf("Coefficients for cte, T,SOC,T^2,SOC^2... respectively are:\n")
for i = 1:length(Bmin)
    fprintf(num2str(Bmin(i))+"\n")
end

%% Funtcions
function [f,fm] = cr_f(p1,p2,q)
f{1} = @(b,x) b(1);
fm{1} = @(b,X,Y) b(1);
counter = 2;
    for z= 1:max(p1,p2)
        if z<=p1
        f{counter} = @(b,x)b(counter)*x(:,1).^z;
        fm{counter} = @(b,X,Y)b(counter)*X.^z;
        counter = counter+1;
        end
        if z<=p2
        f{counter} = @(b,x) b(counter)*x(:,2).^z;
        fm{counter} = @(b,X,Y) b(counter)*Y.^z;
        counter = counter+1;
        end
        if q == 1
            if (p1~=p2)
                error('Ps should be equal 2!')
            end
        f{counter} = @(b,x) b(counter)*x(:,1).*x(:,2);
        fm{counter} = @(b,X,Y,o) b(counter)*X.*Y;
        end
    end
end
