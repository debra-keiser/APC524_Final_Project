"""
Integrate_Peaks

Author: Debra Keiser
Date Modified: 13DEC2023

Description:
This script integrates, standardizes, and calculates differences between PDF peaks from dwell temperature data to observe how atomic coorindation number changes with increasing temperature.
"""


import itertools

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas.plotting import table

from src.Extract_Data import extract_pdf_data


def peak_integration(npz_file_and_directory, save_path):
    """
    Integrate peaks from a given dwell temperature greater than or equal to 100 degrees Celcius data using the trapezoidal rule.
    Post-process by scaling and differentiating peak integrals to determine changes in atomic coordination numbers.
    Args:
        dwell_peaks_dict = Dictionary of peak positions, within which keys are dwell temperatures and values are NumPy arrays of peak positions.
    Returns:
        None.
    """
    # Extract keys and values from the .npz file and store in a new dictionary.
    dwell_peaks_dict = {}
    with np.load(npz_file_and_directory) as open_npz_file:
        for item in open_npz_file:
            dwell_peaks_dict[item] = open_npz_file[item]

    integrated_dwell_temperatures = []
    dwell_peak_integrals_dict = {}
    # Retrieve PDF data from each .gr file containing data from the dwell temperature segments.
    for dwell_temperature in dwell_peaks_dict:
        if int(dwell_temperature) >= 100:
            integrated_dwell_temperatures.append(dwell_temperature)
            _, pdf_dwell_data_g_r = extract_pdf_data(
                "../data/gr_files",
                f"Synthetic_CSH_{int(dwell_temperature):n}degC_normalized.gr",
            )

            trapezoidal_integrals = [
                integrate_peak_areas(pdf_dwell_data_g_r, peak)
                for peak in dwell_peaks_dict[dwell_temperature]
            ]
            dwell_peak_integrals_dict[dwell_temperature] = trapezoidal_integrals

    # Standardize peak integrals.
    dwell_peak_integrals_dict = scale_peak_integrals(dwell_peak_integrals_dict)

    # Compute differences between integrals of the same peak at variable dwell temperatures.
    (
        number_of_integrated_peaks,
        dwell_peak_integral_differences_dict,
    ) = peak_integral_differences(dwell_peaks_dict, dwell_peak_integrals_dict)

    # Create a table to store display peak integral changes.
    create_table(
        number_of_integrated_peaks,
        dwell_peak_integrals_dict,
        dwell_peak_integral_differences_dict,
        save_path,
    )


def integrate_peak_areas(g_r_data, peak_position_index):
    """
    Determine the points which define a given peak and integrate it using the trapezoid method.
    Peak minimums are determined by iteratively comparing magnitudes of intensity, starting from the maximum.
    Args:
        g_r_data = NumPy array of PDF G_r (y-axis) values.
        peak_position_index = Index of the position of the peak to be integrated.
    Returns:
        Definite integral of the specified peak.
    """
    # Find the minimum of the peak at a smaller r value than the maximum.
    i_lower = 1
    min_lower_bound = g_r_data[peak_position_index]
    while min_lower_bound > g_r_data[peak_position_index - i_lower]:
        min_lower_bound = g_r_data[peak_position_index - i_lower]
        i_lower += 1

    # Find the minimum of the peak at a greater r value than the maximum.
    i_upper = 1
    min_upper_bound = g_r_data[peak_position_index]
    while min_upper_bound > g_r_data[peak_position_index + i_upper]:
        min_upper_bound = g_r_data[peak_position_index + i_upper]
        i_upper += 1

    trapezoid_g_r_data = g_r_data[
        peak_position_index - (i_lower - 1) : peak_position_index + (i_upper - 1)
    ]

    # Take the absolute value to integrate only positive intensities.
    return np.trapz(abs(trapezoid_g_r_data))


def scale_peak_integrals(peak_integrals_dict):
    """
    Scale peaks integrals relative to corresponding reference integrals to standardize data across dwell temperatures.
    Scale factor is calculated with respect to the reference Si-O peak (~1.63 Angstroms).
    Args:
        peak_integrals_dict = Dictionary of peak integrals, within which keys are dwell temperatures and values are NumPy arrays of definite integrals.
    Returns:
        Dictionary of standardized peak integrals for each dwell temperature.
        Keys are dwell temperatures greater than the reference dwell temperature and values are NumPy arrays of scaled definite integrals.
    """
    # Set the first dwell temperature as the reference.
    reference_dwell_temperature = next(iter(peak_integrals_dict.keys()))
    reference_Si_O_integral = (peak_integrals_dict[reference_dwell_temperature])[0]

    # Scale every set of peak integrals for dwell temperatures greater than the reference by multiplying by a scale factor.
    for dwell_temperature in peak_integrals_dict:
        if dwell_temperature != reference_dwell_temperature:
            Si_O_scale_factor = (
                reference_Si_O_integral / (peak_integrals_dict[dwell_temperature])[0]
            )
            peak_integrals_dict[dwell_temperature] = np.multiply(
                peak_integrals_dict[dwell_temperature], Si_O_scale_factor
            )

    return peak_integrals_dict


def peak_integral_differences(peaks_dict, peak_integrals_dict):
    """
    Determine peak integral differences relative to reference peak integrals.
    Args:
        peaks_dict = Dictionary of peak positions, within which keys are dwell temperatures and values are NumPy arrays of positions.
        peak_integrals_dict = Dictionary of peak integrals, within which keys are dwell temperatures and values are NumPy arrays of scaled definite integrals.
    Returns:
        Dictionary of reference peak integrals, dictionary of peak integral differences with respect to the reference.
        Keys are positions and values are definite integrals in the reference dictionary.
        Keys are dwell temperatures greater than the reference and values are NumPy arrays of computed differences in the differences dictionary.
    """
    # Set the first dwell temperature as the reference.
    reference_dwell_temperature = next(iter(peak_integrals_dict.keys()))
    reference_peak_integrals_dict = {}

    # Select peaks that appear under 5 Angstroms.
    for peak_position in peaks_dict[reference_dwell_temperature]:
        if peak_position < 500:
            reference_peak_integrals_dict[peak_position] = (
                peak_integrals_dict[reference_dwell_temperature]
            )[np.where(peaks_dict[reference_dwell_temperature] == peak_position)[0][0]]

    # Store the selected reference peak positions as a list.
    reference_peak_positions = list(reference_peak_integrals_dict.keys())

    # At each subsequent dwell temperature, find the (shifted) peak corresponding to a given reference peak and substract the respective integrals.
    # Store the absolute values of the differences per dwell temperature in a dictionary.
    peak_integral_differences_dict = {}
    for dwell_temperature in peak_integrals_dict:
        if dwell_temperature > reference_dwell_temperature:
            integral_differences_list = subtract_integrals(
                dwell_temperature,
                reference_peak_positions,
                reference_peak_integrals_dict,
                peaks_dict,
                peak_integrals_dict,
            )

            peak_integral_differences_dict[
                dwell_temperature
            ] = integral_differences_list

    return len(reference_peak_positions), peak_integral_differences_dict


def subtract_integrals(
    dwell_temperature,
    reference_peak_positions,
    reference_peak_integrals_dict,
    peaks_dict,
    peak_integrals_dict,
):
    """
    At each dwell temperature after the reference, find the (shifted) peak corresponding to a given reference peak and substract the respective integrals.
    A subfunction/extension of peak_integral_differences function.
    Args:
        dwell_temperature = current dwell temperature greater than the reference dwell temperature.
        reference_peak_positions = List of peak positions at the reference dwell temperature.
        reference_peak_integrals_dict = Dictionary of reference integrals within which keys are peak positions and values are definite integrals.
        peaks_dict = Dictionary of peak positons, within which keys are dwell temperatures and values are NumPy arrays of positions.
        peak_integrals_dict = Dictionary of peak integrals, within which keys are dwell temperatures and values are NumPy arrays of scaled definite integrals.
    Returns:
        List of absolute values of differences between reference peak integrals and peak integrals of the current/specified dwell temperature.
    """
    integral_differences_list = []
    for ref_position, shifted_position in itertools.product(
        reference_peak_positions, peaks_dict[dwell_temperature]
    ):
        if shifted_position in range(ref_position - 15, ref_position + 16):
            integral_differences_list.append(
                round(
                    abs(
                        (peak_integrals_dict[dwell_temperature])[
                            np.where(peaks_dict[dwell_temperature] == shifted_position)
                        ]
                        - reference_peak_integrals_dict[ref_position]
                    )[0],
                    1,
                )
            )

    return integral_differences_list


def create_table(
    n_integrated_peaks, peak_integrals_dict, peak_integral_differences_dict, save_path
):
    """
    Create a table that contains computed changes in peak integrals with respect to the reference dwell temperature and integrals.
    The reference dwell temperature is listed first and shows no integral change (i.e., 0) for each peak.
    Args:
        n_integrated_peaks = Total number of peaks identified and integrated at the reference dwell temperature.
        peak_integrals_dict = List of peak positions at the reference dwell temperature.
        peak_integral_differences_dict = Dictionary of reference integrals within which keys are peak positions and values are definite integrals.
    Returns:
        Prints a PNG file containing the table to the specified directory.
    """
    dwell_peak_integral_differences_matrix = [[0] * n_integrated_peaks]
    df_row_names = [f"{int(next(iter(peak_integrals_dict.keys()))):n}\u00B0C"]
    df_column_names = []
    for dwell_temperature in peak_integral_differences_dict:
        dwell_peak_integral_differences_matrix.append(
            peak_integral_differences_dict[dwell_temperature]
        )
        df_row_names.append(f"{int(dwell_temperature):n}\u00B0C")

    for peak in range(n_integrated_peaks):
        df_column_names.append(f"Peak {peak + 1:n}")

    df = pd.DataFrame.from_records(dwell_peak_integral_differences_matrix)
    df.index = df_row_names
    df.columns = df_column_names
    ax = plt.subplot(111, frame_on=False)
    ax.axis("off")
    table(ax, df, loc="center")
    plt.savefig(
        save_path,
        bbox_inches="tight",
    )
