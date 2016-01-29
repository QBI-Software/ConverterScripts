This is a Python v3.4 script but should be fine in Python 2.7
There are libraries that you will need in Python to run this (numpy and scipy) which can be a pain to install (https://www.scipy.org/install.html).  If you use Anaconda (or Miniconda), this will have everything you need (http://store.continuum.io/cshop/anaconda/).
1. Run the Spyder app, 
2. then open the script (utrackconverter.py), 
3. then select the green play/run button - in the popup window: under "command line options" enter " -i sampledata\channel_1.mat -o sampledata\out.csv"
(You can use the up arrow key in the Console window to re-run)


To run script on commandline:
1. Open terminal
2. Change to working directory containing the code
3. Run with python (version 3.4) as:
python utrackconverter.py -i <input> -o <output>
EXAMPLE:
>python utrackconverter.py -i sampledata/channel_1.mat -o sampledata/channel_1_output.csv
(where -i is the full path to the input file and -o is the full path to the output file)
