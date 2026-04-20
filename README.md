# Histogram-Analysis-Lab
A Python implementation for manual histogram computation, contrast measurement, and histogram equalization.

## Group Members (Group 5)
This project was developed by the following students from the Department of Information Technology:

| Name | ID | Section |
| :--- | :--- | :--- |
| Abdullah Mubarak | 2342239 | IT3 |
| Abdulrahman Salem Al-Wasabi | 2343237 | IT3 |
| Hassan Ahmed Asiri | 2339657 | IT2 |
| Moath Abbas Eissa | 2338818 | IT2 |
| Osama Mazhud Al-Ghamdi | 2336767 | IT2 |

## Academic Information
* [cite_start]Course: CPIT 380 - Multimedia Technologies [cite: 9]
* [cite_start]Assignment: LAB Assignment 1 (Histogram Analysis & Contrast Enhancement) [cite: 7, 8]
* [cite_start]Submitted to: Prof. Saim Rasheed [cite: 10]
* [cite_start]University: King Abdulaziz University (KAU) [cite: 4]
* [cite_start]Faculty: Faculty of Computing and Information Technology (FCIT) [cite: 5]
* [cite_start]Academic Year: 2025/2026, Spring Semester [cite: 14]
* [cite_start]Date of Submission: Thursday, April 23, 2026 [cite: 13]

## Project Overview and Technical Explanations
This lab focuses on low-level image manipulation without the use of automated libraries like OpenCV. Every algorithm is implemented manually to demonstrate a deep understanding of image data structures.

### Task 1: Grayscale and Histogram Computation
The system transforms input RGB images into grayscale using the average intensity method. It then iterates through every pixel to build a frequency distribution (Histogram) representing the intensity levels from 0 to 255.

### Task 2: Contrast Metrics and Decision Logic
We implemented two primary mathematical models to assess image quality:
* Michelson Contrast: Measures the relation between the maximum and minimum pixel intensities.
* RMS Contrast: Calculates the standard deviation of pixel intensities to represent the overall spread.
The system automatically decides if an image requires enhancement based on these quantitative metrics.

### Task 3: Manual Histogram Equalization
This module enhances image contrast by spreading out the most frequent intensity values. This is achieved by:
1. Computing the Cumulative Distribution Function (CDF).
2. Normalizing the CDF values to the 0-255 range.
3. Remapping the original pixel values to their new, equalized levels.

### Task 4: Integrated Analysis Pipeline
A complete workflow that processes multiple test cases (Low, Normal, and High contrast images) sequentially, providing real-time console summaries and side-by-side visualizations.

## How to Run
1. Ensure the jes4py and matplotlib libraries are installed.
2. Clone the repository and navigate to the project directory.
3. Execute the integrated script: Task4_MainPipeline.py.
4. Follow the interactive prompts to select your image files for analysis.
