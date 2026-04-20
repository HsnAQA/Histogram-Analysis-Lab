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
* Course: CPIT 380 - Multimedia Technologies
* Assignment: LAB Assignment 1 (Histogram Analysis & Contrast Enhancement)
* Submitted to: Prof. Saim Rasheed
* University: King Abdulaziz University (KAU)
* Faculty: Faculty of Computing and Information Technology (FCIT)
* Academic Year: 2025/2026, Spring Semester
* Date of Submission: Thursday, April 23, 2026

## Technical Overview and Analysis Categories
This project explores how digital images store and distribute light intensity. We categorize and analyze images based on their dynamic range:

### 1. Image Contrast Categories
* **Low Contrast Images:** These images have a narrow range of intensity values. In the histogram, pixels are "clumped" together in a small area (usually the middle or one side), resulting in a "washed-out" look with very little distinction between dark and light areas.
* **Normal Contrast Images:** These images display a healthy balance of light and dark. The histogram shows a broad distribution across the intensity scale (0-255), providing clear details and natural transitions.
* **High Contrast Images:** These images have extreme differences between light and dark areas. The histogram often shows high peaks at both the very dark (0) and very bright (255) ends, with fewer mid-tones.

### 2. Manual Implementation Tasks
* **Task 1: Grayscale and Histogram Logic:** We convert RGB data into a single intensity channel using the average method. The histogram is then built manually by counting the occurrence of each intensity level from 0 to 255.
* **Task 2: Quantitative Metrics:** * **Michelson Contrast:** Focuses on the extreme pixel values (Min and Max) to determine the image's overall reach.
    * **RMS Contrast:** Uses the standard deviation to measure how much pixel intensities vary from the average.
* **Task 3: Enhancement via Equalization:** For images identified as "Low Contrast," the system applies Histogram Equalization. By calculating the Cumulative Distribution Function (CDF), we stretch the "clumped" pixels across the full 0-255 range to reveal hidden details.

### 3. Integrated Pipeline
The system is designed to handle multiple test cases sequentially. It provides a real-time console summary and visualizes the transformation from the original state to the enhanced state.

## How to Run
1. Ensure the jes4py and matplotlib libraries are installed.
2. Clone the repository and navigate to the project directory.
3. Execute the integrated script: Task4_MainPipeline.py.
4. Follow the interactive prompts to select your image files for analysis.
