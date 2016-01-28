#!/usr/bin/python3
"""
    QBI MatlabConverter: Read mat files from u-track into csv
    U-track http://lccb.hms.harvard.edu/software.html
    TRACK DATA FORMAT: from chooseTracks.m
    %INPUT  trackedFeatureInfo: -- EITHER --
%                           Output of trackWithGapClosing:
%                           Matrix indicating the positions and amplitudes
%                           of the tracked features to be plotted. Number
%                           of rows = number of tracks, while number of
%                           columns = 8*number of time points. Each row
%                           consists of
%                           [x1 y1 z1 a1 dx1 dy1 dz1 da1 x2 y2 z2 a2 dx2 dy2 dz2 da2 ...]
%                           in image coordinate system (coordinates in
%                           pixels). NaN is used to indicate time points
%                           where the track does not exist.
%                           -- OR --
%                           Output of trackCloseGapsKalman:
%                           Structure array with number of entries equal to
%                           the number of tracks (or compound tracks when
%                           merging/splitting are considered). Contains the
%                           fields:
%           .tracksCoordAmpCG: The positions and amplitudes of the tracked
%                              features, after gap closing. Number of rows
%                              = number of track segments in compound
%                              track. Number of columns = 8 * number of
%                              frames the compound track spans. Each row
%                              consists of
%                              [x1 y1 z1 a1 dx1 dy1 dz1 da1 x2 y2 z2 a2 dx2 dy2 dz2 da2 ...]
%                              NaN indicates frames where track segments do
%                              not exist.
%           .seqOfEvents     : Matrix with number of rows equal to number
%                              of events happening in a track and 4
%                              columns:
%                              1st: Frame where event happens;
%                              2nd: 1 - start of track, 2 - end of track;
%                              3rd: Index of track segment that ends or starts;
%                              4th: NaN - start is a birth and end is a death,
%                                   number - start is due to a split, end
%                                   is due to a merge, number is the index
%                                   of track segment for the merge/split.

    ANALYSIS FORMAT AS BELOW: from trackDiffusionAnalysis1.m
% OUTPUT diffAnalysisRes : Structure array with the following fields per
%                         track:
%           .classification: Number of segment x 3 matrix.
%                           *Column 1: Classification based on asymmetry.
%                            1 = asymmetric, 0 = not asymmetric.
%                           *Column 2: Classification based on moment
%                            scaling spectrum analysis applied to the
%                            tracks using their full dimensionality.
%                            1 = confined Brownian, 2 = pure Brownian,
%                            3 = directed motion.
%                           *Column 3: Classification of motion along
%                            the preferred direction for linear tracks,
%                            also based on moment scaling spectrum analysis.
%                            1 = confined Brownian, 2 = pure Brownian,
%                            3 = directed motion.
%           .fullDim       : MSS analysis results for full dimensionality.
%                            Structure with fields:
%               .mssSlope    : Slope of the line representing moment
%                              scaling power vs. moment order.
%               .genDiffCoef : Generalized diffusion coefficient for each
%                              order employed. The "normal" (MSD) diffusion
%                              coefficient is the 3rd entry.
%               .scalingPower: The moment scaling power for each order
%                              employed. The scaling power of the MSD is
%                              the 3rd entry.
%           .oneDim        : MSS analysis results for reduced dimensionality.
%                            Structure with same fields as fullDim.
%           .confRadius    : For particles undergoing confined motion, the
%                            confinement radius assuming circular
%                            confinement, or the 2 confinement dimensions
%                            assuming rectangular confinement.
%                            For particles undergoing linear motion, the 2
%                            confinement dimensions parallel and
%                            perpendicular to the direction of motion.
%       errFlag         : 0 if executed normally, 1 otherwise.

    *******************************************************************************
    Copyright (C) 2015  QBI Software, The University of Queensland

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
"""
import numpy as np
import scipy.io
import csv
import sys


class MatTrackAnalysis:
    """
    ['mssSlope', 'genDiffCoef', 'scalingPower', 'normDiffCoef']
    """
    def __init__(self):
        # Initialize fields
        self.tracknum = None
        self.mssSlope = None
        self.genDiffCoef = None
        self.scalingPower = None
        self.normDiffCoef = None
        self.asymmetry = 0 #Classification
        self.moment = 0 #Classification
        self.motion = 0 #Classification


class Matconverter:

    def __init__(self, inputfile=None):
        # Initialize fields
        self.totalTracks = None
        self.dataloaded = False
        self.inputfile = inputfile
        self.mtalist = []
        #self.tracklist = []

    """
    Reading MssSlope, genDiffCoeff, Scaling power
    D:\Projects\Meunier_tracking\data\channel_1
    """
    def loaddata(self):
        mydata = scipy.io.loadmat(self.inputfile, struct_as_record=False,squeeze_me=True)
        allanalysisdata = mydata['diffAnalysisRes']
        tracks = 1
        for analysis in allanalysisdata:
            analysisdata = analysis.fullDim
            classification = analysis.classification

            if (not np.isscalar(analysisdata.mssSlope)):
                for i in range(len(analysisdata.mssSlope)):
                    mta = MatTrackAnalysis()
                    mta.tracknum = tracks
                    #classification[i] = self.replaceNaN(classification[i],0)
                    mta.asymmetry = classification[i][0]
                    mta.moment = classification[i][1]
                    mta.motion = classification[i][2]
                    mta.mssSlope = analysisdata.mssSlope[i]
                    mta.genDiffCoef = analysisdata.genDiffCoef[i][2] #3rd val is normalised
                    mta.scalingPower = analysisdata.scalingPower[i][2]
                    mta.normDiffCoef = analysisdata.normDiffCoef[i]
                    self.mtalist.append(mta)
            else:
                mta = MatTrackAnalysis()
                mta.tracknum = tracks
                #classification = self.replaceNaN(classification,0)
                mta.asymmetry = classification[0]
                mta.moment = classification[1]
                mta.motion = classification[2]
                mta.mssSlope = analysisdata.mssSlope
                mta.genDiffCoef = analysisdata.genDiffCoef[2]
                mta.scalingPower = analysisdata.scalingPower[2]
                mta.normDiffCoef = analysisdata.normDiffCoef
                self.mtalist.append(mta)
            self.dataloaded = True
            tracks = tracks + 1

        return tracks

    """Utility to replace NaN with a value
    """
    def replaceNaN(self, ary, val):
        for x in range(len(ary)):
            if np.isnan(ary[x]):
                ary[x] = val
        return ary

    """ Output to csv file
    """
    def save_csv(self,fullfilename):
        try:
            if sys.version_info >= (3, 0, 0):
                fo = open(fullfilename, 'w', newline='')
            else:
                fo = open(fullfilename, 'wb')
        except IOError:
            msg = "ERROR: cannot access output file (maybe open in another program): " + fullfilename
            return msg
        with fo as csvfile:
            fieldnames = ['tracknum', 'asymmetry', 'moment', 'motion',
                          'mssSlope', 'normDiffCoeff', 'genDiffCoeff', 'scalingPower']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for mta in self.mtalist:
                writer.writerow({'tracknum': mta.tracknum,
                                 'asymmetry': mta.asymmetry,
                                 'moment': mta.moment,
                                 'motion': mta.motion,
                                 'mssSlope': mta.mssSlope,
                                 'normDiffCoeff': mta.normDiffCoef,
                                 'genDiffCoeff': mta.genDiffCoef,
                                 'scalingPower': mta.scalingPower})
            msg = "**Conversion Complete"
            return msg




if __name__ == "__main__":
    import argparse
    #defaults
    inputfile = 'D:\\Projects\\Meunier_tracking\\Converterscripts\\sampledata\\channel_1.mat'
    outputfile = 'D:\\Projects\\Meunier_tracking\\Converterscripts\\sampledata\\channel_1_output.csv'
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", dest="input",
                        default=inputfile, help="Full path to input file")
    parser.add_argument("-o", "--output", dest="output",
                        default=outputfile, help="Full path to output file")
    args = parser.parse_args()
    spt = Matconverter(args.input)
    tracks = spt.loaddata()
    if (tracks > 1):
        print("Data rows loaded: ",tracks)
    else:
        print("No data loaded")
    rtn = spt.save_csv(args.output)
    print(rtn, ": ", args.output)