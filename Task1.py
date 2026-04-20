import matplotlib.pyplot as plt
from jes4py import *

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
    plt.show()

if __name__ == "__main__":
    path = pickAFile()
    if path:
        pic = makePicture(path)
        if pic.image.mode != 'RGB': 
            pic.image = pic.image.convert('RGB')
        
        hist, gray_pic = convert_to_grayscale_and_get_hist(pic)
        show(gray_pic)
        plot_histogram(hist, "Task 1: Histogram Analysis")