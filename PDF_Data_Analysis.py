import os
import re
from datetime import datetime

import numpy as np
from ordered_set import OrderedSet

# Analyze time- and temperature-dependent pair distribution function data.
# Details about the experiment are extracted from a log file.
# Pair distribution function data is stored and read from .gr files.


def read_file(file_to_read):
    """
    Read a file line-by-line and extract each line's data.
    Args:
        file: File to be parsed/read.
    Returns:
        Each line from the file as items in a list.
    """
    data_from_file = open(file_to_read)
    individual_lines = data_from_file.readlines()
    return individual_lines


def extract_time(
    current_line,
):  # TEST THIS BY VALIDATING VIA DATETIME (validate(datetime.strptime(substring, "%H:%M:%S")))
    """
    Identify the time stamp recorded for a specified measurement.
    Regex syntax: r' ' = raw string, \b = beginning or end of string, \\d = digit (0-9).
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


def find_repetitive_data(value_to_match, master_list_of_data):
    """
    Search a list of data to identify multiple items that are identical to a target item.
    Args:
        value_to_match: Target item to which all list items will be compared.
        master_list_of_data: List of data to search.
    Returns:
        Indexes of the items in the searched list that are the same as the target.
    """
    instances_of_repetition = []
    for index in range(len(master_list_of_data)):
        if master_list_of_data[index] == value_to_match:
            instances_of_repetition.append(index)
    return instances_of_repetition


def pull_indexed_data(indices, master_list_of_data):
    """
    Select multiple items from a master list and store in a new list.
    Args:
        indices: List of indexes that guides which data to store.
        master_list_of_data: List to extract data from based on specified indices.
    Returns:
        List that contains a specific subset of data from the master list.
    """
    data_of_interest = []
    for index in indices:
        data_of_interest.append(master_list_of_data[index])
    return data_of_interest


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


def read_file_different_directory(file_directory, file_to_read):
    """
    Read a file from a different directory line-by-line and extract each line's data.
    Args:
        file_directory: Name of or path to directory under current working directory.
        file: File to be parsed/read.
    Returns:
        Each line from the file as items in a list.
    """
    with open(os.path.join(file_directory, file_to_read)) as open_file:
        data_from_file = open_file.read()
    return data_from_file


experimental_data = read_file("log.txt")

recorded_times_from_experiment = []
recorded_temperatures_from_experiment = []
for line in experimental_data:
    if re.search(r"Synthetic_CSH_pdf.", line) is not None:
        recorded_times_from_experiment.append(extract_time(line))
        recorded_temperatures_from_experiment.append(float(extract_temperature(line)))

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
        repeated_data_indices = find_repetitive_data(
            rounded_temperatures[search_index], rounded_temperatures
        )
        measurement_times_at_temp_multiple_of_100.append(
            pull_indexed_data(repeated_data_indices, recorded_times_from_experiment)
        )
        search_index = repeated_data_indices.pop() + 1
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

# print(measurements_to_analyze_recorded_times) # ADD AS TEST???
# print(measurements_to_analyze_recorded_temperatures)
# print(len(measurements_to_analyze_recorded_times))
# print(len(measurements_to_analyze_recorded_temperatures))

PDF_initial_data = read_file_different_directory(
    "gr_files", f"Synthetic_CSH_0{rounded_temperatures[0]:n}degC_normalized.gr"
)

two_minute_interval_count = 0
next_dwell_temperature = 100
for temperature in OrderedSet(rounded_temperatures):
    if temperature == rounded_temperatures[0]:
        pass
    elif divide_by_100(temperature).is_integer() is False:
        PDF_ramp_data = read_file_different_directory(
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
        PDF_ramp_data = read_file_different_directory(
            "gr_files",
            "Synthetic_CSH_CSH_pdf_ramp_{:n}_0{:n}_normalized.gr".format(
                next_dwell_temperature, two_minute_interval_count
            ),
        )
    else:
        PDF_ramp_data = read_file_different_directory(
            "gr_files",
            "Synthetic_CSH_CSH_pdf_ramp_{:n}_0{:n}_normalized.gr".format(
                next_dwell_temperature, two_minute_interval_count
            ),
        )
        PDF_dwell_data = read_file_different_directory(
            "gr_files",
            f"Synthetic_CSH_{next_dwell_temperature:n}degC_normalized.gr",
        )
        two_minute_interval_count = 0
        next_dwell_temperature += 100


# ANALYZE EACH DATASET
