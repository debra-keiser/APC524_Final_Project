"""
Read_Log_File

Author: Debra Keiser
Date Modified: 09DEC2023

Description:
This script reads the log.txt file and extracts relevant details of experiment progress.
"""


import os
import re
from datetime import datetime


def extract_time_temp_data(file_directory, file_to_read):
    """
    Read a file line-by-line and extract time and temperature identifiers from each line.
    Args:
        file_to_read: File to be parsed/read.
    Returns:
        List of times, list of temperatures, list of rounded temperatures at which PDF data was recorded.
    """
    with open(os.path.join(file_directory, file_to_read)) as open_file:
        individual_lines = open_file.readlines()

    recorded_times_from_experiment = []
    recorded_temperatures_from_experiment = []
    for line in individual_lines:
        if re.search(r"Synthetic_CSH_pdf.", line) is not None:
            recorded_times_from_experiment.append(extract_time(line))
            recorded_temperatures_from_experiment.append(
                float(extract_temperature(line))
            )

    # Convert time and temperature data to convenient formats for subsequent use.
    recorded_times_from_experiment = list(
        map(time_HMS_to_seconds, recorded_times_from_experiment)
    )
    rounded_temperatures = list(
        map(round_to_tens_place, recorded_temperatures_from_experiment)
    )

    return (
        recorded_times_from_experiment,
        recorded_temperatures_from_experiment,
        rounded_temperatures,
    )


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

    # Search for where the temperature is located in the line.
    temperature_readout_index = current_split_line.index("T") + 2

    return current_split_line[temperature_readout_index]


def time_HMS_to_seconds(time_HMS_format):
    """
    Convert time written in standard H:M:S format to seconds.
    Args:
        time_HMS_format: Time formatted as "H:M:S".
    Returns:
        Time in seconds that is equivalent to corresponding H:M:S format.
    """
    datetime_object = datetime.strptime(time_HMS_format, "%H:%M:%S")

    return (
        datetime_object.second
        + (datetime_object.minute * 60)
        + (datetime_object.hour * 3600)
    )


def round_to_tens_place(unrounded_value):
    """
    Round a given value to the nearest 10s place (e.g., 1234 -> 1230).
    Args:
        unrounded_value: Value to be rounded.
    Returns:
        Unrounded value now rounded as shown above.
    """

    return round(unrounded_value, -1)
