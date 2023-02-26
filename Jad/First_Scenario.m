function [tvec,Savec,Sbvec,Scvec]= First_Scenario(check,cycles,C1,Po,zi,zc,I0,T0,h0,c0,tc,tgi,stay,home,ti,tg,tvec,Savec,Sbvec,Scvec)  
if check ==1
for cycle = 1:cycles
[z0,I0,T0,h0,c0,~,t1,S1a,S1b,S1c] = Power_Control (Po,1,ti,ti+tc,zi,I0,T0,h0,c0,"Time");
[z0,I0,T0,h0,c0,tf2,t2,S2a,S2b,S2c] = Power_Control (-C1,0,ti+tc,zc,z0,I0,T0,h0,c0,"SOC");
charging_time = tf2-(tc+ti);
[z0,I0,T0,h0,c0,~,t3,S3a,S3b,S3c] = Power_Control (Po,1,tf2,tg+charging_time,z0,I0,T0,h0,c0,"Time");
[z0,I0,T0,h0,c0,~,t4,S4a,S4b,S4c] = Power_Control (0,0,tg+charging_time,tg+charging_time+stay,z0,I0,T0,h0,c0,"Time");
[z0,I0,T0,h0,c0,~,t5,S5a,S5b,S5c] = Power_Control (Po,1,tg+charging_time+stay,tgi+tg+charging_time+stay,z0,I0,T0,h0,c0,"Time");
[z0,I0,T0,h0,c0,~,t6,S6a,S6b,S6c] = Power_Control (0,0,tgi+tg+charging_time+stay,tgi+tg+charging_time+stay+home,z0,I0,T0,h0,c0,"Time");
[~,~,~,~,~,~,t7,S7a,S7b,S7c] = Power_Control (-1,0,tgi+tg+charging_time+stay+home,zi,z0,I0,T0,h0,c0,"SOC");
ti = t7(end,1); tg = tgi+t7(end,1);
tvec = [tvec;t1;t2;t3;t4;t5;t6;t7]; Savec = [Savec;S1a;S2a;S3a;S4a;S5a;S6a;S7a];
Sbvec = [Sbvec;S1b;S2b;S3b;S4b;S5b;S6b;S7b]; Scvec = [Scvec;S1c;S2c;S3c;S4c;S5c;S6c;S7c];
end
else
for cycle = 1:cycles  
[z0,I0,T0,h0,c0,~,t1,S1a,S1b,S1c] = Power_Control (Po,1,ti,ti+tgi,zi,I0,T0,h0,c0,"Time");
[z0,I0,T0,h0,c0,~,t2,S2a,S2b,S2c] = Power_Control (0,0,ti+tgi,ti+tgi+stay,z0,I0,T0,h0,c0,"Time");
[z0,I0,T0,h0,c0,~,t3,S3a,S3b,S3c] = Power_Control (Po,1,ti+tgi+stay,ti+tgi+stay+tc-tgi,z0,I0,T0,h0,c0,"Time");
[z0,I0,T0,h0,c0,tf2,t4,S4a,S4b,S4c] = Power_Control (-C1,0,ti+tgi+stay+tc-tgi,zc,z0,I0,T0,h0,c0,"SOC");
[z0,I0,T0,h0,c0,~,t5,S5a,S5b,S5c] = Power_Control (Po,1,tf2,2*tgi-tc+tf2,z0,I0,T0,h0,c0,"Time");
[z0,I0,T0,h0,c0,~,t6,S6a,S6b,S6c] = Power_Control (0,0,2*tgi-tc+tf2,2*tgi-tc+tf2+home,z0,I0,T0,h0,c0,"Time");
[~,~,~,~,~,~,t7,S7a,S7b,S7c] = Power_Control (-1,0,2*tgi-tc+tf2+home,zi,z0,I0,T0,h0,c0,"SOC");
ti = t7(end,1);  
tvec = [tvec;t1;t2;t3;t4;t5;t6;t7]; Savec = [Savec;S1a;S2a;S3a;S4a;S5a;S6a;S7a];
Sbvec = [Sbvec;S1b;S2b;S3b;S4b;S5b;S6b;S7b]; Scvec = [Scvec;S1c;S2c;S3c;S4c;S5c;S6c;S7c];  
end
end
end