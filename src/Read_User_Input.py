"""
Read_User_Input

Author: Meddelin Setiawan
Date Modified: 08DEC2023

Description:
This script reads user_input.txt to feed any functions with PDF files intended to be analyzed.
Returns 2 separate arrays, one indicating the type of experiment (either 'dwell' or 'ramp') and the other indicating the key.
"""
import numpy as np
def read_user_input():
    user_input = open("user_input.txt","r")
    experiment_type = np.array([])
    temperature_point = np.array([])

    for line in user_input:
        fields = line.split(",")
        experiment_type = np.append(experiment_type, fields[0])
        temperature_point = np.append(temperature_point, fields[1][:-1])
    
    user_input.close()
    return experiment_type, temperature_point