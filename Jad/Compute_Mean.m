function [y1val,y2val,Error] = Compute_Mean(t1,t2,S1,S2)
xval = 0:100:min(t1(1,end),t2(1,end));
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
Error = abs((y1val-y2val)/y1val)*100;
end