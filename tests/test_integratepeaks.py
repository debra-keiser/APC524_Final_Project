from src.Integrate_Peaks import (
    scale_peak_integrals,
    peak_integral_differences,
)

import numpy as np

from src.Extract_Data import extract_pdf_data


def test_integrate_peak_areas():
    """Check that the correct lower- and upper-bound peak minimums are identified."""
    _, pdf_dwell_data_g_r = extract_pdf_data("../data/gr_files", f"Synthetic_CSH_100degC_normalized.gr",)
    
    i_lower = 1
    min_lower_bound = pdf_dwell_data_g_r[163]
    while min_lower_bound > pdf_dwell_data_g_r[163 - i_lower]:
        min_lower_bound = pdf_dwell_data_g_r[163 - i_lower]
        i_lower += 1

    i_upper = 1
    min_upper_bound = pdf_dwell_data_g_r[163]
    while min_upper_bound > pdf_dwell_data_g_r[163 + i_upper]:
        min_upper_bound = pdf_dwell_data_g_r[163 + i_upper]
        i_upper += 1

    assert pdf_dwell_data_g_r[163 - (i_lower - 1)] == -0.269175
    assert pdf_dwell_data_g_r[163 + (i_upper - 1)] == -0.332356


def test_scale_peak_integrals():
    """Check that the peak integrals are multiplied by the proper scale factor."""
    mock_scaled_peak_integrals_dict = scale_peak_integrals({100:np.array([5]), 200:np.array([7])})

    assert mock_scaled_peak_integrals_dict[200] == 5


def test_peak_integral_differences():
    """Check that the expected reference and relative dictionaries are returned."""
    mock_reference_peak_integrals_dict, mock_peak_integrals_differences_dict = peak_integral_differences({100:np.array([5, 6, 7]), 200:np.array([7, 8, 9]), 600:np.array([9, 10, 11])}, {100:np.array([150, 300, 550]), 200:np.array([160, 305, 325]), 600:np.array([170, 310, 400])})

    assert mock_reference_peak_integrals_dict == {150:5, 300:6}
    assert len(mock_peak_integrals_differences_dict) == 2
