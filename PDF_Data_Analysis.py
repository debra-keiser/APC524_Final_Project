import re
from datetime import datetime
from ordered_set import OrderedSet


def read_log_file(log_txt_file):
    data_from_log_txt_file = open(log_txt_file, mode = 'r')
    individual_lines = data_from_log_txt_file.readlines() # extract each line from log.txt file
    return individual_lines


def extract_time(current_line): # TEST THIS BY VALIDATING VIA DATETIME (vlaidate(datetime.strptime(substring, "%H:%M:%S")))
    time_in_line = re.search(r'\b\d\d:\d\d:\d\d\b', current_line)
    return time_in_line.group(0)


def extract_temperature(current_line):
    temperature_readout_index = current_line.index("T") + 2
    temperature_in_line = current_line[temperature_readout_index]
    return temperature_in_line


def round_to_tens_place(unrounded_value):
    return round(unrounded_value, -1)


def divide_by_100(dividend):
    divisor = 100
    return dividend/divisor


def find_repetitive_data(value_to_match, master_list_of_data):
    instances_of_repetition = [x for x, q in enumerate(master_list_of_data) if q == value_to_match]
    return instances_of_repetition


def pull_indexed_data(indices, master_list_of_data):
    data_of_interest = []
    for index in indices:
        data_of_interest.append(master_list_of_data[index])
    return data_of_interest


def time_in_seconds(list_of_times_HMS_format):
    list_of_times_seconds = []
    for current_time in list_of_times_HMS_format:
        datetime_object = datetime.strptime(current_time, '%H:%M:%S')
        current_time_in_seconds = datetime_object.second + (datetime_object.minute * 60) + (datetime_object.hour * 3600)
        list_of_times_seconds.append(current_time_in_seconds)
    return list_of_times_seconds


def list_item_differences(list):
    item_differences = []
    for item in list:
        item_differences.append(item - list[0])
    return item_differences


def is_not_two_minutes(time_in_seconds):
    if time_in_seconds == 120:
        return False
    return True


experimental_data = read_log_file("log.txt")

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
        repeated_data_times_seconds = time_in_seconds(repeated_data_times_HMS)
        measurement_times_at_temp_multiple_of_100.append(repeated_data_times_seconds)
        search_index = repeated_data_indices.pop() + 1
    else:
        search_index += 1

measurements_to_skip = []
for dwell_temperature in measurement_times_at_temp_multiple_of_100:
    time_differences_at_dwell_temperature = list_item_differences(dwell_temperature)
    index_of_measurement_to_skip = time_differences_at_dwell_temperature.index(120)
    measurements_to_skip.append(dwell_temperature[index_of_measurement_to_skip])

measurements_to_analyze_recorded_times = []
measurements_to_analyze_recorded_temperatures = []
for check_time_HMS in recorded_times_from_experiment:
    check_time_seconds = time_in_seconds([check_time_HMS])
    if check_time_seconds[0] not in measurements_to_skip:
        measurements_to_analyze_recorded_times.append(check_time_seconds[0])
        include_in_analysis_index = recorded_times_from_experiment.index(check_time_HMS)
        measurements_to_analyze_recorded_temperatures.append(recorded_temperatures_from_experiment[include_in_analysis_index])

initial_PDF_data = read_log_file("Synthetic_CSH_0{:n}degC_normalized.gr".format(rounded_temperatures[0]))

two_minute_interval_count = 0
next_dwell_temperature = 100
for temperature in OrderedSet(rounded_temperatures):
    if divide_by_100(temperature).is_integer() == False and two_minute_interval_count < 10:
        PDF_ramp_data = read_log_file("Synthetic_CSH_CSH_pdf_ramp_{:n}_0{:n}_normalized.gr".format(next_dwell_temperature, two_minute_interval_count))
        two_minute_interval_count += 1
    elif divide_by_100(temperature).is_integer() == True and two_minute_interval_count < 10:
        PDF_ramp_data = read_log_file("Synthetic_CSH_CSH_pdf_ramp_{:n}_0{:n}_normalized.gr".format(next_dwell_temperature, two_minute_interval_count))
        PDF_dwell_data = read_log_file("Synthetic_CSH_{:n}degC_normalized.gr".format(next_dwell_temperature))
        two_minute_interval_count = 0
        next_dwell_temperature += 100
    elif divide_by_100(temperature).is_integer() == True and two_minute_interval_count >= 10:
        PDF_ramp_data = read_log_file("Synthetic_CSH_CSH_pdf_ramp_{:n}_{:n}_normalized.gr".format(next_dwell_temperature, two_minute_interval_count))
        PDF_dwell_data = read_log_file("Synthetic_CSH_{:n}degC_normalized.gr".format(next_dwell_temperature))
        two_minute_interval_count = 0
        next_dwell_temperature += 100



# READ AND ANALYZE EACH DATASET
