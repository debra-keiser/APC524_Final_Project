"""
PDF Plotting Functions

Author: Sophia Bergen
Date Modified: 06DEC2023

Description:
This file contains all functions related to plotting the PDF data
"""

import matplotlib.pyplot as plt
from Bond_Labels import extract_peak_labels
from Extract_Data import extract_pdf_data, rescale_g_r


def plot_peaks(r_list, g_r_list, labels, filename):
    """
    Plots the peaks of PDF data as r(A) vs G(r).

    Args:
    - r_list (list): List of arrays containing r values for each temperature.
    - g_r_list (list): List of arrays containing G(r) values for each temperature corresponding to r values.
    - labels (list): List of labels for each dataset in the plot.
    - filename (str): Name of the file to save the generated plot as a PNG.

    Returns:
    - None: The function saves the plot as a PNG file and does not return any value.
    """
    plt.figure(figsize=(12, 8))  # Modify the figure size as needed
    for i in range(len(r_list)):
        plt.plot(r_list[i], g_r_list[i], label=labels[i])

    plt.title("PDF Data at Increasing Temperatures", fontsize=16)
    plt.xlabel("r (\u00C5)", fontsize=14)
    plt.ylabel("G(r)", fontsize=14)
    plt.legend()
    plt.grid(True)
    # Save the plot as a PNG file
    plt.savefig(filename, format="png")
    plt.close()  # Close the plot to release memory


def plot_zoomed_peaks(r_list, g_r_list, legend_labels, filename):
    """
    Plots the peaks of PDF data within the first five Angstroms. Will label bond types by calling Bond_Labels.

    Args:
    - r_list (list): List of arrays containing r values for each temperature.
    - g_r_list (list): List of arrays containing G(r) values for each temperature corresponding to r values.
    - legend_labels (list): List of labels for each dataset in the plot.
    - filename (str): Name of the file to save the generated plot as a PNG.

    Returns:
    - None: The function saves the plot as a PNG file and does not return any value.
    """
    plt.figure(figsize=(12, 8))  # Modify the figure size as needed

    for i in range(len(r_list)):
        plt.plot(r_list[i], g_r_list[i], label=legend_labels[i])

        # Extract labels for peaks within the first five Angstroms for each dataset
        labels = extract_peak_labels(r_list[0], g_r_list[0])
        # Plot bond lengths within the first five Angstroms

    # Plot bond lengths within the first five Angstroms
    for bond_length in labels.keys():
        plt.text(
            bond_length[1],
            labels[bond_length],
            f"{bond_length[0]}",
            ha="center",
            va="bottom",
        )

    plt.title("PDF Data (0 to 5 Angstroms) at Increasing Temperatures", fontsize=16)
    plt.xlabel("r (\u00C5)", fontsize=14)
    plt.ylabel("G(r)", fontsize=14)
    plt.grid(True)
    plt.xlim(0, 5)
    plt.legend()
    plt.savefig(filename, format="png")
    plt.close()  # Close the plot to release memory


def Plot_multiple_PDFs():
    """
    Loads and plots multiple PDF datasets at different temperatures.

    The function loads data for multple PDFs, plots both original and zoomed-in versions of the datasets,
    and saves the plots as PNG files.

    Returns:
    - total_plot_filename (str): Filename or path of the saved PNG file containing the original plot.
    - zoomed_plot_filename (str): Filename or path of the saved PNG file containing the zoomed-in plot.
    """
    r1, g_r1 = extract_pdf_data(
        "./data/gr_files", "Synthetic_CSH_030degC_normalized.gr"
    )
    r2, g_r2 = extract_pdf_data(
        "./data/gr_files", "Synthetic_CSH_CSH_pdf_ramp_300_09_normalized.gr"
    )
    r3, g_r3 = extract_pdf_data(
        "./data/gr_files", "Synthetic_CSH_CSH_pdf_ramp_600_09_normalized.gr"
    )
    r4, g_r4 = extract_pdf_data(
        "./data/gr_files", "Synthetic_CSH_CSH_pdf_ramp_1000_09_normalized.gr"
    )

    g_r1 = rescale_g_r(g_r1)
    # Call plot_peaks with the datasets for the full r-range plot.
    total_plot_filename = "./data/total_peaks_and_PDFs.png"
    plot_peaks(
        [r1, r2, r3, r4],
        [g_r1, g_r2, g_r3, g_r4],
        ["30\u00B0C", "300\u00B0C", "600\u00B0C", "1000\u00B0C"],
        total_plot_filename,
    )

    # Call plot_zoomed_peaks with the four datasets for the zoomed-in plot.
    zoomed_plot_filename = "./data/zoomed_peaks_and_PDFs2.png"
    plot_zoomed_peaks(
        [r1, r2, r3, r4],
        [g_r1, g_r2, g_r3, g_r4],
        ["30\u00B0C", "300\u00B0C", "600\u00B0C", "1000\u00B0C"],
        zoomed_plot_filename,
    )

    return (
        total_plot_filename,
        zoomed_plot_filename,
    )  # Return filenames or paths of the saved PNG files
