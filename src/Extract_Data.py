import contextlib
import os
import re

import numpy as np
from ordered_set import OrderedSet
from scipy.signal import find_peaks

from src.Determine_Analytes import divide_by_100


def get_pdf_data(rounded_temperatures):
    """
    Extract data from the first .gr file, and continue for each subsequent .gr file of interest.
    Repetitive/Extraneous files are skipped by converting the list in to an ordered set.
    Find the peaks within a specified range, and store the data for further analysis.
    Args:
        rounded_temperatures: List of rounded temperature values.
    Returns:
        Two separate dictionaries for ramp and dwell data.
        Keys are identifying temperatures/intervals and values are NumPy arrays of peak positions.
    """
    pdf_ramp_peaks_dict = {}
    pdf_dwell_peaks_dict = {}
    pdf_initial_data_r, pdf_initial_data_g_r = extract_pdf_data(
        "../gr_files", f"Synthetic_CSH_0{rounded_temperatures[0]:n}degC_normalized.gr"
    )
    pdf_dwell_peaks_dict[f"{rounded_temperatures[0]:n}"] = locate_peaks(
        pdf_initial_data_g_r
    )

    two_minute_interval_count = 0
    next_dwell_temperature = 100
    for temperature in OrderedSet(rounded_temperatures):
        if temperature == rounded_temperatures[0]:
            pass
        elif divide_by_100(temperature).is_integer() is False:
            pdf_ramp_data_r, pdf_ramp_data_g_r = extract_pdf_data(
                "../gr_files",
                "Synthetic_CSH_CSH_pdf_ramp_{:n}_0{:n}_normalized.gr".format(
                    next_dwell_temperature, two_minute_interval_count
                ),
            )
            pdf_ramp_peaks_dict[
                f"{next_dwell_temperature:n}_0{two_minute_interval_count:n}"
            ] = locate_peaks(pdf_ramp_data_g_r)
            two_minute_interval_count += 1
        elif (
            divide_by_100(temperature).is_integer() is True
            and next_dwell_temperature == rounded_temperatures[-1]
        ):
            pdf_ramp_data_r, pdf_ramp_data_g_r = extract_pdf_data(
                "../gr_files",
                "Synthetic_CSH_CSH_pdf_ramp_{:n}_0{:n}_normalized.gr".format(
                    next_dwell_temperature, two_minute_interval_count
                ),
            )
            pdf_ramp_peaks_dict[
                f"{next_dwell_temperature:n}_0{two_minute_interval_count:n}"
            ] = locate_peaks(pdf_ramp_data_g_r)
        else:
            pdf_ramp_data_r, pdf_ramp_data_g_r = extract_pdf_data(
                "../gr_files",
                "Synthetic_CSH_CSH_pdf_ramp_{:n}_0{:n}_normalized.gr".format(
                    next_dwell_temperature, two_minute_interval_count
                ),
            )
            pdf_dwell_data_r, pdf_dwell_data_g_r = extract_pdf_data(
                "../gr_files",
                f"Synthetic_CSH_{next_dwell_temperature:n}degC_normalized.gr",
            )
            pdf_ramp_peaks_dict[
                f"{next_dwell_temperature:n}_0{two_minute_interval_count:n}"
            ] = locate_peaks(pdf_ramp_data_g_r)
            pdf_dwell_peaks_dict[f"{next_dwell_temperature:n}"] = locate_peaks(
                pdf_dwell_data_g_r
            )
            two_minute_interval_count = 0
            next_dwell_temperature += 100

    return pdf_ramp_peaks_dict, pdf_dwell_peaks_dict


def extract_pdf_data(file_directory, gr_file_to_read):
    """
    Read a .gr file and extract r and G(r) data from each line.
    Scale the data if the temperature is less than 100 degrees Celcius.
    Args:
        file_directory: Name of or path to directory containing the .gr file.
        file: .gr file to be parsed/read.
    Returns:
        r and G(r) (raw or scaled) data as NumPy arrays.
    """
    data_from_gr_file = open(os.path.join(file_directory, gr_file_to_read))
    individual_lines = data_from_gr_file.readlines()
    for line in individual_lines:
        if re.search(r"#### start data", line) is not None:
            start_data = individual_lines.index(line)
    r = np.array([])
    g_r = np.array([])
    for r_g_r_pair in range(start_data + 3, len(individual_lines)):
        split_r_g_r_pair = individual_lines[r_g_r_pair].split()
        r = np.append(r, float(split_r_g_r_pair[0]))
        g_r = np.append(g_r, float(split_r_g_r_pair[1]))
    data_from_gr_file.close()
    with contextlib.suppress(StopIteration):
        if (
            int(
                next(
                    iter(filter(lambda x: x.isdigit(), re.split("_", gr_file_to_read)))
                )
            )
            == 100
        ):
            g_r = rescale_g_r(g_r)
    return r, g_r


def rescale_g_r(extracted_g_r_data):
    """
    Account for the presence of water in samples measured at temperatures under 100 degrees Celcius.
    Multiply G(r) data by a computed constant to rescale it with respect to a local maximum peak intensity.
    Args:
        extracted_g_r_data = NumPy array containing raw G(r) values.
    Returns:
        NumPy array of adjusted G(r) values.
    """
    H2O_scale_factor = 0.278468 / max(extracted_g_r_data[160:170])
    return extracted_g_r_data * H2O_scale_factor


def locate_peaks(g_r):
    """
    Locate the peaks (maxima) in G(r) data within a specified range.
    Args:
        g_r = extracted G(r) data, either raw or rescaled.
    Returns:
        NumPy array of indices at which selected maxima in G(r) are present.
    """
    peaks, _ = find_peaks(g_r, height=0)
    peaks = np.delete(peaks, np.where((peaks < 81) | (peaks > 3001)))
    return peaks
