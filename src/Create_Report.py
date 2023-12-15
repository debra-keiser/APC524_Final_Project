"""
Create_Report

Author: Sophia Bergen and Debra Keiser
Date Modified: 15DEC2023

Description:
This script retrieves PDF data, saves peak positions, and generates a portable document file displaying the results of various PDF analysis functions.
"""

# from Peak_Tracking import track_peaks
import os

import numpy as np
from Determine_Analytes import get_analyte_data
from Extract_Data import get_gr_files
from Integrate_Peaks import peak_integration
from Peak_Tracking import track_peaks
from Plot_PDFs import Plot_multiple_PDFs
from Plot_Total_Peaks import plot_total_peaks
from Read_Log_File import extract_time_temp_data
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import (
    Image,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
)


def preliminary_analysis():
    """
    Analyze time- and temperature-dependent pair distribution function (PDF) data.
    Details about the experiment are read from a log.txt file, and pair distribution function data are stored as .gr files.
    Args:
        None.
    Returns:
        Prints two NPZ files containing dictionaries of peaks from ramp and dwell data.
    """
    (
        recorded_times_from_experiment,
        recorded_temperatures_from_experiment,
        rounded_temperatures,
    ) = extract_time_temp_data("../data", "log.txt")

    analyte_times, analyte_temperatures = get_analyte_data(
        recorded_times_from_experiment,
        recorded_temperatures_from_experiment,
        rounded_temperatures,
    )

    pdf_ramp_peaks_dict, pdf_dwell_peaks_dict = get_gr_files(rounded_temperatures)

    np.savez(os.path.join("../data", "pdf_ramp_peaks.npz"), **pdf_ramp_peaks_dict)
    np.savez(os.path.join("../data", "pdf_dwell_peaks.npz"), **pdf_dwell_peaks_dict)


def create_report(file_path):
    doc = SimpleDocTemplate(file_path, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()

    # Title
    title = Paragraph(
        "<b>Automated Pair Distribution Function Analysis for Assessing Reaction Progress</b>",
        styles["Title"],
    )
    story.append(title)

    centered_style = ParagraphStyle(name="Centered", alignment=TA_CENTER)
    author_names = Paragraph(
        "<i>Authors: Sophia Bergen, Debra Keiser, and Meddelin Setiawan</i>",
        centered_style,
    )
    story.append(author_names)

    story.append(PageBreak())

    # Table of Contents
    toc_contents = [
        ("Visualizing PDFs Over Time", 2),
        ("Visualizing Total Number of Peaks Over Time", 2),
        ("Quantifying Peak Positions", 3),
        ("Peak Integration", 4),
    ]

    toc = []
    toc.append(Paragraph("<b>Table of Contents</b>", styles["Normal"]))
    toc.append(Spacer(1, 12))

    for title, page_num in toc_contents:
        toc_link = f"<link href=page{page_num}>{title}</link>"
        toc_entry = Paragraph(toc_link, styles["Normal"])
        toc.append(toc_entry)
        toc.append(Spacer(1, 6))

    story.extend(toc)
    story.append(PageBreak())

    # SECTION 1: PLOTTING
    story.append(
        Paragraph('<a name="page2"/>Section 1: PDF Curve Plotting', styles["Heading1"])
    )
    story.append(Paragraph("This section visualizes the PDF data.", styles["Normal"]))
    # add plot of PDFs on same figure

    total_img, zoom_img = Plot_multiple_PDFs()
    # Assuming 'story' is your report object in ReportLab
    # Add total_image to the report
    total_img_obj = Image(total_img)
    total_img_obj.drawWidth = 600
    total_img_obj.drawHeight = 450
    story.append(total_img_obj)

    # Add zoom_image to the report
    zoom_img_obj = Image(zoom_img)
    zoom_img_obj.drawWidth = 600
    zoom_img_obj.drawHeight = 450
    story.append(zoom_img_obj)
    story.append(PageBreak())

    # SECTION 2: PEAK HISTOGRAM
    story.append(
        Paragraph(
            '<a name="page3"/>Section 2: Visualizing Total Number of Peaks Over Time ',
            styles["Heading1"],
        )
    )
    story.append(
        Paragraph(
            "This section visualizes phase changes by counting the total number of peaks in PDF files across temperatures.",
            styles["Normal"],
        )
    )

    ramp_npz = "../data/pdf_ramp_peaks.npz"
    dwell_npz = "../data/pdf_dwell_peaks.npz"
    image_filename2 = plot_total_peaks(
        ramp_npz, save_path="../data/images/total_peaks_histogram.png"
    )
    img = Image(image_filename2)

    img.drawWidth = 600
    img.drawHeight = 400
    story.append(img)
    story.append(PageBreak())

    # SECTION 3: QUANTIFYING PEAK POSITIONS
    story.append(
        Paragraph(
            '<a name="page4"/>Section 3: Quantifying Peak Positions', styles["Heading1"]
        )
    )
    story.append(
        Paragraph(
            "This table shows select peak positions, in Angstroms, tracked across PDFs recorded at various temperatures. Full results of tracked peak postions are shown in tracked_peak_matrix.txt.",
            styles["Normal"],
        )
    )
    track_peaks(20)
    img = Image("../data/images/selected_tracked_peak_matrix.png")

    img.drawWidth = 600
    img.drawHeight = 400
    story.append(img)
    story.append(PageBreak())

    # SECTION 4: PEAK INTEGRATION
    story.append(
        Paragraph('<a name="page4"/>Section 4: Peak Integration', styles["Heading1"])
    )
    story.append(
        Paragraph(
            "This table lists relative differences between reference peak integrals (denoted 0) at a given temperature and peak integrals calculated at higher temperatures. These values are indicative of changes that occur to atomic coordination numbers as the structure of C-S-H changes.",
            styles["Normal"],
        )
    )
    image_filename4 = peak_integration(
        dwell_npz, save_path="../data/images/peak_integral_differences.png"
    )
    img = Image(image_filename4)

    img.drawWidth = 600
    img.drawHeight = 400
    story.append(img)
    story.append(PageBreak())

    doc.build(story)


# usage:
preliminary_analysis()

output_file_path = "../data/final_output_report.pdf"
create_report(output_file_path)

print(f"Report generated: {output_file_path}")
