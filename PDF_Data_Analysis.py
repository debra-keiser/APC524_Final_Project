import re
from datetime import datetime
from ordered_set import OrderedSet

# Analyze time- and temperature-dependent pair distribution function data.
# Details about the experiment are extracted from a log file.
# Pair distribution function data is stored and read from .gr files.

def read_file(file):
    """
    Read a file a file line-by-line and extract each line's data.
    Args:
        file: File to be parsed/read.
    Returns:
        Each line from the file as items in a list.
    """
    data_from_file = open(file, mode = 'r')
    individual_lines = data_from_file.readlines()
    return individual_lines


def extract_time(current_line): # TEST THIS BY VALIDATING VIA DATETIME (vlaidate(datetime.strptime(substring, "%H:%M:%S")))
    """
    Identify the time stamp recorded for a specified measurement.
    Args:
        current_line: Line to search from a previoiusly read file.
    Returns:
        Recorded time in standard H:M:S format.
    """
    time_in_line = re.search(r'\b\d\d:\d\d:\d\d\b', current_line)
    return time_in_line.group(0)


def extract_temperature(current_split_line):
    """
    Identify the temperature at which a specified measurement taken.
    Args:
        current_line: Split line to search from a previoiusly read file.
    Returns:
        Recorded temperature.
    """
    temperature_readout_index = current_split_line.index("T") + 2
    temperature_in_line = current_split_line[temperature_readout_index]
    return temperature_in_line


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
    divisor = 100
    return dividend/divisor


def find_repetitive_data(value_to_match, master_list_of_data):
    """
    Search a list of data to identify which items are identical to a target item.
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
    Store select data from a master list in a new list.
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


def time_HMS_to_seconds(list_of_times_HMS_format):
    """
    Convert time written in standard H:M:S format to seconds.
    Args:
        list_of_times_HMS_format: List of strings formatted as "H:M:S".
    Returns:
        List of intgers in seconds, equating to corresponding H:M:S formats.
    """
    list_of_times_seconds = []
    for current_time in list_of_times_HMS_format:
        datetime_object = datetime.strptime(current_time, '%H:%M:%S')
        current_time_in_seconds = datetime_object.second + (datetime_object.minute * 60) + (datetime_object.hour * 3600)
        list_of_times_seconds.append(current_time_in_seconds)
    return list_of_times_seconds


def list_item_differences(list):
    """
    Calculate the differences between every item in a list and the first item.
    Args:
        list: List of values to compute differences within.
    Return:
        List of differences, where the first item will always be zero.
    """
    item_differences = []
    for item in list: # CONSIDER USING NUMPY, *ARRAY-AT-A-TIME* INSTEAD OF FOR LOOP
        item_differences.append(item - list[0])
    return item_differences


def is_not_two_minutes(time_in_seconds):
    """
    Check if a given time is not equal to 2 minutes (120 seconds).
    Args:
        Time value, in seconds.
    Return:
        False if the inputted time is 120 seconds, True otherwise.
    """
    if time_in_seconds == 120:
        return False
    return True


experimental_data = read_file("log.txt")

recorded_times_from_experiment = []
recorded_temperatures_from_experiment = []
for line in experimental_data:
    if re.search(r"Synthetic_CSH_pdf.", line) != None:
        recorded_times_from_experiment.append(extract_time(line))
        split_line = line.split(' ')
        recorded_temperatures_from_experiment.append(float(extract_temperature(split_line)))

rounded_temperatures = list(map(round_to_tens_place, recorded_temperatures_from_experiment))
rounded_temperature_quotients = list(map(divide_by_100, rounded_temperatures))

search_index = 0
measurement_times_at_temp_multiple_of_100 = []
while search_index < len(rounded_temperature_quotients):
    floating_point = rounded_temperature_quotients[search_index]
    if floating_point.is_integer() == True:
        repeated_data_indices = find_repetitive_data(floating_point, rounded_temperature_quotients)
        repeated_data_times_HMS = pull_indexed_data(repeated_data_indices, recorded_times_from_experiment)
        repeated_data_times_seconds = time_HMS_to_seconds(repeated_data_times_HMS) # MAP HERE INSTEAD OF USING LIST FORMAT???
        measurement_times_at_temp_multiple_of_100.append(repeated_data_times_seconds)
        search_index = repeated_data_indices.pop() + 1
    else:
        search_index += 1

measurements_to_skip = []
for dwell_temperature in measurement_times_at_temp_multiple_of_100:
    time_differences_at_dwell_temperature = list_item_differences(dwell_temperature)
    index_of_measurement_to_skip = [time_differences_at_dwell_temperature.index(120)]
    measurements_to_skip.append(pull_indexed_data(index_of_measurement_to_skip, dwell_temperature)[0])

measurements_to_analyze_recorded_times = []
measurements_to_analyze_recorded_temperatures = []
for check_time_HMS in recorded_times_from_experiment: # MAP HERE INSTEAD OF FOR LOOP???
    check_time_seconds = time_HMS_to_seconds([check_time_HMS]) # MAP HERE INSTEAD OF FOR LOOP???
    if check_time_seconds[0] not in measurements_to_skip:
        measurements_to_analyze_recorded_times.append(check_time_seconds[0])
        include_in_analysis_index = [recorded_times_from_experiment.index(check_time_HMS)]
        measurements_to_analyze_recorded_temperatures.append(pull_indexed_data(include_in_analysis_index, recorded_temperatures_from_experiment)[0])

print(measurements_to_analyze_recorded_times) # SANITY-CHECKING, REMOVE THESE LATER - ADD AS TEST???
print(measurements_to_analyze_recorded_temperatures)
print(len(measurements_to_analyze_recorded_times))
print(len(measurements_to_analyze_recorded_temperatures))

initial_PDF_data = read_file("Synthetic_CSH_0{:n}degC_normalized.gr".format(rounded_temperatures[0]))

two_minute_interval_count = 0
next_dwell_temperature = 100
for temperature in OrderedSet(rounded_temperatures):
    if divide_by_100(temperature).is_integer() == False and two_minute_interval_count < 10:
        PDF_ramp_data = read_file("Synthetic_CSH_CSH_pdf_ramp_{:n}_0{:n}_normalized.gr".format(next_dwell_temperature, two_minute_interval_count))
        two_minute_interval_count += 1
    elif divide_by_100(temperature).is_integer() == True and two_minute_interval_count < 10:
        PDF_ramp_data = read_file("Synthetic_CSH_CSH_pdf_ramp_{:n}_0{:n}_normalized.gr".format(next_dwell_temperature, two_minute_interval_count))
        PDF_dwell_data = read_file("Synthetic_CSH_{:n}degC_normalized.gr".format(next_dwell_temperature))
        two_minute_interval_count = 0
        next_dwell_temperature += 100
    elif divide_by_100(temperature).is_integer() == True and two_minute_interval_count >= 10:
        PDF_ramp_data = read_file("Synthetic_CSH_CSH_pdf_ramp_{:n}_{:n}_normalized.gr".format(next_dwell_temperature, two_minute_interval_count))
        PDF_dwell_data = read_file("Synthetic_CSH_{:n}degC_normalized.gr".format(next_dwell_temperature))
        two_minute_interval_count = 0
        next_dwell_temperature += 100



# READ AND ANALYZE EACH DATASET
