import numpy as np


def analyte_data(
    recorded_times_from_experiment,
    recorded_temperatures_from_experiment,
    rounded_temperatures,
):
    """
    Separate times and temperatures that correspond to repetitive/extraneous .gr files, saving only relevant data.
    Args:
        recorded_times_from_experiment: List of times at which PDF data was recorded.
        recorded_temperatures_from_experiment: List of temperatures at which PDF data was recorded.
        rounded_temperatures: List of temperatures, each rounded to the nearest 10s place.
    Returns:
        List of analyte times, list of analyte temperatures.
    """
    search_index = 0
    measurement_times_at_temp_multiple_of_100 = []
    # Search for data recorded during five-minute dwell intervals.
    while search_index < len(rounded_temperatures):
        if divide_by_100(rounded_temperatures[search_index]).is_integer() is True:
            search_index, occurrence_times = times_of_target_occurrence(
                rounded_temperatures[search_index],
                rounded_temperatures,
                recorded_times_from_experiment,
            )
            measurement_times_at_temp_multiple_of_100.append(occurrence_times)
        else:
            search_index += 1

    # Skip/Discard extraneous data collected before the five-minute dwell interval concludes.
    measurements_to_skip = []
    for dwell_temperature in measurement_times_at_temp_multiple_of_100:
        time_differences_at_dwell_temperature = list_item_differences(dwell_temperature)
        measurements_to_skip.append(
            dwell_temperature[time_differences_at_dwell_temperature.index(120)]
        )

    analyte_times = []
    analyte_temperatures = []
    for check_time in recorded_times_from_experiment:
        if check_time not in measurements_to_skip:
            analyte_times.append(check_time)
            analyte_temperatures.append(
                recorded_temperatures_from_experiment[
                    recorded_times_from_experiment.index(check_time)
                ]
            )

    return analyte_times, analyte_temperatures


def divide_by_100(dividend):
    """
    Divide a given value by 100.
    Args:
        dividend: Value to divide by 100.
    Returns:
        Dividend reduced by a factor of 100.
    """

    return dividend / 100


def times_of_target_occurrence(value_to_match, list_of_values, list_of_times):
    """
    Search a list of data to identify items that are identical to a target item.
    Find the recorded time at which this value was encountered during the experiment.
    Args:
        value_to_match: Target item to which all list items will be compared.
        list_of_values: List of data to search for a match to the target.
        list_of_times: List of timestamps that is complementary to and the same length as list_of_values.
    Returns:
        Index that advances search_index, list of times at which the items in the searched list are the same as the target.
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
        List of differences.
        The first item of the list will always be zero.
    """
    differences_list = np.array(original_list) - original_list[0]

    return differences_list.tolist()
