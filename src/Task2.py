import math
from jes4py import *

def get_min_max_intensity(pic):
    pixels = getPixels(pic)
    min_val = 255
    max_val = 0
    for p in pixels:
        val = getRed(p)
        if val < min_val: min_val = val
        if val > max_val: max_val = val
    return min_val, max_val

def compute_michelson_contrast(pic):
    min_val, max_val = get_min_max_intensity(pic)
    if (max_val + min_val) == 0:
        return 0.0
    return float(max_val - min_val) / float(max_val + min_val)

def compute_rms_contrast(pic):
    pixels = getPixels(pic)
    total_pixels = len(pixels)
    if total_pixels == 0: return 0.0
    
    sum_intensity = 0
    for p in pixels:
        sum_intensity += getRed(p)
    mean_intensity = float(sum_intensity) / total_pixels
    
    sum_squared_diff = 0
    for p in pixels:
        val = getRed(p)
        diff = val - mean_intensity
        sum_squared_diff += (diff * diff)
    variance = sum_squared_diff / total_pixels
    
    return math.sqrt(variance)

if __name__ == "__main__":
    path = pickAFile()
    if path:
        pic = makePicture(path)
        if pic.image.mode != 'RGB': 
            pic.image = pic.image.convert('RGB')
        
        # Pre-process: Main code logic requires grayscale before contrast check
        pixels = getPixels(pic)
        for p in pixels:
            gray = int((getRed(p) + getGreen(p) + getBlue(p)) / 3)
            setColor(p, makeColor(gray, gray, gray))
            
        michelson = compute_michelson_contrast(pic)
        rms = compute_rms_contrast(pic)
        needs_enhancement = (michelson < 0.25 or rms < 40.0)
        
        print("-" * 30)
        print(f"Michelson Contrast : {michelson:.4f}")
        print(f"RMS Contrast       : {rms:.4f}")
        print(f"Decision           : {'Enhancement REQUIRED' if needs_enhancement else 'Enhancement NOT REQUIRED'}")
        print("-" * 30) 
