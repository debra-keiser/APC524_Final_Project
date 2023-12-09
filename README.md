# APC524 Group Project
Pair Distribution Function Analysis of Time- and Temperature-Dependent Datasets

Authors: Sophia Bergen, Debra Keiser, and Meddelin Setiawan

This Python-based project automates the process of analyzing pair distribution function (PDF) data collected as the temperature varies over time.

The authors would like to acknowledge Professor Claire E. White and Dr. Karina M.L. Alventosa for the experimental data used in this analysis. More information about the experiment itself may be found [here](https://dataspace.princeton.edu/handle/88435/dsp01mg74qq26k).


# Usage
To create the environment required to execute the scripts, run:
```
conda env create --name PDF_Time-Temp_Analysis -f environment.yml
```

If the user is only interested in analyzing a small subset of peaks, they may indicate as such by adding PDF identifiers from the following lists into the user_input.txt file (do not move/remove "finish" from the end of the file).

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

For example: ramp,1000_00
