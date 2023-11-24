import os
import re

import numpy as np

from src.Extract_Data import rescale_g_r


def test_r_gr_extraction():
    """Check that the NumPy arrays of all r and g_r data are equal and can therefore be plotted."""
    for filename in os.listdir("data/gr_files"):
        if filename.endswith(".gr"):
            with open(os.path.join("data/gr_files", filename)) as open_gr_file:
                individual_lines = open_gr_file.readlines()
            for line in individual_lines:
                if re.search(r"#### start data", line) is not None:
                    start_data = individual_lines.index(line)
            r = np.array([])
            g_r = np.array([])
            for r_g_r_pair in range(start_data + 3, len(individual_lines)):
                split_r_g_r_pair = individual_lines[r_g_r_pair].split()
                r = np.append(r, float(split_r_g_r_pair[0]))
                g_r = np.append(g_r, float(split_r_g_r_pair[1]))

            assert len(r) == 6001
            assert len(g_r) == 6001


def test_rescaling():
    """Check that g_r data is scaled appropriately to the correct peak intensity."""
    with open(
        os.path.join(
            "data/gr_files", "Synthetic_CSH_CSH_pdf_ramp_100_04_normalized.gr"
        ),
    ) as open_gr_file:
        individual_lines = open_gr_file.readlines()

    for line in individual_lines:
        if re.search(r"#### start data", line) is not None:
            start_data = individual_lines.index(line)

    g_r = np.array([])
    for r_g_r_pair in range(start_data + 3, len(individual_lines)):
        split_r_g_r_pair = individual_lines[r_g_r_pair].split()
        g_r = np.append(g_r, float(split_r_g_r_pair[1]))

    rescaled_g_r = rescale_g_r(g_r)

    assert rescaled_g_r[164] == 0.278468
