from jes4py import *

def equalize_histogram_manually(pic, hist):
    total_pixels = getWidth(pic) * getHeight(pic)
    
    cdf = [0] * 256
    cdf[0] = hist[0]
    for i in range(1, 256):
        cdf[i] = cdf[i-1] + hist[i]
        
    cdf_min = 0
    for val in cdf:
        if val > 0:
            cdf_min = val
            break
            
    mapping = [0] * 256
    for i in range(256):
        denominator = total_pixels - cdf_min
        if denominator <= 0:
            mapping[i] = 0
        else:
            new_val = int(round((float(cdf[i] - cdf_min) / denominator) * 255.0))
            mapping[i] = max(0, min(255, new_val))
            
    for p in getPixels(pic):
        new_mapped_val = mapping[getRed(p)]
        setColor(p, makeColor(new_mapped_val, new_mapped_val, new_mapped_val))
        
    return pic

if __name__ == "__main__":
    path = pickAFile()
    if path:
        pic = makePicture(path)
        if pic.image.mode != 'RGB': 
            pic.image = pic.image.convert('RGB')
        
        # Initial Grayscale & Hist (as required by the main logic)
        hist = [0] * 256
        pixels = getPixels(pic)
        for p in pixels:
            gray = int((getRed(p) + getGreen(p) + getBlue(p)) / 3)
            setColor(p, makeColor(gray, gray, gray))
            hist[gray] += 1
            
        show(pic) # Before
        equalized_pic = equalize_histogram_manually(pic, hist)
        show(equalized_pic) # After