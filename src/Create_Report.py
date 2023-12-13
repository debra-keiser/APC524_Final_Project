"""""
Create_Report

Author: Sophia Bergen
Date Modified: 08DEC2023

Description:
This script will generate a PDF displaying the results of various PDF analysis functions.
""" ""

# from Peak_Tracking import track_peaks
from Plot_PDFs import Plot_multiple_PDFs
from Plot_Total_Peaks import plot_total_peaks
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
    story.append(Paragraph("This section visualizes the PDF data", styles["Normal"]))
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
            "This section visualizes phase changes by counting the total number of peaks in PDF files across temperatures",
            styles["Normal"],
        )
    )

    npz = "./data/pdf_ramp_peaks.npz"
    image_filename2 = plot_total_peaks(
        npz, save_path="./data/images/total_peaks_histogram.png"
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
            "The results of quanitfying peak postions are in text file called tracked_peak_matrix.txt in the data folder!",
            styles["Normal"],
        )
    )
    story.append(PageBreak())

    # SECTION 4: PEAK INTEGRATION
    story.append(
        Paragraph('<a name="page4"/>Section 4: Peak Integration', styles["Heading1"])
    )
    story.append(
        Paragraph(
            "This table lists relative differences between reference peak integrals (denoted 0) at a given temperature and peak integrals calculated at higher temperatures. These values are indicative of changes that occur to atomic coordination numbers as the structure of C-S-H changes",
            styles["Normal"],
        )
    )
    image_filename4 = (
        "./data/images/Dwell_Temperature_Atomic_Coordination_Number_Changes.png"
    )
    img = Image(image_filename4)

    img.drawWidth = 600
    img.drawHeight = 400
    story.append(img)
    story.append(PageBreak())

    doc.build(story)


# usage:
output_file_path = "./data/final_output_report.pdf"

create_report(output_file_path)
print(f"Report generated: {output_file_path}")
