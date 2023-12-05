"""
Create a peak position tracking matrix for given PDF datasets.
'NaN' indicates the absence of peak. 
Returns text file containing the matrix called "tracked_peak_matrix.txt"
"""
import numpy as np


def calc_diff(dataset_to_track: int, position_index: int, current_position):
    """
   Calculates difference between position in previous and current dataset.
    
    Args:
        dataset_to_track: dataset that is being updated in the Tracked Peak Matrix.
        position_index: index of peak position being tracked.
        current_position: peak position being tracked.

    Returns: 
        difference value
    """
    previous = 1
    previous_position = tracked_matrix[dataset_to_track - previous, position_index]
    while np.isnan(previous_position):
        previous += 1
        previous_position = tracked_matrix[dataset_to_track - previous, position_index]
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


# USER INPUT:
threshold_distance = 20  # maximum peak distance to tolerate peak movements.
total_datasets = 7

# LOAD FILE:
file = np.load("peak_positions_npz/pdf_dwell_peaks.npz")
keys = list(file.keys())

tracked_matrix = np.empty((total_datasets, len(file[keys[0]]))) #make an empty matrix


i = 0
tracked_matrix[i, :] = file[keys[i]] #INITIAL: the first dataset is just being copied. 

for i in range(1, total_datasets):
    p_ori = 0  # starting position index in original dataset. 
    p_tracked = 0  # starting position index in previous datasets in Tracked Peak Matrix.

    while p_tracked < len(tracked_matrix[i - 1, :]) and p_ori < len(file[keys[i]][:]):
        diff = calc_diff(
            i, p_tracked, file[keys[i]][p_ori]
        )
        if abs(diff) <= threshold_distance:
            if p_tracked != len(tracked_matrix[i - 1, :]) - 1:
                diff2 = calc_diff(i, p_tracked + 1, file[keys[i]][p_ori])
            else:
                #for the case when p_tracked is at the last point of data set. 
                diff2 = diff

            if diff2 < diff:
                #Scenario 1: CURRENT DATASET DO NOT CONTAIN AN EXISTING PEAK FROM PREVIOUS DATASETS
                tracked_matrix[
                    i, p_tracked
                ] = "NaN"  
                p_tracked += 1
            else:
                #Scenario 2: PEAKS BEING COMPARED ARE THE SAME PEAK
                tracked_matrix[i, p_tracked] = file[keys[i]][
                    p_ori
                ]  
                p_ori += 1
                p_tracked += 1
        elif diff < -threshold_distance:
            #Scenario 1
            tracked_matrix[
                i, p_tracked
            ] = "NaN"  
            p_tracked += 1
        elif diff > threshold_distance:
            #Scenario 3: NEW PEAK EXIST IN CURRENT DATASET
            tracked_matrix = extend_matrix_length(tracked_matrix, p_tracked)
            tracked_matrix[i, p_tracked] = file[keys[i]][
                p_ori
            ] 
            p_ori += 1
            p_tracked += 1

    #Codes below are to make adjustments to the tail of the matrix
    if (
        tracked_matrix[i, p_tracked - 1] != file[keys[i]][p_ori - 1]
    ):  
        # Reassuring final data point from original data set is included
        tracked_matrix = extend_matrix_length(tracked_matrix, p_tracked)
        tracked_matrix[i, -1] = file[keys[i]][-1]
    else:
        while p_tracked < len(
            tracked_matrix[i - 1, :]
        ):  
            # Reassuring there are no empty (zeros) data points in the tracked data set. 
            tracked_matrix[i, p_tracked] = "NaN"
            p_tracked += 1
#WRITE OUTPUT
print(tracked_matrix)
np.savetxt('tracked_peaks_matrix.txt',tracked_matrix, delimiter='|') #problem here: scientific notation is used when saved as text. 
