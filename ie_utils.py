from PySide6.QtGui import QImage
from PIL import Image

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
