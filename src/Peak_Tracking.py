import numpy as np

def track_peaks(npz_file):
    """
    Generate a 2D matrix (called "tracked") with shape (a, b) such that:
        a: total measurements/gr files
        b: max number of peaks from all measurements 
    The matrix consists of the peak positions, and the "same" peaks (across rows) populate the same index (column) in the matrix.
    The value 'NaN' indicates an undetected peak in the measurement. 

    This version of code has only considered the first two (dwell) files.
    I am still in progress of making the algorithm.
    Args:
        npz_file: .npz file from which data will be loaded/read.
    Returns: 2D matrix containing tracked peaks.
    """

    data_from_npz = np.load(npz_file)
    npz_keys = list(data_from_npz.keys())
    print(npz_keys)

    i = 0
    # Make a new position array which has the shape (total measurements, highest number of peaks).
    tracked = np.empty((2, len(data_from_npz[npz_keys[0]])))
    tracked[0, :] = data_from_npz[npz_keys[0]]
    print(tracked)

    p1 = 0 # p is index in position array
    p2 = 0

    while p1 < len(data_from_npz[npz_keys[0]]) - 1 or p2 < len(data_from_npz[npz_keys[1]]) - 1:
        diff = abs(data_from_npz[npz_keys[i]][p1] - data_from_npz[npz_keys[i + 1]][p2])
        diff2 = abs(data_from_npz[npz_keys[i]][p1 + 1] - data_from_npz[npz_keys[i + 1]][p2])
        while diff > diff2:
            tracked[i + 1, p1] = 'NaN'
            p1 += 1
            diff = diff2
            diff2 = abs(data_from_npz[npz_keys[i]][p1 + 1] - data_from_npz[npz_keys[i + 1]][p2])
        tracked[i+1, p1] = data_from_npz[npz_keys[i + 1]][p2]
        p1 += 1
        p2 += 1
    tracked[i + 1, p1] = data_from_npz[npz_keys[i + 1]][p2]
    print(tracked)
