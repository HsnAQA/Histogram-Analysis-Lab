import math
import os
from jes4py import *

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../..", "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)


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
    Interpretation (as per lecture):
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
    Since intensity ranges from 0-255, the maximum possible std dev is ~127.5
    (when half pixels are 0 and half are 255). A threshold of 40.0 represents
    roughly 31% of that maximum, which aligns with the low-contrast boundary
    used in the Michelson scale (0.25).
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


def decide_enhancement(michelson, rms):
    """
    Determines whether contrast enhancement is needed based on both metrics.
    Enhancement is recommended when EITHER metric indicates low contrast:
        - Michelson < 0.25  (as defined in the lecture slides)
        - RMS < 40.0        (approximately 31% of max possible std dev ~127.5)
    """
    return michelson < 0.25 or rms < 40.0


if __name__ == "__main__":
    path = pickAFile()
    if path:
        pic = makePicture(path)
        if pic.image.mode != "RGB":
            pic.image = pic.image.convert("RGB")

        # Pre-process: convert to grayscale before contrast measurement
        pixels = getPixels(pic)
        for p in pixels:
            gray = int((getRed(p) + getGreen(p) + getBlue(p)) / 3)
            setColor(p, makeColor(gray, gray, gray))

        pic.image.save(os.path.join(OUTPUT_DIR, "task2_grayscale.png"))

        michelson = compute_michelson_contrast(pic)
        rms = compute_rms_contrast(pic)
        needs_enhancement = decide_enhancement(michelson, rms)

        print("-" * 40)
        print(f"Michelson Contrast : {michelson:.4f}")
        print(f"  → {'Low' if michelson < 0.25 else 'Normal' if michelson <= 0.75 else 'High'} contrast")
        print(f"RMS Contrast       : {rms:.4f}")
        print(f"  → {'Low' if rms < 40.0 else 'Normal' if rms <= 80.0 else 'High'} contrast")
        print(f"Decision           : {'Enhancement REQUIRED' if needs_enhancement else 'Enhancement NOT REQUIRED'}")
        print("-" * 40)
