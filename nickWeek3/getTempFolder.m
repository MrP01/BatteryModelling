function [tempFolderName] = getTempFolder(temperature)
%GETTEMPFOLDER Summary of this function goes here
%   Detailed explanation goes here
if temperature == -20
    tempFolderName = "n20c/cleanDataN20C/";
elseif temperature == -10
    tempFolderName = "n10c/cleanDataN10C/";
elseif temperature == 0
    tempFolderName = "0c/cleanData0C/";
elseif temperature == 10
    tempFolderName = "10c/cleanData10C/";
else
    tempFolderName = "25c/cleanData25C/";
end
end

