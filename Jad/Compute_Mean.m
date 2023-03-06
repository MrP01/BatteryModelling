function [y1val,y2val,y3val,y4val,Error] = Compute_Mean(t1,t2,t3,t4,S1,S2,S3,S4)
min1 = min(t1(1,end),t2(1,end));
min2 = min(t3(1,end),t4(1,end));
xval = 0:1:min(min1,min2);
isDuplicate = diff(t1)==0;
t1(isDuplicate) = []; 
S1(isDuplicate) = []; 
yval = interp1(t1,S1,xval);
y1val = mean(yval);
isDuplicate = diff(t2)==0;
t2(isDuplicate) = []; 
S2(isDuplicate) = []; 
yval = interp1(t2,S2,xval);
y2val = mean(yval);
isDuplicate = diff(t3)==0;
t3(isDuplicate) = []; 
S3(isDuplicate) = []; 
yval = interp1(t3,S3,xval);
y3val = mean(yval);
isDuplicate = diff(t4)==0;
t4(isDuplicate) = []; 
S4(isDuplicate) = []; 
yval = interp1(t4,S4,xval);
y4val = mean(yval);
Error = abs((y1val-y2val)/y1val)*100;

end