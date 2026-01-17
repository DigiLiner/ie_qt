from PySide6.QtGui import QImage
from PIL import Image
import numpy as np

from ie_utils import _qimage_to_pil, _pil_to_qimage


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
