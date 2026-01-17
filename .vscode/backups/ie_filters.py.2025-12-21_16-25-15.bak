from PySide6.QtGui import QImage
from PIL import Image
import numpy as np

# Helper functions for conversion moved here for consistency if this file becomes standalone.
# If ie_functions is always available, these can be imported instead.
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


def apply_sepia(img: QImage) -> QImage:
    """
    Applies a sepia filter to the QImage.
    """
    pil_img = _qimage_to_pil(img)
    
    # Ensure image is in RGB mode for manipulation
    if pil_img.mode != 'RGB':
        pil_img = pil_img.convert('RGB')
        
    # Get pixel data as a numpy array for fast processing
    pixels = np.array(pil_img)
    
    # Sepia formula weights
    sepia_matrix = np.array([
        [0.393, 0.769, 0.189],
        [0.349, 0.686, 0.168],
        [0.272, 0.534, 0.131]
    ])
    
    # Apply the sepia transformation
    # We need to reshape the pixel array to be (W*H, 3) to multiply with the (3,3) sepia matrix
    transformed_pixels = pixels.reshape(-1, 3) @ sepia_matrix.T
    
    # Clip values to the valid range [0, 255]
    transformed_pixels = np.clip(transformed_pixels, 0, 255)
    
    # Reshape back to the original image dimensions
    pixels = transformed_pixels.reshape(pixels.shape).astype(np.uint8)
    
    # Create a new PIL image from the modified pixel data
    sepia_img = Image.fromarray(pixels)
    
    # Convert back to QImage
    return _pil_to_qimage(sepia_img)
