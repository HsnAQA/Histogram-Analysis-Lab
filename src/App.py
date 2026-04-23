import os
import matplotlib.pyplot as plt
from jes4py import *

from tasks.histogram_computation import convert_to_grayscale_and_get_hist, describe_distribution
from tasks.contrast_measurement import compute_michelson_contrast, compute_rms_contrast
from tasks.histogram_equalization import equalize_histogram_manually

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def show_step(pic, hist, title, filename):
    """
    Displays the image and its histogram side-by-side in one window.
    Closing the window advances to the next step.
    """
    fig, (ax_img, ax_hist) = plt.subplots(1, 2, figsize=(14, 5))

    ax_img.imshow(pic.image, cmap="gray")
    ax_img.axis("off")
    ax_img.set_title(title)

    ax_hist.bar(range(256), hist, color="gray", width=1)
    ax_hist.set_xlim([0, 255])
    ax_hist.set_xlabel("Intensity Value (0-255)")
    ax_hist.set_ylabel("Frequency")
    ax_hist.set_title(f"Histogram — {title}")
    ax_hist.grid(axis="y", alpha=0.3)

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, filename), dpi=100)
    plt.show()


# =============================================================================
# INTEGRATED PIPELINE (TASK 4)
# =============================================================================
def run_analysis_pipeline(pic_path, category, is_last=False):
    """
    Orchestrates the full image processing workflow for a single image.
    """
    safe_cat = category.replace(" ", "_")

    original_pic = makePicture(pic_path)
    if original_pic.image.mode != "RGB":
        original_pic.image = original_pic.image.convert("RGB")

    proc_pic = makePicture(pic_path)
    if proc_pic.image.mode != "RGB":
        proc_pic.image = proc_pic.image.convert("RGB")

    # Task 1: Grayscale + Histogram
    original_hist, gray_pic = convert_to_grayscale_and_get_hist(proc_pic)
    distribution_desc = describe_distribution(original_hist)

    # Task 2: Contrast Measurement
    michelson = compute_michelson_contrast(gray_pic)
    rms = compute_rms_contrast(gray_pic)
    needs_enhancement = michelson < 0.25 or rms < 40.0

    michelson_label = "Low" if michelson < 0.25 else "Normal" if michelson <= 0.75 else "High"
    rms_label = "Low" if rms < 40.0 else "Normal" if rms <= 80.0 else "High"

    # Task 3: Histogram Equalization
    new_hist, equalized_pic = equalize_histogram_manually(gray_pic, original_hist)

    # Console summary
    print("\n" + "=" * 55)
    print(f"  ANALYSIS SUMMARY: {category.upper()} — {os.path.basename(pic_path)}")
    print("=" * 55)
    print(f"Distribution  : {distribution_desc}")
    print(f"Michelson     : {michelson:.4f}  → {michelson_label} contrast")
    print(f"RMS           : {rms:.4f}  → {rms_label} contrast")
    print(f"Decision      : {'Enhancement REQUIRED' if needs_enhancement else 'Enhancement NOT REQUIRED'}")
    print("-" * 55)

    # Display: photo + histogram together in one window per step.
    # Closing the window advances to the next step.
    show_step(original_pic, original_hist, f"Before Equalization — {category}", f"{safe_cat}_before.png")
    show_step(equalized_pic, new_hist, f"After Equalization — {category}", f"{safe_cat}_after.png")


# =============================================================================
# MAIN
# =============================================================================
if __name__ == "__main__":
    test_categories = ["Low Contrast", "Normal Contrast", "High Contrast"]

    print("=" * 55)
    print("  Histogram Analysis & Contrast Enhancement")
    print("=" * 55)
    print("You will be prompted to select 3 images (Low / Normal / High contrast).")
    print(f"Outputs will be saved to: {OUTPUT_DIR}")

    for index, category in enumerate(test_categories):
        print(f"\n>>> [{category}] Press ENTER to open file picker...")
        input()
        image_path = pickAFile()
        if image_path:
            is_last = index == len(test_categories) - 1
            run_analysis_pipeline(image_path, category, is_last)
        else:
            print(f"  Selection cancelled for '{category}'. Skipping.")

    print("\nTask complete.")
