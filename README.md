# Automated PDF Analysis
## Automated Pair Distribution Function Analysis for Assessing Reaction Progress

Authors: Sophia Bergen, Debra Keiser, and Meddelin Setiawan

This Python-based project computerizes the process of analyzing pair distribution function (PDF) data collected as the temperature varies over time.

The authors would like to acknowledge Professor Claire E. White and Dr. Karina M.L. Alventosa for the experimental data used in this analysis. More information about the experiment itself may be found [here](https://dataspace.princeton.edu/handle/88435/dsp01mg74qq26k).

# USAGE
## Environment
To clone this GitHub repository to your local machine, run:
```
git clone https://github.com/debra-keiser/Automated_PDF_Analysis.git
```
Create the environment required to execute the scripts from the home directory of this repository with:
```
conda env create --name Auto_PDF_Analysis -f environment.yml
conda activate Auto_PDF_Analysis
```
Before execution, remove src. from function imports in Extract_Data.py, Peak_Tracking.py, and Integrate_Peaks.py (included for testing purposes only).
## Execution
Create_Report.py executes all other scripts to analyze PDF data. In the src/ directory, run:
```
python Create_Report.py
```
Input log.txt and .gr files are stored in data/ and data/gr_files, respectively. A description detailing the purpose of each script/function is provided in its respective file.

src/Plot_Total_Peaks.py, src/Plot_PDFs.py, src/Peak_Tracking.py, and src/Integrate_Peaks.py may also be run as standalone scripts after Create_Report.py has been executed once.

## User Input
src/Peak_Tracking.py requires that the user indicates which PDF file(s) they are interested in analyzing by listing the corresponding key(s) in data/user_input.txt (do not move/remove "finish" from the end of the file).

Example syntax:
ramp,1000_00

Keys for "dwell" peaks:
[30, 100, 200, 300, 400, 500, 600, 700, 800, 900]

Keys for "ramp" peaks:
[100_00, 100_01, 100_02, 100_03, 100_04, 100_05, 100_06,
200_00, 200_01, 200_02, 200_03, 200_04, 200_05, 200_06, 200_07, 200_08, 200_09,
300_00, 300_01, 300_02, 300_03, 300_04, 300_05, 300_06, 300_07, 300_08, 300_09,
400_00, 400_01, 400_02, 400_03, 400_04, 400_05, 400_06, 400_07, 400_08, 400_09,
500_00, 500_01, 500_02, 500_03, 500_04, 500_05, 500_06, 500_07, 500_08, 500_09,
600_00, 600_01, 600_02, 600_03, 600_04, 600_05, 600_06, 600_07, 600_08, 600_09,
700_00, 700_01, 700_02, 700_03, 700_04, 700_05, 700_06, 700_07, 700_08, 700_09,
800_00, 800_01, 800_02, 800_03, 800_04, 800_05, 800_06, 800_07, 800_08, 800_09,
900_00, 900_01, 900_02, 900_03, 900_04, 900_05, 900_06, 900_07, 900_08, 900_09,
1000_00, 1000_01, 1000_02, 1000_03, 1000_04, 1000_05, 1000_06, 1000_07, 1000_08, 1000_09]

## Output
All results are stored in data/ and data/images. The main output is a portable document file (final_output_report.pdf) that contains plots and tables generated during the analysis. These plots and tables, in addition to .npz files of peak positions, are also saved and stored individually.
