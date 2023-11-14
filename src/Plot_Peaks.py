import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks


def find_and_plot_peaks(
    r, g_r
):  # also pass file name, from which to pull information to title plot (example below)
    """
    Locate the peaks (maxima) in G(r) data, and plot selected peaks along with the PDF.
    Args:
        r = extracted r data.
        g_r = extracted G(r) data, either raw or rescaled.
    Returns:
        NumPy array of indices at which selected maxima in G(r) are present.
        Saves a plot of PDF data with markers at certain peak positions as a PNG file.
    """
    peaks, _ = find_peaks(g_r, height=0)
    peaks = np.delete(peaks, np.where((peaks < 81) | (peaks > 3001)))
    plt.figure(figsize=(80, 40))
    plt.plot(r, g_r, color="b", linestyle="-", linewidth=5)
    plt.plot(r[peaks], g_r[peaks], linestyle=" ", marker="P", markersize=40)
    plt.title("PDF Data", fontsize=80, fontweight="bold", loc="center")
    plt.xlabel("r (\u00C5)", fontsize=70, loc="center")
    plt.xlim([0, 60])
    plt.xticks(np.arange(0, 61, 10), fontsize=55)
    plt.ylabel("G(r)", fontsize=70, loc="center")
    plt.yticks([], fontsize=55)
    plt.savefig("PDF_Data")
    # matplotlib.pyplot.suptitle('Silhouette Analysis of %d Clusters For %d-Component PCA' % (K,n_PCA_components), fontsize = 75,)
    plt.close()
    return peaks
