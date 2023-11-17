import matplotlib.pyplot as plt
import numpy as np

npz_file = "pdf_ramp_peaks.npz"


def plot_total_peaks(npz_file):
    """
    Identify and plot how the number of peaks changes across PDF samples.

    Args:
        npz_file: .npz file that contains a dictionary where the key is the file name and
        the value is a list of peak postions associated with that PDF.
    Returns:
        Histogram showing the total number of peaks for each PDF file.
    """
    my_dict = np.load(npz_file)
    new_dict = {}

    # Extract keys and values from npz and put in a new dictionary
    for item in my_dict:
        new_dict[item] = my_dict[item]

    # Make a dictionary where the key is file name, value is number of peaks
    num_peaks = {}
    for key in new_dict:
        num_peaks[key] = len(my_dict[key])

    # Select which keys to label on the x-axis (e.g., every 10th key)
    keys_to_label = list(num_peaks.keys())[::10]

    # Display all keys in a historgram
    keys_to_display = list(num_peaks.keys())
    values_to_display = [num_peaks[key] for key in keys_to_display]

    plt.bar(range(len(keys_to_display)), values_to_display, color="g")
    plt.xlabel("File Name")
    plt.ylabel("Number of Peaks")

    # Label only the selected keys for readability
    plt.xticks(
        range(len(keys_to_display)),
        [key if key in keys_to_label else "" for key in keys_to_display],
        rotation=90,
    )
    plt.xticks(rotation=45)
    plt.show()
