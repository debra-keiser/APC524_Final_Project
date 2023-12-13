"""
Analyze_PDF_Data

Author: Debra Keiser
Date Modified: 13DEC2023

Description:
This script executes all other scripts/functions required for the PDF analysis.
"""


import os

import numpy as np
from Determine_Analytes import get_analyte_data
from Extract_Data import get_gr_files
from Integrate_Peaks import peak_integration
from Plot_Total_Peaks import plot_total_peaks
from Read_Log_File import extract_time_temp_data

# Analyze time- and temperature-dependent pair distribution function (PDF) data.
# Details about the experiment are read from a log.txt file.
# Pair distribution function data are stored as .gr files.

(
    recorded_times_from_experiment,
    recorded_temperatures_from_experiment,
    rounded_temperatures,
) = extract_time_temp_data("../data", "log.txt")

analyte_times, analyte_temperatures = get_analyte_data(
    recorded_times_from_experiment,
    recorded_temperatures_from_experiment,
    rounded_temperatures,
)

pdf_ramp_peaks_dict, pdf_dwell_peaks_dict = get_gr_files(rounded_temperatures)

np.savez(os.path.join("../data", "pdf_ramp_peaks.npz"), **pdf_ramp_peaks_dict)
np.savez(os.path.join("../data", "pdf_dwell_peaks.npz"), **pdf_dwell_peaks_dict)

plot_total_peaks("../data", "pdf_ramp_peaks.npz")
peak_integration("../data", "pdf_dwell_peaks.npz")
