import math
from jes4py import *
import matplotlib.pyplot as plt


# =============================================================================
# MODULE: HISTOGRAM COMPUTATION (TASK 1)
# =============================================================================
def convert_to_grayscale_and_get_hist(pic):
    """
    Transforms the input image into a grayscale version and calculates
    the intensity distribution (histogram) manually.
    """
    hist = [0] * 256
    pixels = getPixels(pic)
    for p in pixels:
        r = getRed(p)
        g = getGreen(p)
        b = getBlue(p)
        # Applying the average method for grayscale conversion
        gray_value = int((r + g + b) / 3)
        setColor(p, makeColor(gray_value, gray_value, gray_value))
        hist[gray_value] += 1
    return hist, pic


def plot_histogram(hist, title_text):
    """
    Renders the histogram plot using Matplotlib visualization.
    """
    plt.figure(figsize=(8, 4))
    plt.bar(range(256), hist, color="gray", width=1)
    plt.title(title_text)
    plt.xlabel("Intensity Value (0-255)")
    plt.ylabel("Frequency")
    plt.xlim([0, 255])
    plt.grid(axis="y", alpha=0.3)
    # Non-blocking show allows viewing multiple results simultaneously
    plt.show(block=False)


# =============================================================================
# MODULE: CONTRAST ANALYSIS (TASK 2)
# =============================================================================
def get_min_max_intensity(pic):
    """
    Manually identifies the extreme intensity values within the image.
    """
    pixels = getPixels(pic)
    min_val = 255
    max_val = 0
    for p in pixels:
        val = getRed(p)
        if val < min_val:
            min_val = val
        if val > max_val:
            max_val = val
    return min_val, max_val


def compute_michelson_contrast(pic):
    """
    Computes Michelson Contrast based on manual min/max detection.
    """
    min_val, max_val = get_min_max_intensity(pic)
    if (max_val + min_val) == 0:
        return 0.0
    return float(max_val - min_val) / float(max_val + min_val)


def compute_rms_contrast(pic):
    """
    Computes RMS Contrast (Standard Deviation) manually.
    """
    pixels = getPixels(pic)
    total_pixels = len(pixels)
    if total_pixels == 0:
        return 0.0

    # Calculate Mean Intensity
    sum_intensity = 0
    for p in pixels:
        sum_intensity += getRed(p)
    mean_intensity = float(sum_intensity) / total_pixels

    # Calculate Sum of Squared Differences
    sum_squared_diff = 0
    for p in pixels:
        val = getRed(p)
        diff = val - mean_intensity
        sum_squared_diff += diff * diff
    variance = sum_squared_diff / total_pixels

    return math.sqrt(variance)


# =============================================================================
# MODULE: HISTOGRAM EQUALIZATION (TASK 3)
# =============================================================================
def equalize_histogram_manually(pic, hist):
    """
    Manual implementation of Histogram Equalization using CDF.
    """
    total_pixels = getWidth(pic) * getHeight(pic)

    # 1. Generate Cumulative Distribution Function (CDF)
    cdf = [0] * 256
    cdf[0] = hist[0]
    for i in range(1, 256):
        cdf[i] = cdf[i - 1] + hist[i]

    # 2. Identify CDF Minimum non-zero value
    cdf_min = 0
    for val in cdf:
        if val > 0:
            cdf_min = val
            break

    # 3. Create Mapping Table
    mapping = [0] * 256
    for i in range(256):
        numerator = cdf[i] - cdf_min
        denominator = total_pixels - cdf_min
        if denominator <= 0:
            mapping[i] = 0
        else:
            # Equalization formula mapping
            new_val = int(round((float(numerator) / denominator) * 255.0))
            mapping[i] = max(0, min(255, new_val))

    # 4. Apply transformation to the image
    new_hist = [0] * 256
    pixels = getPixels(pic)
    for p in pixels:
        old_val = getRed(p)
        new_mapped_val = mapping[old_val]
        setColor(p, makeColor(new_mapped_val, new_mapped_val, new_mapped_val))
        new_hist[new_mapped_val] += 1

    return new_hist, pic


# =============================================================================
# MODULE: INTEGRATED PIPELINE (TASK 4)
# =============================================================================
def run_analysis_pipeline(pic_path, category):
    """
    Orchestrates the full image processing workflow.
    """
    # Initialize Pictures & Apply Grayscale Mode Compatibility Fix
    original_pic = makePicture(pic_path)
    if original_pic.image.mode != "RGB":
        original_pic.image = original_pic.image.convert("RGB")

    proc_pic = makePicture(pic_path)
    if proc_pic.image.mode != "RGB":
        proc_pic.image = proc_pic.image.convert("RGB")

    # Process Tasks
    original_hist, gray_pic = convert_to_grayscale_and_get_hist(proc_pic)
    michelson = compute_michelson_contrast(gray_pic)
    rms = compute_rms_contrast(gray_pic)

    # Decision Logic
    needs_enhancement = michelson < 0.25 or rms < 40.0

    # Generate Results
    new_hist, equalized_pic = equalize_histogram_manually(gray_pic, original_hist)

    # Console Reporting Summary
    print("\n" + "=" * 50)
    print(f" ANALYSIS SUMMARY: {category.upper()}")
    print("=" * 50)
    print(f"1. Michelson Contrast : {michelson:.4f}")
    print(f"2. RMS Contrast       : {rms:.4f}")
    print(
        f"3. Decision           : {'Enhancement REQUIRED' if needs_enhancement else 'Enhancement NOT REQUIRED'}"
    )
    print("-" * 50)

    # Visualization
    show(original_pic)
    plot_histogram(original_hist, f"Initial Histogram ({category})")
    show(equalized_pic)
    plot_histogram(new_hist, f"Equalized Histogram ({category})")

    # Workflow Pause
    input(
        ">>> Process paused. Press ENTER to clear data and proceed to the next image..."
    )

    # Clean up plots for the next category
    plt.close("all")


# =============================================================================
# MAIN EXECUTION BLOCK
# =============================================================================
if __name__ == "__main__":
    # Test cases as per submission requirements
    test_categories = ["Low Contrast", "Normal Contrast", "High Contrast"]

    print("Starting Lab Assignment 1: Digital Image Processing Analysis")
    print("Sequential processing for required image categories initialized.")

    for category in test_categories:
        print(f"\nPrompt: Select image for category -> {category}")
        image_path = pickAFile()
        if image_path:
            run_analysis_pipeline(image_path, category)
        else:
            print(f"Category '{category}' selection was cancelled.")

    print("\nTask execution finalized. All data processed.")
