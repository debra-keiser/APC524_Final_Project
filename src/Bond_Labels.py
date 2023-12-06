"""
Identifies and extracts peak labels from the provided PDF data.

The function finds peaks in the PDF data using the locate_peaks function, matches these peaks
with known bond length ranges, and extracts labels for peaks within the first five Angstroms.

Args:
- r1 (numpy.ndarray): Array containing r values (Angstroms) from the PDF data.
 - g_r1 (numpy.ndarray): Array containing G(r) values corresponding to r values.

Returns:
- labels (dict): Dictionary containing labels for peaks within the first five Angstroms,
                with keys as (bond, bond_length) and values as corresponding G(r) values.
"""

import matplotlib.pyplot as plt
import numpy as np
from Extract_Data import locate_peaks

def extract_peak_labels(r1, g_r1):
    """
    This function finds peaks in the PDF data using the locate_peaks function, and matches these peaks
    with known bond length ranges.

    Args:
    - r1 (numpy.ndarray): Array containing r values (Angstroms) from the PDF data.
    - g_r1 (numpy.ndarray): Array containing G(r) values corresponding to r values.

    Returns:
    - labels (dict): Dictionary containing labels for peaks within the first five Angstroms,
                     with keys as (bond, bond_length) and values as corresponding G(r) values.
    """
    
    peaks = locate_peaks(g_r1)  # You can adjust the 'height' parameter as needed

    # Known peak length ranges
    known_peak_ranges = {
        'Si-O': (1.5, 1.7),
        'Ca-O': (2.3, 2.5),
        'O-O': (2.6, 2.7),
        'Si-Si': (3, 3.2)
    }
    # Match identified peaks with known bond length ranges
    matched_peaks = {}
    for bond, (lower, upper) in known_peak_ranges.items():
        matched_indices = [i for i, val in enumerate(r1[peaks]) if lower <= val <= upper]
        matched_peaks[bond] = matched_indices

    labels = {}
    for bond, indices in matched_peaks.items():
        for idx in indices:
            if r1[peaks][idx] <= 5:  # Consider peaks within the first five Angstroms
                bond_length = r1[peaks][idx]  # Retrieve the bond length
                labels[(bond, bond_length)] = g_r1[peaks][idx]  # Save bond and length in the dictionary

    return labels
