function [outputParams] = calculateParameters(runData)

    %% Load specific current and voltage profile.
    measuredVoltage = runData.voltage;
    % OCV = mean(measuredVoltage([1:3 length(measuredVoltage)-3:length(measuredVoltage)]));
    OCV = mean(measuredVoltage(1:5));
    current = runData.current;
    stateOfCharge = runData.SOC;

    %% Calculate R0, R1, C1 through fitting process
    typicalR0 = 8.2e-3;
    typicalR1 = 15.8e-3;
    typicalC1 = 38e3;
    initialParameters = [typicalR0 typicalR1 typicalC1];
    samplingRate = 10; % 10s sampling
    capacity = 2.9; % 2.9Ah cell
    eta = ones(length(current), 1);
    iR10 = 0;

    errorOfPrediction = @(params) getSSE(measuredVoltage, ...
        getVoltageCurveConstOCV(samplingRate, ...
        capacity, ...
        current, ...
        eta, ...
        params, ...
        iR10, ...
        OCV));

    %%
    X = fminsearch(errorOfPrediction, initialParameters);
    % A = [-1 0 0; 0 -1 0; 0 0 -1;
    %      1 0 0 ; 0 1 0 ; 0 0 1];
    % b = [0; 0; 0; 10; 10; 100000];
    % X = fmincon(errorOfPrediction, initialParameters, A, b); % Positive values!
    R0 = X(1); R1 = X(2); C1 = X(3);

    predictedVoltage = getVoltageCurveConstOCV(samplingRate, ...
        capacity, ...
        current, ...
        eta, ...
        [R0 R1 C1], ...
        iR10, ...
        OCV);
    score = getSSE(measuredVoltage, predictedVoltage) / length(predictedVoltage); %mean squared error times a trillion
    SOC = mean(stateOfCharge);

    outputParams = [R0, R1, C1, SOC, score];
end
