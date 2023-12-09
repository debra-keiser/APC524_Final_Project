"""
Read_User_Input

Author: Meddelin Setiawan
Date Modified: 08DEC2023

Description:
This script reads user_input.txt to feed any functions with PDF files intended to be analyzed.
"""

import numpy as np


def read_user_input():
    experiment_type = np.array([])
    temperature_point = np.array([])

    with open("./src/user_input.txt") as file:
        for line in file.readlines()[:-1]:
            fields = line.strip().split(",")
            experiment_type = np.append(experiment_type, fields[0])
            temperature_point = np.append(temperature_point, fields[1])

    file.close()
    return experiment_type, temperature_point