import random
import math
from PySide6.QtGui import QImage
from PIL import Image, ImageFilter
import numpy as np

# Helper functions for conversion to avoid repetition
def _qimage_to_pil(img: QImage) -> Image.Image:
    """Converts a QImage to a PIL Image."""
    # Ensure the QImage is in a format that Pillow can easily handle.
    if img.format() != QImage.Format.Format_ARGB32:
        img = img.convertToFormat(QImage.Format.Format_ARGB32)
    
    buffer = img.bits().tobytes() # type: ignore
    pil_img = Image.frombytes("RGBA", (img.width(), img.height()), buffer, "raw", "BGRA")
    return pil_img

def _pil_to_qimage(pil_img: Image.Image) -> QImage:
    """Converts a PIL Image to a QImage."""
    w, h = pil_img.size
    # Ensure the PIL image is in RGBA format for consistency
    data = pil_img.convert("RGBA").tobytes()
    q_img = QImage(data, w, h, QImage.Format.Format_RGBA8888)
    return q_img.copy()


def melt_image(img: QImage, amount: int = 30) -> QImage:
    """Applies a vertical melt/drip effect to the image."""
    if amount <= 0:
        return img.copy()
        
    pil_img = _qimage_to_pil(img)
    arr = np.array(pil_img)
    h, w, _ = arr.shape

    for x in range(w):
        shift = random.randint(0, amount)
        if shift > 0:
            arr[:, x] = np.roll(arr[:, x], shift, axis=0)

    pil_out = Image.fromarray(arr)
    return _pil_to_qimage(pil_out)


def shear_image(img: QImage, amount: int = 40, horizontal: bool = True, direction: int = 1) -> QImage:
    """Applies a shear effect to the image."""
    pil_img = _qimage_to_pil(img)
    arr = np.array(pil_img)
    h, w, _ = arr.shape

    if horizontal:
        for y in range(h):
            shift = int((y / h) * amount) * direction
            arr[y] = np.roll(arr[y], shift, axis=0)
    else:
        for x in range(w):
            shift = int((x / w) * amount) * direction
            arr[:, x] = np.roll(arr[:, x], shift, axis=0)
            
    pil_out = Image.fromarray(arr)
    return _pil_to_qimage(pil_out)


def blur_image(img: QImage, radius: int = 3) -> QImage:
    """Applies a box blur to the image using Pillow."""
    if radius <= 0:
        return img.copy()
    pil_img = _qimage_to_pil(img)
    pil_blurred = pil_img.filter(ImageFilter.BoxBlur(radius))
    return _pil_to_qimage(pil_blurred)


def mosaic_image(img: QImage, block_size: int = 10) -> QImage:
    """Applies a mosaic/pixelate effect to the image using Pillow."""
    if block_size <= 1:
        return img.copy()
    pil_img = _qimage_to_pil(img)
    w, h = pil_img.size

    # To prevent division by zero if block_size is larger than image dimensions
    if block_size > w or block_size > h:
        return img.copy()

    # Downscale and then upscale to create the pixelated effect
    temp = pil_img.resize((w // block_size, h // block_size), Image.Resampling.NEAREST)
    pil_mosaic = temp.resize((w, h), Image.Resampling.NEAREST)
    return _pil_to_qimage(pil_mosaic)