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

    Grayscale conversion uses the luminosity-weighted method:
        gray = 0.299*R + 0.587*G + 0.114*B
    This is perceptually more accurate than simple averaging because
    the human eye is more sensitive to green than red or blue.
    (ITU-R BT.601 standard)
    """
    hist = [0] * 256
    pixels = getPixels(pic)
    for p in pixels:
        r = getRed(p)
        g = getGreen(p)
        b = getBlue(p)
        # Luminosity-weighted grayscale conversion
        gray_value = int(0.299 * r + 0.587 * g + 0.114 * b)
        gray_value = max(0, min(255, gray_value))
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
    plt.tight_layout()
    # Non-blocking show allows viewing multiple results simultaneously
    plt.show(block=False)


def describe_distribution(hist):
    """
    Provides a brief textual analysis of the histogram distribution.
    Identifies whether the distribution is clustered or spread
    based on the actual min and max intensity values present in the image.
    """
    total = sum(hist)
    if total == 0:
        return "No data."

    # Find actual min and max intensity values that have at least one pixel
    min_intensity = 0
    max_intensity = 255
    for i in range(256):
        if hist[i] > 0:
            min_intensity = i
            break
    for i in range(255, -1, -1):
        if hist[i] > 0:
            max_intensity = i
            break

    spread = max_intensity - min_intensity
    non_zero_bins = sum(1 for v in hist if v > 0)

    if spread < 60:
        distribution_type = "Clustered — Low Contrast"
    elif spread < 150:
        distribution_type = "Moderately spread — Normal Contrast"
    else:
        distribution_type = "Widely spread — High Contrast"

    return (
        f"Intensity range: {min_intensity}–{max_intensity} "
        f"(spread={spread}, active bins={non_zero_bins}/256). "
        f"{distribution_type}."
    )


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
    Computes Michelson Contrast: (max - min) / (max + min).
    Interpretation (as per lecture slides):
        - Close to 0      → Low contrast
        - 0.25 to 0.75    → Normal contrast
        - Close to 1      → High contrast
    """
    min_val, max_val = get_min_max_intensity(pic)
    if (max_val + min_val) == 0:
        return 0.0
    return float(max_val - min_val) / float(max_val + min_val)


def compute_rms_contrast(pic):
    """
    Computes RMS Contrast (Standard Deviation of pixel intensities).
    Since intensity ranges 0–255, the max possible std dev is ~127.5.
    A threshold of 40.0 (~31% of max) aligns proportionally with the
    Michelson low-contrast boundary of 0.25.
    Interpretation:
        - Below 40   → Low contrast  (enhancement recommended)
        - 40 to 80   → Normal contrast
        - Above 80   → High contrast
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

    # Calculate Sum of Squared Differences from Mean
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
    Manual implementation of Histogram Equalization following the exact
    4-step algorithm as presented in the CPIT380 lecture slides.

    Algorithm Steps:
        Step 1: Compute the CDF (Cumulative Frequency Distribution) of the original histogram.
        Step 2: Compute Feq — the ideal equalized histogram (total_pixels / 256 per bin).
        Step 3: Compute CuFeq — the cumulative frequency of the equalized histogram.
        Step 4: Design the mapping — for each original intensity, find the output intensity
                whose CuFeq is closest to the original CDF value.
    """
    total_pixels = getWidth(pic) * getHeight(pic)

    # ------------------------------------------------------------------
    # Step 1: Compute CDF of the original histogram
    # cdf[i] = total number of pixels with intensity <= i
    # ------------------------------------------------------------------
    cdf = [0] * 256
    cdf[0] = hist[0]
    for i in range(1, 256):
        cdf[i] = cdf[i - 1] + hist[i]

    # ------------------------------------------------------------------
    # Step 2: Compute Feq — the ideal equalized histogram
    # Each bin ideally holds (total_pixels / 256) pixels.
    # Remainder pixels are distributed across the first bins.
    # ------------------------------------------------------------------
    base_count = total_pixels // 256
    remainder = total_pixels % 256
    feq = []
    for i in range(256):
        feq.append(base_count + (1 if i < remainder else 0))

    # ------------------------------------------------------------------
    # Step 3: Compute CuFeq — cumulative frequency of the equalized histogram
    # ------------------------------------------------------------------
    cufeq = [0] * 256
    cufeq[0] = feq[0]
    for i in range(1, 256):
        cufeq[i] = cufeq[i - 1] + feq[i]

    # ------------------------------------------------------------------
    # Step 4: Design the mapping
    # For each input intensity, find the output intensity whose CuFeq
    # is closest to the input's CDF value (as shown in the lecture slides).
    # ------------------------------------------------------------------
    mapping = [0] * 256
    for i in range(256):
        target = cdf[i]
        best_match = 0
        best_diff = abs(cufeq[0] - target)
        for j in range(1, 256):
            diff = abs(cufeq[j] - target)
            if diff < best_diff:
                best_diff = diff
                best_match = j
        mapping[i] = best_match

    # Apply the mapping and build the new histogram for verification
    new_hist = [0] * 256
    pixels = getPixels(pic)
    for p in pixels:
        old_val = getRed(p)
        new_val = mapping[old_val]
        setColor(p, makeColor(new_val, new_val, new_val))
        new_hist[new_val] += 1

    return new_hist, pic


# =============================================================================
# MODULE: INTEGRATED PIPELINE (TASK 4)
# =============================================================================
def run_analysis_pipeline(pic_path, category, is_last=False):
    """
    Orchestrates the full image processing workflow for a single image.
    """
    # Initialize Pictures & Apply Grayscale Mode Compatibility Fix
    original_pic = makePicture(pic_path)
    if original_pic.image.mode != "RGB":
        original_pic.image = original_pic.image.convert("RGB")

    proc_pic = makePicture(pic_path)
    if proc_pic.image.mode != "RGB":
        proc_pic.image = proc_pic.image.convert("RGB")

    # --- Task 1: Grayscale + Histogram ---
    original_hist, gray_pic = convert_to_grayscale_and_get_hist(proc_pic)
    distribution_desc = describe_distribution(original_hist)

    # --- Task 2: Contrast Measurement ---
    michelson = compute_michelson_contrast(gray_pic)
    rms = compute_rms_contrast(gray_pic)
    needs_enhancement = michelson < 0.25 or rms < 40.0

    michelson_label = (
        "Low" if michelson < 0.25 else "Normal" if michelson <= 0.75 else "High"
    )
    rms_label = "Low" if rms < 40.0 else "Normal" if rms <= 80.0 else "High"

    # --- Task 3: Histogram Equalization ---
    new_hist, equalized_pic = equalize_histogram_manually(gray_pic, original_hist)

    # --- Console Reporting Summary ---
    print("\n" + "=" * 55)
    print(f"  ANALYSIS SUMMARY: {category.upper()}")
    print("=" * 55)
    print(f"Distribution  : {distribution_desc}")
    print(f"Michelson     : {michelson:.4f}  → {michelson_label} contrast")
    print(f"RMS           : {rms:.4f}  → {rms_label} contrast")
    print(
        f"Decision      : {'Enhancement REQUIRED' if needs_enhancement else 'Enhancement NOT REQUIRED'}"
    )
    print("-" * 55)

    # --- Visualization ---
    show(original_pic)
    plot_histogram(original_hist, f"Before Equalization ({category})")
    show(equalized_pic)
    plot_histogram(new_hist, f"After Equalization ({category})")

    # Workflow Pause — message changes based on whether this is the last image
    if is_last:
        input(">>> All images processed. Press ENTER to exit the program...")
    else:
        input(">>> Press ENTER to proceed to the next image...")
    plt.close("all")


# =============================================================================
# MAIN EXECUTION BLOCK
# =============================================================================
if __name__ == "__main__":
    test_categories = ["Low Contrast", "Normal Contrast", "High Contrast"]

    print("=" * 55)
    print("  Lab Assignment 1: Histogram Analysis & Contrast Enhancement")
    print("=" * 55)
    print("You will be prompted to select 3 images (Low / Normal / High contrast).")

    for index, category in enumerate(test_categories):
        print(f"\n>>> Select image for: {category}")
        image_path = pickAFile()
        if image_path:
            is_last = index == len(test_categories) - 1
            run_analysis_pipeline(image_path, category, is_last)
        else:
            print(f"  Selection cancelled for '{category}'. Skipping.")

    print("\nTask complete.") 
