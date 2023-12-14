"""
Peak_Tracking

Author: Meddelin Setiawan
Date Modified: 13DEC2023

Description:
This script produces a matrix where each peak are tracked across different experiments. The matrix is saved in "tracked_peak_matrix.txt"
"""

import numpy as np
from tabulate import tabulate

from src.Read_User_Input import read_user_input


def calc_diff(experiment_to_track: int, position_index: int, current_position, matrix):
    """
    Calculates difference between position in previous and current experiment.

     Args:
         experiment_to_track: experiment that is being updated in the Tracked Peak Matrix.
         position_index: index of peak position being tracked.
         current_position: peak position being tracked.

     Returns:
         difference value
    """
    previous = 1
    previous_position = matrix[experiment_to_track - previous, position_index]
    while np.isnan(previous_position):
        previous += 1
        previous_position = matrix[experiment_to_track - previous, position_index]
    return previous_position - current_position


def extend_matrix_length(old, new_position):
    """
    Inserts a column (axis = 1) of 'NaN' in a 2D matrix

    Args:
        old: old matrix
        new_position: index in matrix where 'NaN' will be inserted.

    returns
        new matrix
    """
    new = np.insert(old, new_position, "NaN", axis=1)
    return new


def track_peaks(threshold_distance: float):
    """
    Tracks peaks from experiments indicated in user_input.txt

    Args:
        threshold_distance: the maximum displacement (in 10^2 Angstroms) for peaks from 2 different experiments to be considered the same peak.

    returns
        "tracked_peak_matrix.txt", which is the file name containing tracking results.
    """
    # LOAD USER INPUT:
    experiment_type, temperature_point = read_user_input()
    max_distance = (
        threshold_distance  # maximum peak distance to tolerate peak movements.
    )
    total_experiments = len(experiment_type)

    # Initialize tracked peak matrix.
    first_experiment = np.load("../data/pdf_" + experiment_type[0] + "_peaks.npz")
    tracked_matrix = np.empty(
        (total_experiments, len(first_experiment[temperature_point[0]]))
    )  # make an empty matrix
    tracked_matrix[0, :] = first_experiment[
        temperature_point[0]
    ]  # the peak positions in first experiment are just being copied.

    for i in range(1, total_experiments):
        file = np.load("../data/pdf_" + experiment_type[i] + "_peaks.npz")
        p_ori = 0  # starting position index in original experiment.
        p_tracked = (
            0  # starting position index in previous experiments in Tracked Peak Matrix.
        )

        while p_tracked < len(tracked_matrix[i - 1, :]) and p_ori < len(
            file[temperature_point[i]][:]
        ):
            diff = calc_diff(
                i, p_tracked, file[temperature_point[i]][p_ori], tracked_matrix
            )
            if abs(diff) <= max_distance:
                if p_tracked != len(tracked_matrix[i - 1, :]) - 1:
                    diff2 = calc_diff(
                        i,
                        p_tracked + 1,
                        file[temperature_point[i]][p_ori],
                        tracked_matrix,
                    )
                else:
                    # for the case when p_tracked is at the last point of data set.
                    diff2 = diff

                if diff2 < diff:
                    # Scenario 1: CURRENT EXPERIMENT DO NOT CONTAIN AN EXISTING PEAK FROM PREVIOUS experimentS
                    tracked_matrix[i, p_tracked] = "NaN"
                    p_tracked += 1
                else:
                    # Scenario 2: PEAKS BEING COMPARED ARE THE SAME PEAK
                    tracked_matrix[i, p_tracked] = file[temperature_point[i]][p_ori]
                    p_ori += 1
                    p_tracked += 1
            elif diff < -max_distance:
                # Scenario 1
                tracked_matrix[i, p_tracked] = "NaN"
                p_tracked += 1
            elif diff > max_distance:
                # Scenario 3: NEW PEAK EXIST IN CURRENT EXPERIMENT
                tracked_matrix = extend_matrix_length(tracked_matrix, p_tracked)
                tracked_matrix[i, p_tracked] = file[temperature_point[i]][p_ori]
                p_ori += 1
                p_tracked += 1

        # Codes below are to make adjustments to the tail of the matrix
        if tracked_matrix[i, p_tracked - 1] != file[temperature_point[i]][p_ori - 1]:
            # Reassuring final data point from original data set is included
            tracked_matrix = extend_matrix_length(tracked_matrix, p_tracked)
            tracked_matrix[i, -1] = file[temperature_point[i]][-1]
        else:
            while p_tracked < len(tracked_matrix[i - 1, :]):
                # Reassuring there are no empty (zeros) data points in the tracked data set.
                tracked_matrix[i, p_tracked] = "NaN"
                p_tracked += 1

    # SAVING OUTPUT:
    non_nan_indices = ~np.isnan(tracked_matrix)  # Identify non-NaN elements
    tracked_matrix[non_nan_indices] = (
        tracked_matrix[non_nan_indices] / 100
    )  # changing the positions from index to distance in Angstroms
    tracked_matrix_list = tracked_matrix.tolist()
    for i in range(len(tracked_matrix_list)):
        tracked_matrix_list[i].insert(
            0, experiment_type[i] + " " + temperature_point[i]
        )

    headers = [f"Peak {i + 1}" for i in range(tracked_matrix.shape[1])]
    headers = np.insert(headers, 0, "PDF")
    tracked_table = tabulate(tracked_matrix_list, headers, tablefmt="grid")

    # output_file_path = os.path.join('../data/', 'tracked_peak_matrix.txt')
    with open("../data/tracked_peak_matrix.txt", "w") as file:
        file.write(tracked_table)

    print(
        "Peak tracking is successful! The matrix containing tracked peaks has been saved as tracked_peak_matrix.txt in 'data' folder!"
    )

    return "tracked_peak_matrix.txt"
