import re
from datetime import datetime


def extract_time_temp_data(file_to_read):
    """
    Read a file line-by-line and extract data from each line.
    Args:
        file_to_read: File to be parsed/read.
    Returns:
        Lists that contain times and temperatures at which PDF data was recorded.
    """
    data_from_file = open(file_to_read)
    individual_lines = data_from_file.readlines()
    data_from_file.close()
    recorded_times_from_experiment = []
    recorded_temperatures_from_experiment = []
    for line in individual_lines:
        if re.search(r"Synthetic_CSH_pdf.", line) is not None:
            recorded_times_from_experiment.append(extract_time(line))
            recorded_temperatures_from_experiment.append(
                float(extract_temperature(line))
            )
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
    temperature_readout_index = current_split_line.index("T") + 2
    return current_split_line[temperature_readout_index]


def time_HMS_to_seconds(time_HMS_format):
    """
    Convert time written in standard H:M:S format to seconds.
    Args:
        time_HMS_format: Time formatted as "H:M:S".
    Returns:
        Time in seconds, equating to corresponding H:M:S format.
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
        Unrounded value, now rounded as shown above.
    """
    return round(unrounded_value, -1)
