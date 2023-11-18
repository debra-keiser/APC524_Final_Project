'''
My objective is to generate a new 2D matrix (called "tracked") with shape (a,b) where:
    a: total measurements/gr files
    b: max number of peaks from all measurements 
The matrix consists of the peak positions, and the "same" peaks (across rows) populate the same index (column) in the matrix.
The value 'NaN' indicates undetected peak in the measurement. 

This version of code has only considered the first two (dwell) files.
I am still in progress of making the algorithm. 

Great start Medi! It looks like this commit failed the pre-commit when it was pushed. To make sure 
it passes all the formatting requirements, try to run pre-commit against your file before pushing to main. 
'''
import numpy as np

file = np.load("../peak_positions_npz/pdf_dwell_peaks.npz")
keys = list(file.keys())
print(keys)

i = 0

#make a new position array which has the shape (total measurements,highest number of peaks)
tracked = np.empty((2,len(file[keys[0]])))
tracked[0,:] = file[keys[0]]
print(tracked)

p1 = 0 #p is index in position array
p2 = 0

def find_next_peak_index(arr, indx):
"""Find the next index of a peak in the array"""
    while indx < len(arr) - 1:
        if arr[idnx] <= arr[indx+1]
            return indx
        idnx += 1
    return indx

# Compare peaks between two keys and update tracked array
while p1 < len(file[keys[0]])-1 or p2 < len(file[keys[1]])-1:
    diff = abs(file[keys[i]][p1]-file[keys[i+1]][p2])
    diff2 = abs(file[keys[i]][p1+1]-file[keys[i+1]][p2])
    while diff>diff2:
        p1 = find_next_peak_index(file[keys[i]], p1)
    tracked[i+1,p1] = file[keys[i+1]][p2]
    p1 += 1
    p2 += 1
tracked[i+1,p1] = file[keys[i+1]][p2]
print(tracked)
