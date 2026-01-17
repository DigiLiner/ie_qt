import math
import random
from collections import deque
from typing import Set,Tuple, Callable

from PySide6.QtGui import QImage, QPixmap, QPainter, QColor, QPen, QRadialGradient, QBrush, QPolygon, QPainterPath, \
    QLinearGradient, QBitmap, QRegion
from PySide6.QtCore import QPoint, QRect, Qt, QPointF, QSize, QRectF
import ie_globals
import PySide6.QtCore

def _apply_selection_clip(painter: QPainter):
    """
    Applies the pre-calculated global clipping region to the painter.
    """
    if ie_globals.has_selection and ie_globals.selection_region:
        painter.setClipRegion(ie_globals.selection_region)

def is_point_in_selection(x: int, y: int) -> bool:
    """
    Checks if a point is inside the pre-calculated global selection region.
    """
    if not ie_globals.has_selection or not ie_globals.selection_region:
        return True
    return ie_globals.selection_region.contains(QPoint(x, y))


def draw_pen(img1: QImage, start_pos: QPoint, end_pos: QPoint):
    painter = QPainter(img1)
    _apply_selection_clip(painter)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setPen(ie_globals.current_pen)
    painter.drawLine(start_pos, end_pos)
    painter.end()

def draw_line(img1: QImage, pt1: QPoint, pt2: QPoint, task: str):
    if task != "move": return
    painter = QPainter(img1)
    _apply_selection_clip(painter)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setPen(ie_globals.current_pen)
    painter.drawLine(pt1, pt2)
    painter.end()


def draw_brush(img: QImage, pos: QPoint, angle: float = 0.0):
    painter = QPainter(img)
    _apply_selection_clip(painter)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    
    size = ie_globals.brush_size
    hardness = ie_globals.brush_hardness / 100.0
    color = ie_globals.current_pen.color()
    
    painter.save()
    painter.translate(pos)
    
    rect = QRect(-size // 2, -size // 2, size, size)
    
    gradient = QRadialGradient(QPoint(0,0), size / 2)
    center_color = QColor(color)
    edge_color = QColor(color)
    edge_color.setAlpha(0)
    
    gradient.setColorAt(0, center_color)
    gradient.setColorAt(hardness, center_color)
    gradient.setColorAt(1.0, edge_color)
    
    painter.setBrush(QBrush(gradient))
    painter.setPen(Qt.PenStyle.NoPen)
    painter.drawEllipse(rect)
    
    painter.restore()
    painter.end()


def draw_circle(img1: QImage,  pt1:QPoint, pt2:QPoint,task:str) -> None:
    if task != "move": return
    painter = QPainter(img1)
    _apply_selection_clip(painter)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    radius = math.trunc(math.hypot(pt1.x() - pt2.x(), pt1.y() - pt2.y()))
    painter.setPen(ie_globals.current_pen)
    painter.setBrush(ie_globals.current_brush)
    painter.drawEllipse(pt1, radius, radius)
    painter.end()

def draw_circle_outline(img1: QImage,  pt1:QPoint, pt2:QPoint,task:str) -> None:
    if task != "move": return
    painter = QPainter(img1)
    _apply_selection_clip(painter)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    radius = math.trunc(math.hypot(pt1.x() - pt2.x(), pt1.y() - pt2.y()))
    painter.setPen(ie_globals.current_pen)
    painter.setBrush(Qt.BrushStyle.NoBrush)
    painter.drawEllipse(pt1, radius, radius)
    painter.end()


def draw_rect(img1: QImage,  pt1:QPoint, pt2:QPoint,task:str) -> None:
    if task != "move": return
    painter = QPainter(img1)
    _apply_selection_clip(painter)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setPen(ie_globals.current_pen)
    painter.setBrush(ie_globals.current_brush)
    painter.drawRect(QRect(pt1, pt2))
    painter.end()

def draw_round_rect(img1: QImage,  pt1:QPoint, pt2:QPoint,task:str,corner_radius:int=10) -> None:
    if task != "move": return
    painter = QPainter(img1)
    _apply_selection_clip(painter)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setPen(ie_globals.current_pen)
    painter.setBrush(ie_globals.current_brush)
    painter.drawRoundedRect(QRect(pt1, pt2), corner_radius, corner_radius)
    painter.end()

def draw_spray(img1: QImage, pt1:QPoint,task:str):
    if task != "move": return
    painter = QPainter(img1)
    painter.setPen(ie_globals.current_pen)
    for _ in range(ie_globals.spray_density):
        x = int(pt1.x() + random.gauss(0, ie_globals.spray_radius))
        y = int(pt1.y() + random.gauss(0, ie_globals.spray_radius))
        if is_point_in_selection(x, y):
            painter.drawPoint(x, y)
    painter.end()

def erase(img1: QImage, start_pos: QPoint, end_pos: QPoint, task: str) -> None:
    """
    Erases a part of the image using a soft brush with opacity and hardness control.
    """
    if task not in ["down", "move"]: return

    painter = QPainter(img1)
    _apply_selection_clip(painter)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_DestinationOut)

    # --- Interpolate points for a smooth line ---
    length = math.hypot(end_pos.x() - start_pos.x(), end_pos.y() - start_pos.y())
    if length < 1:
        num_steps = 1
    else:
        # Dab spacing should be less than the brush radius
        spacing = ie_globals.brush_size / 3.0
        num_steps = int(length / spacing) + 1

    for i in range(num_steps + 1):
        t = i / num_steps
        current_pos = QPointF(start_pos) * (1.0 - t) + QPointF(end_pos) * t

        # --- Create soft brush gradient for each dab ---
        size = ie_globals.brush_size
        hardness = ie_globals.brush_hardness / 100.0
        # For DestinationOut, only the alpha channel matters.
        # We get the global opacity from the current pen.
        opacity = ie_globals.current_pen.color().alphaF()

        rect = QRectF(
            current_pos.x() - size / 2, current_pos.y() - size / 2,
            size, size
        )

        gradient = QRadialGradient(current_pos, size / 2)

        # Center of the brush: Black with global opacity
        center_color = QColor(0, 0, 0, int(255 * opacity))
        # Edge of the brush: Fully transparent
        edge_color = QColor(0, 0, 0, 0)

        gradient.setColorAt(0, center_color)
        # Hardness determines where the full opacity ends
        gradient.setColorAt(hardness, center_color)
        # Fade to transparent at the edge
        gradient.setColorAt(1.0, edge_color)

        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(rect)

    painter.end()


def fill(img1: QImage, pt1: QPoint, task: str,tolerance:float) -> None:
    if task != "down": return

    w, h = img1.width(), img1.height()
    start_x, start_y = pt1.x(), pt1.y()

    if not (0 <= start_x < w and 0 <= start_y < h): return
    
    if ie_globals.has_selection and not is_point_in_selection(start_x, start_y):
        return

    target_color = img1.pixelColor(start_x, start_y)
    fill_color = ie_globals.current_brush.color()

    if target_color == fill_color: return

    queue = deque([(start_x, start_y)])
    processed = set([(start_x, start_y)])

    while queue:
        x, y = queue.popleft()
        
        if color_distance(img1.pixelColor(x, y), target_color) <= tolerance and is_point_in_selection(x, y):
            img1.setPixelColor(x, y, fill_color)
            
            for nx, ny in [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]:
                if 0 <= nx < w and 0 <= ny < h and (nx, ny) not in processed:
                    processed.add((nx, ny))
                    queue.append((nx, ny))

# --- Selection Tools ---

def _finalize_selection(pixels: set, shape: str, bounds: QRect, edge_pixels: set | None = None):
    if not pixels:
        ie_globals.has_selection = False
        ie_globals.selection_region = None
        ie_globals.selection_type = None
        ie_globals.current_selection = set()
        ie_globals.selection_edge_pixels = set()
        ie_globals.selection_bounds = QRect()
        return

    ie_globals.current_selection = pixels
    ie_globals.selection_bounds = bounds
    ie_globals.selection_type = shape
    
    ie_globals.selection_edge_pixels = edge_pixels if edge_pixels is not None else set()
    
    region = QRegion()
    for x, y in pixels:
        region = region.united(QRect(x, y, 1, 1))
    ie_globals.selection_region = region
    
    ie_globals.has_selection = True
    ie_globals.selection_animation_active = True

def select_wand(img1: QImage, pt1: QPoint, task: str) -> None:
    if task != "down": return
    
    w, h = img1.width(), img1.height()
    start_x, start_y = pt1.x(), pt1.y()
    if not (0 <= start_x < w and 0 <= start_y < h): return

    target_color = img1.pixelColor(start_x, start_y)
    
    # Prevent freezing on transparent areas
    if target_color.alpha() == 0:
        print("Cannot select fully transparent area.")
        return

    tolerance = ie_globals.fill_tolerance 
    
    selected_pixels = set()
    edge_pixels = set()
    queue = deque([(start_x, start_y)])
    visited = set([(start_x, start_y)])

    while queue:
        x, y = queue.popleft()
        
        if color_distance(img1.pixelColor(x, y), target_color) <= tolerance:
            selected_pixels.add((x, y))
            is_edge = False
            for nx, ny in [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]:
                if not (0 <= nx < w and 0 <= ny < h and color_distance(img1.pixelColor(nx, ny), target_color) <= tolerance):
                    is_edge = True
                
                if 0 <= nx < w and 0 <= ny < h and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    queue.append((nx, ny))
            
            if is_edge:
                edge_pixels.add((x,y))

    _finalize_selection(selected_pixels, 'wand', find_selection_bounds(selected_pixels), edge_pixels=edge_pixels)

def select_rect(pt1: QPoint, pt2: QPoint, task: str):
    rect = QRect(pt1, pt2).normalized()
    
    if task == "move":
        ie_globals.selection_bounds = rect
        ie_globals.selection_type = 'rect'
        ie_globals.has_selection = True
        ie_globals.selection_animation_active = True
        ie_globals.selection_edge_pixels = set()
        ie_globals.current_selection = set()
        ie_globals.selection_region = None

    elif task == "release":
        pixels = set()
        for x in range(rect.left(), rect.right() + 1):
            for y in range(rect.top(), rect.bottom() + 1):
                pixels.add((x, y))
        _finalize_selection(pixels, 'rect', rect)

def select_circle(pt1: QPoint, pt2: QPoint, task: str):
    radius = math.hypot(pt1.x() - pt2.x(), pt1.y() - pt2.y())
    # Use floating point center for accuracy
    center_x, center_y = pt1.x(), pt1.y()
    
    # Bounding box for visualization and iteration
    rect = QRect(round(center_x - radius), round(center_y - radius), round(radius * 2), round(radius * 2))

    if task == "move":
        ie_globals.selection_bounds = rect
        ie_globals.selection_type = 'circle'
        ie_globals.has_selection = True
        ie_globals.selection_animation_active = True
        ie_globals.selection_edge_pixels = set()
        ie_globals.current_selection = set()
        ie_globals.selection_region = None

    elif task == "release":
        pixels = set()
        radius_sq = radius * radius
        
        # Iterate through the bounding box of the circle
        for x in range(rect.left(), rect.right() + 1):
            for y in range(rect.top(), rect.bottom() + 1):
                # Check if the integer pixel coordinate is within the circle's radius
                if (x - center_x)**2 + (y - center_y)**2 <= radius_sq:
                    pixels.add((x, y))
        
        _finalize_selection(pixels, 'circle', rect)


def find_selection_bounds(selected_pixels) -> QRect:
    if not selected_pixels: return QRect()
    min_x = min(x for x, y in selected_pixels)
    max_x = max(x for x, y in selected_pixels)
    min_y = min(y for x, y in selected_pixels)
    max_y = max(y for x, y in selected_pixels)
    return QRect(min_x, min_y, max_x - min_x + 1, max_y - min_y + 1)

def color_distance(c1: QColor, c2: QColor) -> float:
    return math.sqrt(
        (c1.red() - c2.red())**2 +
        (c1.green() - c2.green())**2 +
        (c1.blue() - c2.blue())**2 +
        (c1.alpha() - c2.alpha())**2
    )
