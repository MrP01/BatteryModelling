function [tvec,Savec,Sbvec,Scvec,Sdvec,SOH_OF_EACH_TRIP,tzella,Sazella,tonce,Saonce]= First_Scenario(check,cycles,C1,Po,zi,zc,I0,T0,h0,c0,tc,tgi,stay,home,ti,tg,tvec,tzella,Sazella,Savec,Sbvec,Scvec,Sdvec,c,zopt)
SOH_OF_EACH_TRIP = zeros([3 cycles]);
if check ==1
for cycle = 1:cycles
    if cycle == 1
        z0 = zi;
    end
[z0,I0,T0,h0,c0,~,t1,S1a,S1b,S1c,S1d] = Power_Control (Po,1,ti,ti+tc,z0,I0,T0,h0,c0,"Time",0,c);
[z0,I0,T0,h0,c0,tf2,t2,S2a,S2b,S2c,S2d] = Power_Control (-C1,0,ti+tc,zc,z0,I0,T0,h0,c0,"SOC",0,c);
charging_time = tf2-(tc+ti);
[z0,I0,T0,h0,c0,~,t3,S3a,S3b,S3c,S3d] = Power_Control (Po,1,tf2,tg+charging_time,z0,I0,T0,h0,c0,"Time",0,c);
[z0,I0,T0,h0,c0,~,t4,S4a,S4b,S4c,S4d] = Power_Control (0,0,tg+charging_time,tg+charging_time+stay,z0,I0,T0,h0,c0,"Time",0,c);
[z0,I0,T0,h0,c0,~,t5,S5a,S5b,S5c,S5d] = Power_Control (Po,1,tg+charging_time+stay,tgi+tg+charging_time+stay,z0,I0,T0,h0,c0,"Time",0,c);
% if z0<zopt
% [z0,I0,T0,h0,c0,tf3,t6,S6a,S6b,S6c,S6d] = Power_Control (-1,0,tgi+tg+charging_time+stay,zopt,z0,I0,T0,h0,c0,"SOC",0,c);
% else
    t6 = []; S6a = []; S6b = []; S6c= []; S6d=[]; tf3=tgi+tg+charging_time+stay;
% end
[z0,I0,T0,h0,c0,~,t7,S7a,S7b,S7c,S7d] = Power_Control (0,0,tf3,tf3+home,z0,I0,T0,h0,c0,"Time",0,c);
[z0,I0,T0,h0,c0,~,t8,S8a,S8b,S8c,S8d] = Power_Control (-1,0,tf3+home,zi,z0,I0,T0,h0,c0,"SOC",0,c);
ti = t8(end,1); tg = tgi+t8(end,1);
if cycle == 1
    tonce = [t1;t2;t3;t5;t6;t8]; Saonce = [S1a;S2a;S3a;S5a;S6a;S8a];
end
tvec = [tvec;t1;t2;t3;t4;t5;t6;t7;t8]; Savec = [Savec;S1a;S2a;S3a;S4a;S5a;S6a;S7a;S8a];
tzella = [tzella;t1;t2;t3;t5;t6;t8]; Sazella = [Sazella;S1a;S2a;S3a;S5a;S6a;S8a];
Sbvec = [Sbvec;S1b;S2b;S3b;S4b;S5b;S6b;S7b;S8b]; Scvec = [Scvec;S1c;S2c;S3c;S4c;S5c;S6c;S7c;S8c];
Sdvec = [Sdvec;S1d;S2d;S3d;S4d;S5d;S6d;S7d;S8d];
SOH_OF_EACH_TRIP(1, cycle) = ti;
SOH_OF_EACH_TRIP(2, cycle) = S8c(end, 1);
SOH_OF_EACH_TRIP(3, cycle) = S8b(end, 1);
end
else
for cycle = 1:cycles
    if cycle == 1
        z0 = zi;
    end
[z0,I0,T0,h0,c0,~,t1,S1a,S1b,S1c,S1d] = Power_Control (Po,1,ti,ti+tgi,z0,I0,T0,h0,c0,"Time",0,c);
[z0,I0,T0,h0,c0,~,t2,S2a,S2b,S2c,S2d] = Power_Control (0,0,ti+tgi,ti+tgi+stay,z0,I0,T0,h0,c0,"Time",0,c);
[z0,I0,T0,h0,c0,~,t3,S3a,S3b,S3c,S3d] = Power_Control (Po,1,ti+tgi+stay,ti+tgi+stay+tc-tgi,z0,I0,T0,h0,c0,"Time",0,c);
[z0,I0,T0,h0,c0,tf2,t4,S4a,S4b,S4c,S4d] = Power_Control (-C1,0,ti+tgi+stay+tc-tgi,zc,z0,I0,T0,h0,c0,"SOC",0,c);
[z0,I0,T0,h0,c0,~,t5,S5a,S5b,S5c,S5d] = Power_Control (Po,1,tf2,2*tgi-tc+tf2,z0,I0,T0,h0,c0,"Time",0,c);
% if z0<zopt
% [z0,I0,T0,h0,c0,tf3,t6,S6a,S6b,S6c,S6d] = Power_Control (-1,0,2*tgi-tc+tf2,zopt,z0,I0,T0,h0,c0,"SOC",0,c);
% else
    t6 = []; S6a = []; S6b = []; S6c= []; S6d=[]; tf3 = 2*tgi-tc+tf2;
% end
[z0,I0,T0,h0,c0,~,t7,S7a,S7b,S7c,S7d] = Power_Control (0,0,tf3,tf3+home,z0,I0,T0,h0,c0,"Time",0,c);
[z0,I0,T0,h0,c0,~,t8,S8a,S8b,S8c,S8d] = Power_Control (-1,0,tf3+home,zi,z0,I0,T0,h0,c0,"SOC",0,c);
ti = t8(end,1);
tvec = [tvec;t1;t2;t3;t4;t5;t6;t7;t8]; Savec = [Savec;S1a;S2a;S3a;S4a;S5a;S6a;S7a;S8a];
Sbvec = [Sbvec;S1b;S2b;S3b;S4b;S5b;S6b;S7b;S8b]; Scvec = [Scvec;S1c;S2c;S3c;S4c;S5c;S6c;S7c;S8c];
tzella = [tzella;t1;t3;t4;t5;t6;t8]; Sazella = [Sazella;S1a;S3a;S4a;S5a;S6a;S8a];
Sdvec = [Sdvec;S1d;S2d;S3d;S4d;S5d;S6d;S7d;S8d];
if cycle == 1
    tonce = [t1;t3;t4;t5;t6;t8]; Saonce = [S1a;S3a;S4a;S5a;S6a;S8a];
end
SOH_OF_EACH_TRIP(1, cycle) = ti;
SOH_OF_EACH_TRIP(2, cycle) = S8c(end, 1);
SOH_OF_EACH_TRIP(3, cycle) = S8b(end, 1);
end
end
end
