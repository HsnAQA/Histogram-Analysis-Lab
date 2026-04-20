import matplotlib.pyplot as plt
from jes4py import *


def convert_to_grayscale_and_get_hist(pic):
    """
    Transforms the input image into a grayscale version and calculates
    the intensity distribution (histogram) manually.

    Grayscale conversion uses the luminosity-weighted method:
        gray = 0.299*R + 0.587*G + 0.114*B
    This method is perceptually more accurate than simple averaging
    because the human eye is more sensitive to green than red or blue.
    (Simple average: gray = (R + G + B) / 3 — less perceptually accurate)
    """
    hist = [0] * 256
    pixels = getPixels(pic)
    for p in pixels:
        r = getRed(p)
        g = getGreen(p)
        b = getBlue(p)
        # Luminosity-weighted grayscale conversion (ITU-R BT.601 standard)
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


if __name__ == "__main__":
    path = pickAFile()
    if path:
        pic = makePicture(path)
        if pic.image.mode != "RGB":
            pic.image = pic.image.convert("RGB")

        hist, gray_pic = convert_to_grayscale_and_get_hist(pic)

        print("-" * 50)
        print("Task 1: Histogram Analysis")
        print(describe_distribution(hist))
        print("-" * 50)

        show(gray_pic)
        plot_histogram(hist, "Task 1: Grayscale Histogram")

        input(">>> Analysis complete. Press ENTER to exit...")
        plt.close("all")
