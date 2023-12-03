import matplotlib.pyplot as plt
from Extract_Data import extract_pdf_data


def plot_peaks(r_list, g_r_list, labels):
    """
    Plot selected peaks along with the PDF.
    Args:
        r_list: List of r data arrays.
        g_r_list: List of G(r) data arrays, either raw or rescaled.
        labels: List of labels for each dataset.
    Returns:
        None (displays the plot).
    """
    plt.figure(figsize=(12, 8))  # Modify the figure size as needed
    for i in range(len(r_list)):
        plt.plot(r_list[i], g_r_list[i], label=labels[i])

    plt.title("PDF Data at Increasing Temperatures", fontsize=16)
    plt.xlabel("r (\u00C5)", fontsize=14)
    plt.ylabel("G(r)", fontsize=14)
    plt.legend()
    plt.grid(True)
    plt.show()


# Load data for the four PDFs.
r1, g_r1 = extract_pdf_data("../data/gr_files", "Synthetic_CSH_030degC_normalized.gr")
r2, g_r2 = extract_pdf_data(
    "../data/gr_files", "Synthetic_CSH_CSH_pdf_ramp_300_09_normalized.gr"
)
r3, g_r3 = extract_pdf_data(
    "../data/gr_files", "Synthetic_CSH_CSH_pdf_ramp_600_09_normalized.gr"
)
r4, g_r4 = extract_pdf_data(
    "../data/gr_files", "Synthetic_CSH_CSH_pdf_ramp_1000_09_normalized.gr"
)

# Call plot_peaks with the four datasets.
plot_peaks(
    [r1, r2, r3, r4],
    [g_r1, g_r2, g_r3, g_r4],
    ["30\u00B0C", "300\u00B0C", "600\u00B0C", "1000\u00B0C"],
)
