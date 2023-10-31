import contextlib
import os
import re
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
from ordered_set import OrderedSet
from scipy.signal import find_peaks

# Analyze time- and temperature-dependent pair distribution function (PDF) data.
# Details about the experiment are extracted from a log file.
# Pair distribution function data is stored and read from .gr files.


def extract_time_temp_data(file_to_read):
    """
    Read a file line-by-line and extract data from each line.
    Args:
        file_to_read: File to be parsed/read.
    Returns:
        Lists that contain data of interest.
    """
    data_from_file = open(file_to_read)
    individual_lines = data_from_file.readlines()
    data_from_file.close()
    time_data = []
    temp_data = []
    for line in individual_lines:
        if re.search(r"Synthetic_CSH_pdf.", line) is not None:
            time_data.append(extract_time(line))
            temp_data.append(float(extract_temperature(line)))
    return time_data, temp_data


def extract_time(current_line):
    """
    Identify the time stamp recorded for a specified measurement.
    re.search looks for the substring "##:##:##".
    RegEx syntax: r" " = raw string, \b = beginning or end of string, \\d = digit (0-9).
    Args:
        current_line: Line to search from a previoiusly read file.
    Returns:
        Recorded time in standard H:M:S format.
    """
    time_in_line = re.search(r"\b\d\d:\d\d:\d\d\b", current_line)
    return time_in_line.group(0)


def extract_temperature(current_line):
    """
    Identify the temperature at which a specified measurement taken.
    Args:
        current_line: Split line to search from a previoiusly read file.
    Returns:
        Recorded temperature.
    """
    current_split_line = current_line.split(" ")
    temperature_readout_index = current_split_line.index("T") + 2
    temperature_in_line = current_split_line[temperature_readout_index]
    return temperature_in_line


def time_HMS_to_seconds(time_HMS_format):
    """
    Convert time written in standard H:M:S format to seconds.
    Args:
        time_HMS_format: Time formatted as "H:M:S".
    Returns:
        Time in seconds, equating to corresponding H:M:S format.
    """
    datetime_object = datetime.strptime(time_HMS_format, "%H:%M:%S")
    time_seconds = (
        datetime_object.second
        + (datetime_object.minute * 60)
        + (datetime_object.hour * 3600)
    )
    return time_seconds


def round_to_tens_place(unrounded_value):
    """
    Round a given value to the nearest 10s place (e.g., 1234 -> 1230).
    Args:
        unrounded_value: Value to be rounded.
    Returns:
        Unrounded value, now rounded as shown above.
    """
    return round(unrounded_value, -1)


def divide_by_100(dividend):
    """
    Divide a given value by 100.
    Args:
        dividend: Value to divide by 100.
    Returns:
        Dividend, now reduced by a factor of 100.
    """
    return dividend / 100


def times_of_target_occurence(value_to_match, list_of_values, list_of_times):
    """
    Search a list of data to identify items that are identical to a target item.
    Subsequently find the recorded time at which this value was encountered during the experiment.
    Args:
        value_to_match: Target item to which all list items will be compared.
        list_of_values: List of data to search for a match to the target.
        list_of_times: List of timestamps that is complementary to and the same length as list_of_values.
    Returns:
        Times at which the items in the searched list are the same as the target.
    """
    instances_of_target_value = []
    for index in range(len(list_of_values)):
        if list_of_values[index] == value_to_match:
            instances_of_target_value.append(index)
    corresponding_times = []
    for index in instances_of_target_value:
        corresponding_times.append(list_of_times[index])
    return instances_of_target_value.pop() + 1, corresponding_times


def list_item_differences(original_list):
    """
    Calculate the differences between every item in a list and the first item.
    Args:
        original_list: List of values to compute differences within.
    Return:
        List of differences, where the first item will always be zero.
    """
    differences_list = np.array(original_list) - original_list[0]
    return differences_list.tolist()


def extract_PDF_data(file_directory, gr_file_to_read):
    """
    Read a .gr file and extract r and Gr data from each line.
    Scale the data if the temperature is less than 100 degrees Celcius.
    Args:
        file_directory: Name of or path to directory containing the .gr file.
        file: .gr file to be parsed/read.
    Returns:
        r and G(r) data as NumPy arrays.
    """
    data_from_gr_file = open(os.path.join(file_directory, gr_file_to_read))
    individual_lines = data_from_gr_file.readlines()
    for line in individual_lines:
        if re.search(r"#### start data", line) is not None:
            start_data = individual_lines.index(line)
    r = []
    Gr = []
    for r_Gr_pair in range(start_data + 3, len(individual_lines)):
        split_r_Gr_pair = individual_lines[r_Gr_pair].split()
        r.append(float(split_r_Gr_pair[0]))
        Gr.append(float(split_r_Gr_pair[1]))
    data_from_gr_file.close()
    r = np.array(r, dtype="float64")
    Gr = np.array(Gr, dtype="float64")
    with contextlib.suppress(IndexError):
        if (
            int(
                next(
                    iter(filter(lambda x: x.isdigit(), re.split("_", gr_file_to_read)))
                )
            )
            == 100
        ):
            Gr = rescale_Gr(Gr)
    return r, Gr


def rescale_Gr(extracted_Gr_data):
    """
    Account for the presence of water in samples measured at temperatures under 100 degrees Celcius.
    Multiply G(r) data by a computed constant to rescale it with respect to a local maximum peak intensity.
    Args:
        extracted_Gr_data = NumPy array containing raw G(r) values.
    Returns:
        NumPy array of adjusted G(r) values.
    """
    H2O_scale_factor = 0.278468 / max(extracted_Gr_data[160:170])
    rescaled_Gr_data = extracted_Gr_data * H2O_scale_factor
    return rescaled_Gr_data


def find_and_plot_peaks(
    r, Gr
):  # also pass file name, from which to pull information to title plot (example below)
    """
    Locate the peaks (maxima) in G(r) data, and plot selected peaks along with the PDF.
    Args:
        r = extracted r data.
        Gr = extracted G(r) data, either raw or rescaled.
    Returns:
        NumPy array of indices at which selected maxima in G(r) are present.
        Saves a plot of PDF data with markers at certain peak positions as a PNG file.
    """
    peaks, _ = find_peaks(Gr, height=0)
    peaks = np.delete(peaks, np.where((peaks < 81) | (peaks > 3001)))
    plt.figure(figsize=(80, 40))
    plt.plot(r, Gr, color="b", linestyle="-", linewidth=5)
    plt.plot(r[peaks], Gr[peaks], linestyle=" ", marker="P", markersize=40)
    plt.title("PDF Data", fontsize=80, fontweight="bold", loc="center")
    plt.xlabel("r (\u00C5)", fontsize=70, loc="center")
    plt.xlim([0, 60])
    plt.xticks(np.arange(0, 61, 10), fontsize=55)
    plt.ylabel("G(r)", fontsize=70, loc="center")
    plt.yticks([], fontsize=55)
    plt.savefig("PDF_Data")
    # matplotlib.pyplot.suptitle('Silhouette Analysis of %d Clusters For %d-Component PCA' % (K,n_PCA_components), fontsize = 75,)
    plt.close()
    return peaks


(
    recorded_times_from_experiment,
    recorded_temperatures_from_experiment,
) = extract_time_temp_data("log.txt")

recorded_times_from_experiment = list(
    map(time_HMS_to_seconds, recorded_times_from_experiment)
)
rounded_temperatures = list(
    map(round_to_tens_place, recorded_temperatures_from_experiment)
)

search_index = 0
measurement_times_at_temp_multiple_of_100 = []
while search_index < len(rounded_temperatures):
    if divide_by_100(rounded_temperatures[search_index]).is_integer() is True:
        search_index, occurrence_times = times_of_target_occurence(
            rounded_temperatures[search_index],
            rounded_temperatures,
            recorded_times_from_experiment,
        )
        measurement_times_at_temp_multiple_of_100.append(occurrence_times)
    else:
        search_index += 1

measurements_to_skip = []
for dwell_temperature in measurement_times_at_temp_multiple_of_100:
    time_differences_at_dwell_temperature = list_item_differences(dwell_temperature)
    measurements_to_skip.append(
        dwell_temperature[time_differences_at_dwell_temperature.index(120)]
    )

measurements_to_analyze_recorded_times = []
measurements_to_analyze_recorded_temperatures = []
for check_time in recorded_times_from_experiment:
    if check_time not in measurements_to_skip:
        measurements_to_analyze_recorded_times.append(check_time)
        measurements_to_analyze_recorded_temperatures.append(
            recorded_temperatures_from_experiment[
                recorded_times_from_experiment.index(check_time)
            ]
        )

PDF_initial_data_r, PDF_initial_data_Gr = extract_PDF_data(
    "gr_files", f"Synthetic_CSH_0{rounded_temperatures[0]:n}degC_normalized.gr"
)
PDF_initial_data_Gr = rescale_Gr(PDF_initial_data_Gr)

two_minute_interval_count = 0
next_dwell_temperature = 100
for temperature in OrderedSet(rounded_temperatures):
    if temperature == rounded_temperatures[0]:
        pass
    elif divide_by_100(temperature).is_integer() is False:
        PDF_ramp_data_r, PDF_ramp_data_Gr = extract_PDF_data(
            "gr_files",
            "Synthetic_CSH_CSH_pdf_ramp_{:n}_0{:n}_normalized.gr".format(
                next_dwell_temperature, two_minute_interval_count
            ),
        )
        two_minute_interval_count += 1
    elif (
        divide_by_100(temperature).is_integer() is True
        and next_dwell_temperature == rounded_temperatures[-1]
    ):
        PDF_ramp_data_r, PDF_ramp_data_Gr = extract_PDF_data(
            "gr_files",
            "Synthetic_CSH_CSH_pdf_ramp_{:n}_0{:n}_normalized.gr".format(
                next_dwell_temperature, two_minute_interval_count
            ),
        )
    else:
        PDF_ramp_data_r, PDF_ramp_data_Gr = extract_PDF_data(
            "gr_files",
            "Synthetic_CSH_CSH_pdf_ramp_{:n}_0{:n}_normalized.gr".format(
                next_dwell_temperature, two_minute_interval_count
            ),
        )
        PDF_dwell_data_r, PDF_dwell_data_Gr = extract_PDF_data(
            "gr_files", f"Synthetic_CSH_{next_dwell_temperature:n}degC_normalized.gr"
        )
        two_minute_interval_count = 0
        next_dwell_temperature += 100

peak_indices = find_and_plot_peaks(PDF_ramp_data_r, PDF_ramp_data_Gr)
