"""
Working Algorithm. Will make helpful explanations later + how to actually use it
"""
import numpy as np


def calc_diff(dataset_to_track: int, position_index: int, current_position):
    """
    dataset_to_track: dataset number (peak positions from single PDF) that is being updated in the Tracked Peak Matrix.
    position_index: index of peak position being tracked.
    current_position: peak position being tracked.

    This function calculates previous_position - current_position.
    """
    previous = 1
    previous_position = tracked_matrix[dataset_to_track - previous, position_index]
    while np.isnan(previous_position):
        previous += 1
        previous_position = tracked_matrix[dataset_to_track - previous, position_index]
    return previous_position - current_position


def extend_matrix_length(old, new_p):
    new = np.insert(old, new_p, "NaN", axis=1)
    return new


# USER INPUT:
threshold_distance = 20  # maximum peak distance to tolerate peak movements.
file = np.load("peak_positions_npz/pdf_dwell_peaks.npz")
keys = list(file.keys())
print(keys)
total_datasets = 7

# make a new position array which has the shape (total measurements,highest number of peaks)
tracked_matrix = np.empty((total_datasets, len(file[keys[0]])))

i = 0  # dataset 0 (30 degrees)
tracked_matrix[i, :] = file[keys[i]]
print(tracked_matrix)

for i in range(1, total_datasets):
    print(i, keys[i])
    p_old = 0  # starting position index from old dataset
    p_tracked = 0  # starting position index from new dataset

    while p_tracked < len(tracked_matrix[i - 1, :]) and p_old < len(file[keys[i]][:]):
        diff = calc_diff(
            i, p_tracked, file[keys[i]][p_old]
        )  # calculate difference between peak position from previous and current dataset
        if abs(diff) <= threshold_distance:
            if p_tracked != len(tracked_matrix[i - 1, :]) - 1:
                diff2 = calc_diff(i, p_tracked + 1, file[keys[i]][p_old])
            else:
                diff2 = diff

            if diff2 < diff:
                tracked_matrix[
                    i, p_tracked
                ] = "NaN"  # CURRENT DATASET DO NOT CONTAIN AN EXISTING PEAK FROM PREVIOUS DATASETS
                p_tracked += 1
            else:
                tracked_matrix[i, p_tracked] = file[keys[i]][
                    p_old
                ]  # PEAK BEING COMPARED ARE THE SAME PEAK
                p_old += 1
                p_tracked += 1
        elif diff < -threshold_distance:
            tracked_matrix[
                i, p_tracked
            ] = "NaN"  # CURRENT DATASET DO NOT CONTAIN AN EXISTING PEAK FROM PREVIOUS DATASETS
            p_tracked += 1
        elif diff > threshold_distance:
            tracked_matrix = extend_matrix_length(tracked_matrix, p_tracked)
            tracked_matrix[i, p_tracked] = file[keys[i]][
                p_old
            ]  # NEW PEAK EXIST IN CURRENT DATASET
            p_old += 1
            p_tracked += 1
    print(tracked_matrix)

    # Below make adjustments to the tail of the matrix
    if (
        tracked_matrix[i, p_tracked - 1] != file[keys[i]][p_old - 1]
    ):  # Reassuring final data point is included
        print("hello")
        tracked_matrix = extend_matrix_length(tracked_matrix, p_tracked)
        tracked_matrix[i, -1] = file[keys[i]][-1]
    else:
        while p_tracked < len(
            tracked_matrix[i - 1, :]
        ):  # Reassuring all "zeros" at the tail converted to Nan
            print("hey")
            tracked_matrix[i, p_tracked] = "NaN"
            p_tracked += 1
    print(tracked_matrix)
