%%
dataDir = "/Users/nickwest/Documents/Oxford/MMSC/Hilary/Battery Modeling/BatteryModelling/cleanData/";
outputData = zeros([258 6]); % 258 total runs, R0 R1 C1 SOC T MeanSquaredError at each
filenames = ["hello";"goodbye"];
temperatures = [-20 -10 0 10 25];

count = 1;
for i = 1:length(temperatures)
    tempDataDir = dataDir+getTempFolder(temperatures(i));
    % Get a list of all files in the folder with the desired file name pattern.
    filePattern = fullfile(tempDataDir, '*.csv'); % Change to whatever pattern you need.
    theFiles = dir(filePattern);
    for k = 1 : length(theFiles)
        baseFilename = theFiles(k).name;
        filenames(count) = baseFilename;
%         fullFileName = fullfile(theFiles(k).folder, baseFileName);
        %fprintf(1, 'Now reading %s with temperature %d\n', baseFilename, getTempFromFilename(baseFilename))
        inputData = readtable(tempDataDir+baseFilename);
        outputData(count, :) = [getTempFromFilename(baseFilename) calculateParameters(inputData)];
        count = count + 1;
    end
end
header = {'T', 'R0', 'R1', 'C1', 'SOC', 'MeanSquaredError', 'Run'};
finalOutput = table(outputData(:,1), ...
                    outputData(:,2), ...
                    outputData(:,3), ...
                    outputData(:,4), ...
                    outputData(:,5), ...
                    outputData(:,6), ...
                    filenames, ...
                    'VariableNames', header);
finalOutput
writetable(finalOutput);
