function [temperature] = getTempFromFilename(filename)
%GETTEMPFROMFILENAME Summary of this function goes here
%   Detailed explanation goes here
newStr = split(filename, "_");
newStr = newStr{2};
newStr = newStr(1:length(newStr)-5);
if newStr(1) == "N" || newStr(1) == "n"
    temperature = -str2num(newStr(2:length(newStr)));
else
    temperature = str2num(newStr);
end
end
