import matplotlib.pyplot as plt
import numpy as np


def plot_total_peaks(npz_file):
    """
    Identify and plot how the number of peaks changes across PDF samples.

    Args:
        npz_file: .npz file that contains a dictionary where the key is the file name and
        the value is a list of peak postions associated with that PDF.
    Returns:
        Histogram showing the total number of peaks for each PDF file.
    """
   data_from_npz = np.load(npz_file)
   npz_dict = {}

    # Extract keys and values from npz and store in a dictionary.
    for item in  data_from_npz:
        npz_dict[item] = data_from_npz[item]

    # Make a dictionary where the key is file name, value is number of peaks.
    number_of_peaks_dict = {}
    for key in npz_dict:
        number_of_peaks_dict[key] = len(data_from_npz[key])

    # Select which keys to label on the x-axis (e.g., every 10th key).
    keys_to_label = list(number_of_peaks_dict.keys())[::10]

    # Display all keys and values in a historgram.
    keys_to_display = list(number_of_peaks_dict.keys())
    values_to_display = [number_of_peaks_dict[key] for key in keys_to_display]

    plt.bar(range(len(keys_to_display)), values_to_display, color = "g")
    plt.xlabel("File Name")
    plt.ylabel("Number of Peaks")

    # Label only the selected keys for readability.
    plt.xticks(
        range(len(keys_to_display)),
        [key if key in keys_to_label else "" for key in keys_to_display],
        rotation = 90,
    )
    plt.xticks(rotation = 45)
    plt.tight_layout()
    plt.savefig('Total_Ramp_Peaks.png')
