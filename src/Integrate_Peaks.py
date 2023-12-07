import os

import numpy as np

from src.Extract_Data import extract_pdf_data


def peak_integration(dwell_peaks_dict):
    """
    Integrate peaks from a given dwell temperature greater than or equal to 100 degrees Celcius data using the trapezoidal rule.
    Post-process by scaling and differentiating peak integrals to determine changes in atomic coordination numbers.
    Args:
        dwell_peaks_dict = Dictionary of peak positions, within which keys are dwell temperatures and values are NumPy arrays of peak center/maximum indices.
    Returns:
        Dictionary of scaled peak integral differences written to a .npz file.
        Keys are dwell temperatures and values are NumPy arrays of peak integral differences.
    """
    dwell_peak_integrals_dict = {}

    # Retrieve PDF data from each .gr file containing data from the dwell temperature segments.
    for dwell_temperature in dwell_peaks_dict:
        if int(dwell_temperature) >= 100:
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
        reference_dwell_peak_integrals_dict,
        dwell_peak_integral_differences_dict,
    ) = peak_integral_differences(dwell_peak_integrals_dict, dwell_peaks_dict)

    np.savez(
        os.path.join("../data", "pdf_dwell_peak_integral_differences.npz"),
        **dwell_peak_integral_differences_dict,
    )


def integrate_peak_areas(g_r_data, peak_position_index):
    """
    Determine the points which define a given peak and integrate it using the trapezoid method.
    Peak minimums are determined by iteratively comparing magnitudes of intensity, starting from the maximum.
    Args:
        g_r_data = NumPy array of PDF G_r (y-axis) values.
        peak_position_index = Index of the center position (maximum) of the peak to be integrated.
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
        peak_integrals_dict = Dictionary of peak integrals, within which keys are dwell temperatures and values are NumPy arrays of peak integrals.
    Returns:
        Dictionary of standardized peak integrals for each dwell temperature.
        Keys are dwell temperatures greater than the reference dwell temperature and values are NumPy arrays of scaled peak integrals.
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


def peak_integral_differences(peak_integrals_dict, peaks_dict):
    """
    Determine peak integral differences relative to reference peak integrals.
    Args:
        peak_integrals_dict = Dictionary of peak integrals, within which keys are dwell temperatures and values are NumPy arrays of scaled peak integrals.
        peaks_dict = Dictionary of peak positons, within which keys are dwell temperatures and values are NumPy arrays of peak center/maximum indices.
    Returns:
        Dictionary of reference peak integrals, dictionary of peak integral differences with respect to the reference.
        Keys are peak position indices and values are peak integrals in the reference dictionary.
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
            integral_differences_list = []
            for ref_position in reference_peak_positions:
                for shifted_position in peaks_dict[dwell_temperature]:
                    if shifted_position in range(ref_position - 15, ref_position + 16):
                        integral_differences_list.append(
                            abs(
                                (peak_integrals_dict[dwell_temperature])[
                                    np.where(
                                        peaks_dict[dwell_temperature]
                                        == shifted_position
                                    )
                                ]
                                - reference_peak_integrals_dict[ref_position]
                            )[0]
                        )

            peak_integral_differences_dict[dwell_temperature] = np.array(
                integral_differences_list
            )

    return reference_peak_integrals_dict, peak_integral_differences_dict
