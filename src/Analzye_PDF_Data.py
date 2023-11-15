from Determine_Analytes import analyte_data
from Extract_Data import get_PDF_data
from Plot_Peaks import find_and_plot_peaks
from Read_Log_File import extract_time_temp_data

# Analyze time- and temperature-dependent pair distribution function (PDF) data.
# Details about the experiment are read from a log.txt file.
# Pair distribution function data are stored as .gr files.

(
    recorded_times_from_experiment,
    recorded_temperatures_from_experiment,
    rounded_temperatures,
) = extract_time_temp_data("../log.txt")

analyte_times, analyte_temperatures = analyte_data(
    recorded_times_from_experiment,
    recorded_temperatures_from_experiment,
    rounded_temperatures,
)

pdf_ramp_data_r, pdf_ramp_data_g_r = get_PDF_data(rounded_temperatures)

peak_indicies = find_and_plot_peaks(pdf_ramp_data_r, pdf_ramp_data_g_r)
