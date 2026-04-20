from jes4py import *
import matplotlib.pyplot as plt


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
    # Each bin should ideally contain (total_pixels / 256) pixels.
    # We distribute the remainder across the first bins to keep integers.
    # ------------------------------------------------------------------
    base_count = total_pixels // 256
    remainder = total_pixels % 256
    feq = []
    for i in range(256):
        # First 'remainder' bins get one extra pixel to account for rounding
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
    for p in getPixels(pic):
        old_val = getRed(p)
        new_val = mapping[old_val]
        setColor(p, makeColor(new_val, new_val, new_val))
        new_hist[new_val] += 1

    return new_hist, pic


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


if __name__ == "__main__":
    path = pickAFile()
    if path:
        pic = makePicture(path)
        if pic.image.mode != "RGB":
            pic.image = pic.image.convert("RGB")

        # Convert to grayscale and compute initial histogram manually
        hist = [0] * 256
        pixels = getPixels(pic)
        for p in pixels:
            gray = int((getRed(p) + getGreen(p) + getBlue(p)) / 3)
            setColor(p, makeColor(gray, gray, gray))
            hist[gray] += 1

        show(pic)
        plot_histogram(hist, "Task 3: Before Equalization")

        new_hist, equalized_pic = equalize_histogram_manually(pic, hist)

        show(equalized_pic)
        plot_histogram(new_hist, "Task 3: After Equalization")

        input(">>> Equalization complete. Press ENTER to exit...")
        plt.close("all")
