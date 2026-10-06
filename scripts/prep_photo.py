"""
Prepare the photo for clean ASCII conversion:
1. Frame the subject properly (face & upper body).
2. Enhance contrast and sharpness so facial features stand out.
3. Clean the background to pure white (renders as empty space in ASCII).
4. Save source-prepped.png.
"""
import sys, os
from PIL import Image, ImageEnhance, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
INP = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "source-photo.png")
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "..", "source-prepped.png")

def prep():
    img = Image.open(INP).convert("RGB")
    w, h = img.size
    
    # Framing focusing on head & upper body
    crop_box = (int(w * 0.05), int(h * 0.06), int(w * 0.95), int(h * 0.94))
    img = img.crop(crop_box)
    
    # Convert to grayscale
    gray = img.convert("L")
    
    # Enhance contrast
    gray = ImageEnhance.Contrast(gray).enhance(1.45)
    
    # Push light background to pure white (255) so it dissolves in ASCII
    lut = []
    for i in range(256):
        if i >= 210:
            lut.append(255)
        elif i <= 80:
            lut.append(int(i * 0.75))
        else:
            lut.append(i)
    gray = gray.point(lut)
    
    gray = gray.filter(ImageFilter.SHARPEN)
    
    # Square canvas
    side = max(gray.size)
    canvas = Image.new("L", (side, side), 255)
    offset = ((side - gray.size[0]) // 2, (side - gray.size[1]) // 2)
    canvas.paste(gray, offset)
    
    canvas.save(OUT)
    print(f"wrote {OUT} {canvas.size}")

if __name__ == "__main__":
    prep()
