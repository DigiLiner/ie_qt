import math
import random
from collections import deque
from typing import Set,Tuple, Callable

from PySide6.QtGui import QImage, QPixmap, QPainter, QColor, QPen , QRadialGradient, QBrush, QPolygon
from PySide6.QtCore import QPoint, QRect, Qt
import ie_globals
import PySide6.QtCore

def is_point_in_selection(x: int, y: int) -> bool:
    """
    Checks if a given point (x, y) is within the currently active selection.

    Args:
        x (int): The x-coordinate of the point.
        y (int): The y-coordinate of the point.

    Returns:
        bool: True if the point is within the selection or if no selection is active, False otherwise.
    """
    if not ie_globals.has_selection or not ie_globals.current_selection:
        return True
    return (x, y) in ie_globals.current_selection

def draw_line(img1: QImage, pt1: QPoint, pt2: QPoint, task: str):
    """
    Draws a point or a line with a blur effect that scales with the pen_blur setting.

    Args:
        img1 (QImage): The QImage object to draw on.
        pt1 (QPoint): The starting point for drawing.
        pt2 (QPoint): The ending point for drawing (used for lines).
        task (str): The drawing task ("down" for a point, "move" for a line).
    """
    if task not in ["down", "move"]:
        return

    if not is_point_in_selection(pt1.x(), pt1.y()):
        return
    if task == "move" and not is_point_in_selection(pt2.x(), pt2.y()):
        return

    painter = QPainter(img1)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)

    base_color = ie_globals.current_pen.color()
    base_alpha = base_color.alpha()
    pen_width = ie_globals.current_pen.width()
    print("pen blur:", ie_globals.pen_blur)
    print("pen opacity:", base_alpha)
    if ie_globals.pen_blur > 0:
        # Blur radius and stroke count now scale with the pen_blur slider
        blur_radius = (pen_width * 0.1) + (ie_globals.pen_blur / 15.0)
        num_blur_strokes = int(5 + ie_globals.pen_blur / 10)

        for _ in range(num_blur_strokes):
            radius = random.uniform(0, blur_radius)
            angle = random.uniform(0, 2 * math.pi)
            offset_x = radius * math.cos(angle)
            offset_y = radius * math.sin(angle)
            
            normalized_distance = radius / blur_radius if blur_radius > 0 else 0
            # Alpha is now more sensitive to the slider value
            blur_alpha = int(base_alpha * (1 - normalized_distance))
            if blur_alpha < 0: blur_alpha = 0

            blurred_color = QColor(base_color.red(), base_color.green(), base_color.blue(), blur_alpha)
            
            blurred_pen = QPen(ie_globals.current_pen)
            blurred_pen.setColor(blurred_color)
            painter.setPen(blurred_pen)

            if task == "down":
                painter.drawPoint(QPoint(int(pt1.x() + offset_x), int(pt1.y() + offset_y)))
            elif task == "move":
                p1_offset = QPoint(int(pt1.x() + offset_x), int(pt1.y() + offset_y))
                p2_offset = QPoint(int(pt2.x() + offset_x), int(pt2.y() + offset_y))
                painter.drawLine(p1_offset, p2_offset)

    # Draw the main, solid stroke on top
    painter.setPen(ie_globals.current_pen)
    painter.setBrush(ie_globals.current_brush)
    if task == "down":
        painter.drawPoint(pt1)
    elif task == "move":
        painter.drawLine(pt1, pt2)

    painter.end()


def draw_brush(img: QImage, pos: QPoint, angle: float = 0.0):
    """
    Draws a brush stamp based on the current global settings.
    Acts as a dispatcher to different brush functions.
    """
    if ie_globals.brush_mode == "solid":
        if ie_globals.brush_shape == "circle":
            draw_circular_brush(img, pos, angle)
        elif ie_globals.brush_shape == "square":
            draw_square_brush(img, pos, angle)
        elif ie_globals.brush_shape == "star":
            draw_star_brush(img, pos, angle)
        elif ie_globals.brush_shape == "cylinder":
            draw_cylinder_brush(img, pos, angle)
    elif ie_globals.brush_mode == "image" and ie_globals.brush_image:
        draw_image_brush(img, pos, angle)
    elif ie_globals.brush_mode == "pattern" and ie_globals.pattern_image:
        draw_pattern_brush(img, pos)

def draw_circular_brush(img: QImage, pos: QPoint, angle: float = 0.0):
    """
    Draws a single circular brush stamp on the image at the given position.
    Handles size, hardness, and rotation.
    """
    painter = QPainter(img)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    
    size = ie_globals.brush_size
    hardness = ie_globals.brush_hardness / 100.0
    color = ie_globals.current_pen.color()
    
    painter.save()
    painter.translate(pos)
    painter.rotate(angle)
    
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

def draw_square_brush(img: QImage, pos: QPoint, angle: float = 0.0):
    """
    Draws a single square brush stamp on the image at the given position.
    Handles size, hardness, and rotation.
    """
    painter = QPainter(img)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    
    size = ie_globals.brush_size
    hardness = ie_globals.brush_hardness / 100.0
    color = ie_globals.current_pen.color()
    
    painter.save()
    painter.translate(pos)
    painter.rotate(angle)
    
    rect = QRect(-size // 2, -size // 2, size, size)
    
    if hardness >= 0.99:
        painter.setBrush(QBrush(color))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRect(rect)
    else:
        gradient = QRadialGradient(QPoint(0,0), size / 2)
        
        center_color = QColor(color)
        edge_color = QColor(color)
        edge_color.setAlpha(0)
        
        gradient.setColorAt(0, center_color)
        gradient.setColorAt(hardness, center_color)
        gradient.setColorAt(1.0, edge_color)
        
        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRect(rect)
        
    painter.restore()
    painter.end()

def draw_star_brush(img: QImage, pos: QPoint, angle: float = 0.0):
    """
    Draws a star-shaped brush stamp.
    """
    painter = QPainter(img)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    
    size = ie_globals.brush_size
    color = ie_globals.current_pen.color()
    num_points = 5 # Example: 5-pointed star
    
    painter.save()
    painter.translate(pos)
    painter.rotate(angle)
    
    polygon = QPolygon()
    for i in range(num_points * 2):
        radius = size // 2 if i % 2 == 0 else size // 4
        theta = i * (360 / (num_points * 2)) - 90
        point = QPoint(radius * math.cos(math.radians(theta)), radius * math.sin(math.radians(theta)))
        polygon.append(point)
        
    painter.setBrush(QBrush(color))
    painter.setPen(Qt.PenStyle.NoPen)
    painter.drawPolygon(polygon)
    
    painter.restore()
    painter.end()

def draw_cylinder_brush(img: QImage, pos: QPoint, angle: float = 0.0):
    """
    Draws a cylinder (ellipse) shaped brush stamp.
    """
    painter = QPainter(img)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    
    size = ie_globals.brush_size
    color = ie_globals.current_pen.color()
    
    painter.save()
    painter.translate(pos)
    painter.rotate(angle)
    
    # Make it an ellipse, for example, width is half of the height
    rect = QRect(-size // 4, -size // 2, size // 2, size)
    
    painter.setBrush(QBrush(color))
    painter.setPen(Qt.PenStyle.NoPen)
    painter.drawEllipse(rect)
    
    painter.restore()
    painter.end()


def draw_image_brush(img: QImage, pos: QPoint, angle: float = 0.0):
    """
    Draws an image as a brush stamp with rotation.
    """
    if not ie_globals.brush_image:
        return
        
    painter = QPainter(img)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    
    brush_img = ie_globals.brush_image
    size = ie_globals.brush_size
    
    scaled_brush_img = brush_img.scaled(size, size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
    
    painter.save()
    painter.translate(pos)
    painter.rotate(angle)
    
    top_left = QPoint(-scaled_brush_img.width() // 2, -scaled_brush_img.height() // 2)
    
    painter.drawImage(top_left, scaled_brush_img)
    painter.restore()
    painter.end()

def draw_pattern_brush(img: QImage, pos: QPoint):
    """
    Paints with a tiled pattern.
    """
    if not ie_globals.pattern_image:
        return
        
    painter = QPainter(img)
    
    size = ie_globals.brush_size
    
    # Create a brush from the pattern image
    pattern_brush = QBrush(ie_globals.pattern_image)
    painter.setBrush(pattern_brush)
    painter.setPen(Qt.PenStyle.NoPen)
    
    # Draw a shape (e.g., a circle or square) filled with the pattern
    if ie_globals.brush_shape == "circle":
        painter.drawEllipse(pos, size // 2, size // 2)
    elif ie_globals.brush_shape == "square":
        rect = QRect(pos.x() - size // 2, pos.y() - size // 2, size, size)
        painter.drawRect(rect)
        
    painter.end()


def draw_circle(img1: QImage,  pt1:QPoint, pt2:QPoint,task:str) -> None:
    """
    Draws a filled circle on the image with a high-quality, adjustable blur effect.

    Args:
        img1 (QImage): The QImage object to draw on.
        pt1 (QPoint): The center point of the circle.
        pt2 (QPoint): A point on the circumference of the circle, used to determine the radius.
        task (str): The drawing task. Only "move" is supported for continuous drawing.
    """
    if task != "move":
        return

    painter = QPainter(img1)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    
    radius = math.trunc(math.hypot(pt1.x() - pt2.x(), pt1.y() - pt2.y()))

    # If blur is 0, draw a simple, hard-edged circle
    if ie_globals.pen_blur == 0:
        painter.setPen(ie_globals.current_pen)
        painter.setBrush(ie_globals.current_brush)
        painter.drawEllipse(pt1, radius, radius)
        painter.end()
        return

    # --- Gradient-based Blur Logic ---
    
    # The color of the blur is based on the PEN color.
    blur_color = ie_globals.current_pen.color()
    
    # Create a transparent version of the color for the gradient edge
    transparent_color = QColor(blur_color)
    transparent_color.setAlpha(0)

    # The "hardness" of the edge is controlled by the pen_blur slider (0-100)
    hardness = 1.0 - (ie_globals.pen_blur / 100.0)

    # Create the radial gradient
    gradient = QRadialGradient(pt1, radius)
    
    # The gradient is solid up to the "hardness" point, then fades to transparent
    gradient.setColorAt(0, blur_color)
    gradient.setColorAt(hardness, blur_color)
    gradient.setColorAt(1.0, transparent_color)

    # Use the gradient as the brush
    gradient_brush = QBrush(gradient)
    
    painter.setBrush(gradient_brush)
    painter.setPen(QPen(QColor(0, 0, 0, 0)))  # Create an instance of QPen and set it to NoPen
    
    painter.drawEllipse(pt1, radius, radius)
    
    painter.end()

def draw_circle_outline(img1: QImage,  pt1:QPoint, pt2:QPoint,task:str) -> None:
    """
    Draws a hollow circle on the image with a high-quality, adjustable blur effect.

    Args:
        img1 (QImage): The QImage object to draw on.
        pt1 (QPoint): The center point of the circle.
        pt2 (QPoint): A point on the circumference of the circle, used to determine the radius.
        task (str): The drawing task. Only "move" is supported for continuous drawing.
    """
    if task != "move":
        return

    painter = QPainter(img1)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    
    radius = math.trunc(math.hypot(pt1.x() - pt2.x(), pt1.y() - pt2.y()))
    pen_width = ie_globals.current_pen.widthF()

    # If blur is 0, draw a simple, hard-edged outline
    if ie_globals.pen_blur == 0:
        painter.setPen(ie_globals.current_pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawEllipse(pt1, radius, radius)
        painter.end()
        return

    # --- Multi-draw Blur Logic for Outlines ---
    base_color = ie_globals.current_pen.color()
    base_alpha = base_color.alpha()
    
    # The blurriness scales with the pen_blur slider
    blur_amount = (pen_width / 2) + (ie_globals.pen_blur / 10.0)
    num_steps = int(5 + ie_globals.pen_blur / 5)

    for i in range(num_steps):
        # Each step is more transparent than the last
        t = i / float(num_steps)
        alpha = int(base_alpha * (1.0 - t) * 0.5) # Multiply by 0.5 to make it softer
        
        # The pen gets slightly wider with each step to create the blur
        current_width = pen_width + (t * blur_amount)
        
        color = QColor(base_color)
        color.setAlpha(alpha)
        
        pen = QPen(ie_globals.current_pen)
        pen.setColor(color)
        pen.setWidthF(current_width)
        
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        
        painter.drawEllipse(pt1, radius, radius)

    # Draw the main outline on top to keep it crisp
    painter.setPen(ie_globals.current_pen)
    painter.setBrush(Qt.BrushStyle.NoBrush)
    painter.drawEllipse(pt1, radius, radius)

    painter.end()


def draw_rect(img1: QImage,  pt1:QPoint, pt2:QPoint,task:str) -> None:
    """
    Draws a rectangle on the image.

    Args:
        img1 (QImage): The QImage object to draw on.
        pt1 (QPoint): The top-left corner of the rectangle.
        pt2 (QPoint): The bottom-right corner of the rectangle.
        task (str): The drawing task. Only "move" is supported for continuous drawing.
    """
    if task != "move":
        return

    painter = QPainter(img1)
    painter.setPen(ie_globals.current_pen)
    painter.setBrush(ie_globals.current_brush)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    rect = QRect(pt1,pt2)
    painter.drawRect(rect)
    painter.end()

def draw_round_rect(img1: QImage,  pt1:QPoint, pt2:QPoint,task:str,corner_radius:int=10) -> None:
    """
    Draws a rounded rectangle on the image.

    Args:
        img1 (QImage): The QImage object to draw on.
        pt1 (QPoint): The top-left corner of the rectangle.
        pt2 (QPoint): The bottom-right corner of the rectangle.
        task (str): The drawing task. Only "move" is supported for continuous drawing.
        corner_radius (int): The radius of the corners for the rounded rectangle.
    """
    if task != "move":
        return

    if not (is_point_in_selection(pt1.x(), pt1.y()) and 
            is_point_in_selection(pt2.x(), pt2.y())):
        return

    painter= QPainter(img1)
    painter.setPen(ie_globals.current_pen)
    painter.setBrush(ie_globals.current_brush)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    rect = QRect(pt1,pt2)
    painter.drawRoundedRect(rect,corner_radius,corner_radius)
    painter.end()

def draw_spray(img1: QImage, pt1:QPoint,task:str):
    """
    Draws a spray effect on the image.

    Args:
        img1 (QImage): The QImage object to draw on.
        pt1 (QPoint): The center point for the spray effect.
        task (str): The drawing task. Only "move" is supported for continuous spraying.
    """
    if task != "move":
        return

    painter = QPainter(img1)
    painter.setPen(ie_globals.current_pen)
    painter.setBrush(ie_globals.current_brush)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    for i in range(ie_globals.spray_density):
        x = int(pt1.x() + random.gauss(0, ie_globals.spray_radius))
        y = int(pt1.y() + random.gauss(0, ie_globals.spray_radius))
        if is_point_in_selection(x, y): #seçim kontrolü
            painter.drawPoint(x, y)

    painter.end()


def select_wand(img1: QImage, pt1: QPoint, task: str) -> None:
    """
    Performs an enhanced flood fill selection based on color similarity,
    similar to a magic wand tool.

    Args:
        img1 (QImage): The QImage object to perform the selection on.
        pt1 (QPoint): The starting point for the flood fill.
        task (str): The task to perform. Only "down" is supported to initiate selection.
    """
    if task != "down":
        return

    print("🎯 Seçim - Geliştirilmiş Flood Fill")
    
    target_color = img1.pixel(pt1.x(), pt1.y())
    start_x, start_y = pt1.x(), pt1.y()
    
    w, h = img1.width(), img1.height()
    
    # Başlangıç noktası geçerli mi?
    if not (0 <= start_x < w and 0 <= start_y < h):
        print("❌ Başlangıç noktası resim sınırları dışında")
        return
    
    visited = set()
    queue = deque()
    queue.append((start_x, start_y))
    visited.add((start_x, start_y))
    
    selected_pixels = set()
    edge_pixels = set()
    
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    
    while queue:
        x, y = queue.popleft()
        current_color = img1.pixel(x, y)
        
        # Sadece hedef renkteki pikselleri seç
        if current_color == target_color:
            selected_pixels.add((x, y))
            
            
            # Kenar kontrolü
            is_edge = False
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < w and 0 <= ny < h:
                    neighbor_color = img1.pixel(nx, ny)
                    if neighbor_color != target_color:
                        is_edge = True
                        break
                else:
                    is_edge = True
                    break
            
            if is_edge:
                edge_pixels.add((x, y))

        
            
            # Komşuları kuyruğa ekle
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < w and 0 <= ny < h and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    queue.append((nx, ny))
    
    # Seçim bilgilerini kaydet
    if selected_pixels:
        bounds = find_selection_bounds(selected_pixels)
        ie_globals.current_selection = selected_pixels
        ie_globals.selection_bounds = bounds
        ie_globals.selection_edge_pixels = edge_pixels
        ie_globals.has_selection = True
        ie_globals.selection_animation_active = True  # ANİMASYONU AKTİF ET
        
        print(f"✅ {len(selected_pixels)} piksel seçildi")
        print(f"📍 Tıklanan nokta: ({start_x}, {start_y})")
        print(f"📍 Seçim sınırları: {bounds}")
        
        center_x = bounds.x() + bounds.width() // 2
        center_y = bounds.y() + bounds.height() // 2
        print(f"📍 Seçim merkezi: ({center_x}, {center_y})")
        
    else:
        print("❌ Seçim bulunamadı")
        ie_globals.has_selection = False



def color_distance(color1, color2):
    """
    Calculates the Euclidean distance between two QColor objects in RGBA space.

    Args:
        color1 (QColor): The first color.
        color2 (QColor): The second color.

    Returns:
        float: The Euclidean distance between the two colors.
    """
    c1 = QColor(color1)
    c2 = QColor(color2)
    
    r_diff = c1.red() - c2.red()
    g_diff = c1.green() - c2.green()
    b_diff = c1.blue() - c2.blue()
    a_diff = c1.alpha() - c2.alpha()
    
    return math.sqrt(r_diff*r_diff + g_diff*g_diff + b_diff*b_diff + a_diff*a_diff)

def get_8_directions(have_seen, center_pos, w, h):
    """
    Returns the 8-directional neighbors of a center point that are within image bounds and not yet seen.

    Args:
        have_seen (Set[Tuple[int, int]]): A set of points that have already been processed.
        center_pos (Tuple[int, int]): A tuple representing the center position (x, y).
        w (int): Width of the image.
        h (int): Height of the image.

    Returns:
        List[Tuple[int, int]]: A list of 8-directional neighbor points that are within bounds and not seen.
    """
    points = []
    cx, cy = center_pos
    
    directions = [(1,0), (1,1), (0,1), (-1,1), (-1,0), (-1,-1), (0,-1), (1,-1)]
    

    for dx, dy in directions:
        xx, yy = cx + dx, dy + dy
        
        if 0 <= xx < w and 0 <= yy < h and (xx, yy) not in have_seen:
            points.append((xx, yy))
            have_seen.add((xx, yy))
    
    return points
def find_selection_bounds(selected_pixels) -> QRect:
    """
    Calculates the bounding rectangle for a given set of selected pixels.

    Args:
        selected_pixels (Set[Tuple[int, int]]): A set of (x, y) pixel coordinates.

    Returns:
        QRect: A QRect object representing the smallest rectangle that encloses all selected pixels.
               Returns an empty QRect if `selected_pixels` is empty.
    """
    if not selected_pixels:
        return QRect()
    
    min_x = min(x for x, y in selected_pixels)
    max_x = max(x for x, y in selected_pixels)
    min_y = min(y for x, y in selected_pixels)
    max_y = max(y for x, y in selected_pixels)
    
    bounds = PySide6.QtCore.QRect(min_x, min_y, max_x - min_x + 1, max_y - min_y + 1)
    
    return bounds
def fill(img1: QImage, pt1: QPoint, task: str,tolerance:float) -> None:
    """
    Fills an area of the image starting from the point `pt1` with the specified `task`.
    Currently supports the "down" task which uses flood fill algorithm to fill connected pixels
    of similar color.

    Args:
        img1 (QImage): The image to be filled.
        pt1 (QPoint): The starting point for the fill operation.
        task (str): The task to perform, currently only "down" is supported.
        tolerance (float): The color tolerance for the fill operation, ranging from 0.0 to 1.0.
                           A higher tolerance allows filling of colors that are less similar to the target color.
    """
    if task != "down":
        return

    painter = QPainter(img1)
    print("Fill")

    # Global pen'i değiştirmemek için kopyasını oluştur
    temp_pen = QPen(ie_globals.current_pen) 
    temp_pen.setWidth(1)  # Doldurma için her zaman 1px kullanılır
    painter.setPen(temp_pen)

    # set the brush of the painter
    painter.setBrush(ie_globals.current_brush)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    
    target_color = QColor(img1.pixelColor(pt1.x(), pt1.y()))
    x, y = int(pt1.x()), int(pt1.y())
    
    have_seen: Set[Tuple[int, int]] = set()
    queue = deque([(x, y)])
    w = img1.width()
    h = img1.height()
    
    tolerance = ie_globals.fill_tolerance
    r2, g2, b2, a2 = target_color.red(), target_color.green(), target_color.blue(), target_color.alpha()

    while queue:
        x, y = queue.popleft()
        color1 = QColor(img1.pixelColor(x, y))
        
        is_match = False
        if tolerance == 0:
            if color1 == target_color:
                is_match = True
        else:
            r1, g1, b1, a1 = color1.red(), color1.green(), color1.blue(), color1.alpha()
            if (abs(r1 - r2) <= tolerance) and (abs(g1 - g2) <= tolerance) and \
                (abs(b1 - b2) <= tolerance) and (abs(a1 - a2) <= tolerance):
                is_match = True
        
        if is_match:
            if is_point_in_selection(x, y):
                painter.drawPoint(x, y)
            queue.extend(get_cardinal_points(have_seen, (x, y), w, h))

    painter.end()

def get_cardinal_points(have_seen, center_pos, w, h):
    """
    Returns the cardinal points (up, down, left, right) around the center position
    that are within the image bounds and not yet seen.

    Args:
        have_seen (Set[Tuple[int, int]]): A set of points that have already been processed.
        center_pos (Tuple[int, int]): A tuple representing the center position (x, y).
        w (int): Width of the image.
        h (int): Height of the image.

    Returns:
        List[Tuple[int, int]]: A list of cardinal points that are within bounds and not seen.
    """
    try:
        points = []
        cx, cy = center_pos

        cardinal_directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]

        for x, y in cardinal_directions:
            xx, yy = cx + x, cy + y

            # Check if the point is within the image bounds and not in have_seen
            if 0 <= xx < w and 0 <= yy < h and (xx, yy) not in have_seen:
                points.append((xx, yy))
                have_seen.add((xx, yy))

        return points

    except Exception as e:
        print(f"An error occurred in get_cardinal_points: {e}")
        return []



def erase(img1: QImage, pt1: QPoint, task: str) -> bool | None:
    """
    Erases parts of the image using the current pen settings.

    Args:
        img1 (QImage): The QImage object to erase from.
        pt1 (QPoint): The current point of the eraser.
        task (str): The erasing task ("down" for initial point, "move" for continuous erasing).

    Returns:
        bool | None: True if erasing occurred, None otherwise.
    """
    if task not in ["down", "move"]:
        return

    painter = QPainter(img1)
    painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_Clear)
    

    eraser_pen = QPen()
    eraser_pen.setWidth(ie_globals.current_pen.width())
    eraser_pen.setCapStyle(PySide6.QtCore.Qt.PenCapStyle.RoundCap)
    
    if task == "down":
        painter.setPen(eraser_pen)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.drawPoint(pt1.x(), pt1.y())
        erase.last_pos = pt1
    elif task == "move":
        if hasattr(erase, 'last_pos'):
            eraser_pen.setJoinStyle(PySide6.QtCore.Qt.PenJoinStyle.RoundJoin)
            painter.setPen(eraser_pen)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            painter.drawLine(erase.last_pos, pt1)
            erase.last_pos = pt1
    
    painter.end()
    return True
def erase_soft(img1: QImage, pt1: QPoint, task: str) -> bool | None:
    """
    Performs a soft erase effect using a radial gradient brush.

    Args:
        img1 (QImage): The QImage object to erase from.
        pt1 (QPoint): The center point of the soft eraser.
        task (str): The erasing task ("down" or "move").

    Returns:
        bool | None: True if erasing occurred, None otherwise.
    """
    if task not in ["down", "move"]:
        return None

    painter = QPainter(img1)
    painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_DestinationOut)
    
    gradient = QRadialGradient(pt1.x(), pt1.y(), ie_globals.current_pen.width() // 2)
    gradient.setColorAt(0.0, QColor(0, 0, 0, 255))
    gradient.setColorAt(0.7, QColor(0, 0, 0, 128))
    gradient.setColorAt(1.0, QColor(0, 0, 0, 0))
    
    soft_brush = QBrush(gradient)
    painter.setBrush(soft_brush)
    painter.setPen(PySide6.QtCore.Qt.PenStyle.NoPen)
    
    radius = ie_globals.current_pen.width() // 2
    painter.drawEllipse(pt1.x() - radius, pt1.y() - radius, radius * 2, radius * 2)
    painter.end()
    
    return True
## Realistic eraser with pressure and hardness control
def erase_real(img1: QImage, pt1: QPoint, task: str, pressure: float = 1.0, hardness: float = 0.5) -> bool | None:
    """
    Performs a realistic erase effect with pressure and hardness control.

    Args:
        img1 (QImage): The QImage object to erase from.
        pt1 (QPoint): The current point of the eraser.
        task (str): The erasing task ("down" or "move").
        pressure (float): The pressure applied to the eraser (0.0-1.0), affecting its size.
        hardness (float): The hardness of the eraser (0.0-1.0), affecting the edge softness.

    Returns:
        bool | None: True if erasing occurred, None otherwise.
    """
    if task not in ["down", "move"]:
        return None

    painter = QPainter(img1)
    painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_DestinationOut)
    
    base_radius = ie_globals.current_pen.width() // 2
    actual_radius = int(base_radius * pressure)  # Basınca göre boyut
    
    if hardness > 0.8:
        # Sert silgi - düz daire
        solid_brush = QBrush(QColor(0, 0, 0, 200))
        painter.setBrush(solid_brush)
        painter.setPen(PySide6.QtCore.Qt.PenStyle.NoPen)
        painter.drawEllipse(pt1.x() - actual_radius, pt1.y() - actual_radius, 
                           actual_radius * 2, actual_radius * 2)
    
    else:
        # Yumuşak silgi - gradient
        gradient = QRadialGradient(pt1.x(), pt1.y(), actual_radius)
        
        # Hardness'a göre gradient ayarla
        inner_radius = actual_radius * hardness
        gradient.setColorAt(0.0,QColor(0, 0, 0, 200))
        gradient.setColorAt(inner_radius/actual_radius, QColor(0, 0, 0, 100))
        gradient.setColorAt(1.0, QColor(0, 0, 0, 0))
        
        soft_brush = QBrush(gradient)
        painter.setBrush(soft_brush)
        painter.setPen(PySide6.QtCore.Qt.PenStyle.NoPen)
        painter.drawEllipse(pt1.x() - actual_radius, pt1.y() - actual_radius, 
                           actual_radius * 2, actual_radius * 2)
    
    painter.end()
    return True
