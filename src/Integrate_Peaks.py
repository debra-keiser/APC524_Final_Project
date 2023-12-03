import os

import numpy as np

from src.Extract_Data import extract_pdf_data, rescale_g_r


def peak_integration(dwell_peaks_dict):
    """
    Integrate peaks from a given dwell temperature data using the trapezoidal rule.
    Args:
        dwell_peaks_dict = dictionary which contains a NumPy array of peak positions (value) for a given dwell temperature (key).
    Returns:
        A dictionary containing a NumPy array of peak integrals (value) for a given dwell temperature (key), written to a .npz file.
    """
    # Define the center of the peak, the spacing between points of the trapezoids, and a dictionary to store peak integrals.
    dwell_peak_integrals_dict = {}

    # Retrieve PDF data from each .gr file containing data from the dwell temperature segments.
    for dwell_temperature in dwell_peaks_dict:
        if int(dwell_temperature) < 100:
            _, pdf_dwell_data_g_r = extract_pdf_data(
                "../data/gr_files",
                f"Synthetic_CSH_0{int(dwell_temperature):n}degC_normalized.gr",
            )
            pdf_dwell_data_g_r = rescale_g_r(pdf_dwell_data_g_r)
        else:
            _, pdf_dwell_data_g_r = extract_pdf_data(
                "../data/gr_files",
                f"Synthetic_CSH_{int(dwell_temperature):n}degC_normalized.gr",
            )

        trapezoidal_integrals = [
            define_trapezoids(pdf_dwell_data_g_r, peak)
            for peak in dwell_peaks_dict[dwell_temperature]
        ]
        dwell_peak_integrals_dict[dwell_temperature] = trapezoidal_integrals

    np.savez(
        os.path.join("../data", "pdf_dwell_peak_integrals.npz"),
        **dwell_peak_integrals_dict,
    )


def define_trapezoids(g_r_data, peak_position_index):
    """
    Determine the points which define and integrate using the trapezoid for a given peak.
    Spacing between points on the x-axis is specified by dr, in Angstroms.
    Args:
        g_r_data = NumPy array of PDF G_r (y-axis) values.
        peak_position_index = index of the center position (maximum) of the peak to be integrated.
    Returns:
        Definite integral of the specified peak.
    """
    dr = 9  # +/- 0.9 Angstroms
    trapezoid_g_r_data = g_r_data[
        peak_position_index - dr : peak_position_index + dr + 1
    ]

    return np.trapz(abs(trapezoid_g_r_data))
