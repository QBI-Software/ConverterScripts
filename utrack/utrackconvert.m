% TITLE: Convert u-track analysis output to csv file
% Developed for Meunier Lab (Andreas P)
% by Liz Cooper-Williams, QBI (e.cooperwilliams@uq.edu.au)
% Version: 1.0 (30 Jan 2016)
% ---------------------------------------------------------------
% Copyright (C) 2016  QBI Software, The University of Queensland
%
% This program is free software; you can redistribute it and/or modify
% it under the terms of the GNU General Public License as published by
% the Free Software Foundation; either version 2 of the License, or
% (at your option) any later version.
% This program is distributed in the hope that it will be useful,
% but WITHOUT ANY WARRANTY; without even the implied warranty of
% MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
% GNU General Public License for more details.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Clear any preloaded vars - remove if not wanted
clear
% Open matlab data
[filename,filepath] = uigetfile({'*.mat'},'Select mat file');
inputfile = fullfile(filepath,filename);
outputfile = sprintf('%s_extracted.csv',filename);
output = fullfile(filepath, outputfile);
mydata = load(inputfile)

% Output to csv
colnames = {'tracknum' 'asymmetry' 'moment' 'motion' ...
            'mssSlope' 'normDiffCoeff' 'genDiffCoeff' 'scalingPower'}
tabledata =[];%zeros(length(mydata.diffAnalysisRes),length(colnames));
for j=1:length(mydata.diffAnalysisRes)
    analysisdata = mydata.diffAnalysisRes(j).fullDim;
    classification = mydata.diffAnalysisRes(j).classification;
    tracknum = j

    if (length(analysisdata.mssSlope) > 1)
        for i=1:length(analysisdata.mssSlope)
            asymmetry = classification(i,1);
            moment = classification(i,2);
            motion = classification(i,3);
            mssslope = analysisdata.mssSlope(i);
            normdiffcoeff = analysisdata.normDiffCoef(i);
            gendiffcoeff = analysisdata.genDiffCoef(i,3); %3rd normalized
            scalingpower = analysisdata.scalingPower(i,3);
            row1 = [j asymmetry moment motion mssslope normdiffcoeff gendiffcoeff scalingpower];
            tabledata = cat(1,tabledata,row1);
            %tabledata(i,:) = row1;
        end
    else
        asymmetry = classification(1);
        moment = classification(2);
        motion = classification(3);
        mssslope = analysisdata.mssSlope;
        normdiffcoeff = analysisdata.normDiffCoef;
        gendiffcoeff = analysisdata.genDiffCoef(3); %3rd normalized
        scalingpower = analysisdata.scalingPower(3);
        row1 = [j asymmetry moment motion mssslope normdiffcoeff gendiffcoeff scalingpower];
        tabledata = cat(1,tabledata,row1);
    end
end
T = array2table(tabledata);
T.Properties.VariableNames = colnames(1,:);
T
writetable(T,output);
