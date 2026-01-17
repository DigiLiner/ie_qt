# This file contains global variables used by the image editor.
import PySide6
import PySide6.QtGui
import PySide6.QtCore
import PySide6.QtWidgets
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt, QSettings
from PySide6.QtGui import QPen, QColor, QBrush, QImage, QPainter, QMouseEvent, QPixmap
import main_ui as iemain
import main_ui as main_ui

class ie_tool:
    def __init__(self, name:str, icon:str, tool_id:int, shortcut:str="", description:str="", finished:bool=False):
        
    
        self.name = name
        self.icon = icon
        self.tool_id = tool_id
        self.shortcut = shortcut
        self.description = ""
        self.finished = False # developer tag


ie_tool_pen = ie_tool("Pen", "svgicons/pen-gray.svg", 1000, "P", "Pen Tool",True)
'''
Represents the Pen tool in the image editor.
- `name`: "Pen" - Display name of the tool.
- `icon`: "svgicons/pen-gray.svg" - Path to the tool's SVG icon.
- `tool_id`: 1000 - Unique identifier for the tool.
- `shortcut`: "P" - Keyboard shortcut for activating the tool.
- `description`: "Pen Tool" - A brief description of the tool's function.
- `finished`: True - Indicates if the tool's implementation is complete.
'''
ie_tool_brush = ie_tool("Brush", "svgicons/brush.svg", 1001, "B", "Brush Tool",False)
'''
Represents the Brush tool in the image editor.
- `name`: "Brush" - Display name of the tool.
- `icon`: "svgicons/brush.svg" - Path to the tool's SVG icon.
- `tool_id`: 1001 - Unique identifier for the tool.
- `shortcut`: "B" - Keyboard shortcut for activating the tool.
- `description`: "Brush Tool" - A brief description of the tool's function.
- `finished`: False - Indicates if the tool's implementation is complete.
'''
ie_tool_line = ie_tool("Line", "svgicons/line-gray.svg", 1002, "L", "Line Tool",True)
'''
Represents the Line tool in the image editor.
- `name`: "Line" - Display name of the tool.
- `icon`: "svgicons/line-gray.svg" - Path to the tool's SVG icon.
- `tool_id`: 1002 - Unique identifier for the tool.
- `shortcut`: "L" - Keyboard shortcut for activating the tool.
- `description`: "Line Tool" - A brief description of the tool's function.
- `finished`: True - Indicates if the tool's implementation is complete.
'''
ie_tool_rect = ie_tool("Rectangle", "svgicons/rectangle.svg", 1003, "R", "Rectangle Tool",True)
'''
Represents the Rectangle tool in the image editor.
- `name`: "Rectangle" - Display name of the tool.
- `icon`: "svgicons/rectangle.svg" - Path to the tool's SVG icon.
- `tool_id`: 1003 - Unique identifier for the tool.
- `shortcut`: "R" - Keyboard shortcut for activating the tool.
- `description`: "Rectangle Tool" - A brief description of the tool's function.
- `finished`: True - Indicates if the tool's implementation is complete.
'''
ie_tool_circle = ie_tool("Circle", "svgicons/circle-gray.svg", 1004, "C", "Circle Tool",True)
'''
Represents the Circle tool in the image editor.
- `name`: "Circle" - Display name of the tool.
- `icon`: "svgicons/circle-gray.svg" - Path to the tool's SVG icon.
- `tool_id`: 1004 - Unique identifier for the tool.
- `shortcut`: "C" - Keyboard shortcut for activating the tool.
- `description`: "Circle Tool" - A brief description of the tool's function.
- `finished`: True - Indicates if the tool's implementation is complete.
'''
ie_tool_spray = ie_tool("Spray", "svgicons/spray-gray.svg", 1005, "S", "Spray Tool",True)
'''
Represents the Spray tool in the image editor.
- `name`: "Spray" - Display name of the tool.
- `icon`: "svgicons/spray-gray.svg" - Path to the tool's SVG icon.
- `tool_id`: 1005 - Unique identifier for the tool.
- `shortcut`: "S" - Keyboard shortcut for activating the tool.
- `description`: "Spray Tool" - A brief description of the tool's function.
- `finished`: True - Indicates if the tool's implementation is complete.
'''
ie_tool_fill = ie_tool("Fill", "svgicons/fill.svg", 1006, "F", "Fill Tool",True)
'''
Represents the Fill tool in the image editor.
- `name`: "Fill" - Display name of the tool.
- `icon`: "svgicons/fill.svg" - Path to the tool's SVG icon.
- `tool_id`: 1006 - Unique identifier for the tool.
- `shortcut`: "F" - Keyboard shortcut for activating the tool.
- `description`: "Fill Tool" - A brief description of the tool's function.
- `finished`: True - Indicates if the tool's implementation is complete.
'''
ie_tool_text = ie_tool("Text", "svgicons/text.svg", 1007, "T", "Text Tool",False)
'''
Represents the Text tool in the image editor.
- `name`: "Text" - Display name of the tool.
- `icon`: "svgicons/text.svg" - Path to the tool's SVG icon.
- `tool_id`: 1007 - Unique identifier for the tool.
- `shortcut`: "T" - Keyboard shortcut for activating the tool.
- `description`: "Text Tool" - A brief description of the tool's function.
- `finished`: False - Indicates if the tool's implementation is complete.
'''
ie_tool_eraser = ie_tool("Eraser", "svgicons/eraser-gray.svg", 1008, "E", "Eraser Tool",False)
'''
Represents the Eraser tool in the image editor.
- `name`: "Eraser" - Display name of the tool.
- `icon`: "svgicons/eraser-gray.svg" - Path to the tool's SVG icon.
- `tool_id`: 1008 - Unique identifier for the tool.
- `shortcut`: "E" - Keyboard shortcut for activating the tool.
- `description`: "Eraser Tool" - A brief description of the tool's function.
- `finished`: False - Indicates if the tool's implementation is complete.
'''
ie_tool_pan = ie_tool("Pan", "svgicons/pan-gray.svg", 1010, "P", "Pan Tool",False)
'''
Represents the Pan tool in the image editor.
- `name`: "Pan" - Display name of the tool.
- `icon`: "svgicons/pan-gray.svg" - Path to the tool's SVG icon.
- `tool_id`: 1010 - Unique identifier for the tool.
- `shortcut`: "P" - Keyboard shortcut for activating the tool.
- `description`: "Pan Tool" - A brief description of the tool's function.
- `finished`: False - Indicates if the tool's implementation is complete.
'''
ie_tool_dropper = ie_tool("Dropper", "svgicons/dropper.svg", 1011, "D", "Dropper Tool",True)
'''
Represents the Dropper tool (color picker) in the image editor.
- `name`: "Dropper" - Display name of the tool.
- `icon`: "svgicons/dropper.svg" - Path to the tool's SVG icon.
- `tool_id`: 1011 - Unique identifier for the tool.
- `shortcut`: "D" - Keyboard shortcut for activating the tool.
- `description`: "Dropper Tool" - A brief description of the tool's function.
- `finished`: True - Indicates if the tool's implementation is complete.
'''
ie_tool_rounded_rect = ie_tool("Rounded Rectangle", "svgicons/rounded-rectangle.svg", 1012, "O","Rounded Rectangle Tool",True)
'''
Represents the Rounded Rectangle tool in the image editor.
- `name`: "Rounded Rectangle" - Display name of the tool.
- `icon`: "svgicons/rounded-rectangle.svg" - Path to the tool's SVG icon.
- `tool_id`: 1012 - Unique identifier for the tool.
- `shortcut`: "O" - Keyboard shortcut for activating the tool.
- `description`: "Rounded Rectangle Tool" - A brief description of the tool's function.
- `finished`: True - Indicates if the tool's implementation is complete.
'''
ie_tool_ellipse = ie_tool("Ellipse", "svgicons/ellipse-gray.svg", 1013, "L", "Ellipse Tool",True)
'''
Represents the Ellipse tool in the image editor.
- `name`: "Ellipse" - Display name of the tool.
- `icon`: "svgicons/ellipse-gray.svg" - Path to the tool's SVG icon.
- `tool_id`: 1013 - Unique identifier for the tool.
- `shortcut`: "L" - Keyboard shortcut for activating the tool.
- `description`: "Ellipse Tool" - A brief description of the tool's function.
- `finished`: True - Indicates if the tool's implementation is complete.
'''
ie_tool_wand = ie_tool("Wand", "svgicons/wand.svg", 1014, "W", "Wand Tool",False)
'''
Represents the Magic Wand tool in the image editor.
- `name`: "Wand" - Display name of the tool.
- `icon`: "svgicons/wand.svg" - Path to the tool's SVG icon.
- `tool_id`: 1014 - Unique identifier for the tool.
- `shortcut`: "W" - Keyboard shortcut for activating the tool.
- `description`: "Wand Tool" - A brief description of the tool's function.
- `finished`: False - Indicates if the tool's implementation is complete.
'''
ie_tool_polygon = ie_tool("Polygon", "svgicons/polygon-gray.svg", 1015, "G","Polygon Tool",False)
'''
Represents the Polygon tool in the image editor.
- `name`: "Polygon" - Display name of the tool.
- `icon`: "svgicons/polygon-gray.svg" - Path to the tool's SVG icon.
- `tool_id`: 1015 - Unique identifier for the tool.
- `shortcut`: "G" - Keyboard shortcut for activating the tool.
- `description`: "Polygon Tool" - A brief description of the tool's function.
- `finished`: False - Indicates if the tool's implementation is complete.
'''
ie_tool_bezier = ie_tool("Bezier", "svgicons/bezier-gray.svg", 1016, "B", "Bezier Tool",False)
'''
Represents the Bezier tool in the image editor.
- `name`: "Bezier" - Display name of the tool.
- `icon`: "svgicons/bezier-gray.svg" - Path to the tool's SVG icon.
- `tool_id`: 1016 - Unique identifier for the tool.
- `shortcut`: "B" - Keyboard shortcut for activating the tool.
- `description`: "Bezier Tool" - A brief description of the tool's function.
- `finished`: False - Indicates if the tool's implementation is complete.
'''
ie_tool_select_rect = ie_tool("Select Rectangle", "svgicons/select-rectangle-gray.svg", 1017, "S","Select Rectangle Tool",False)
'''
Represents the Rectangle Selection tool in the image editor.
- `name`: "Select Rectangle" - Display name of the tool.
- `icon`: "svgicons/select-rectangle-gray.svg" - Path to the tool's SVG icon.
- `tool_id`: 1017 - Unique identifier for the tool.
- `shortcut`: "S" - Keyboard shortcut for activating the tool.
- `description`: "Select Rectangle Tool" - A brief description of the tool's function.
- `finished`: False - Indicates if the tool's implementation is complete.
'''
ie_tool_select_circle = ie_tool("Select Circle", "svgicons/select-circle-gray.svg", 1018, "S","Select Circle Tool",False)
'''
Represents the Circle Selection tool in the image editor.
- `name`: "Select Circle" - Display name of the tool.
- `icon`: "svgicons/select-circle-gray.svg" - Path to the tool's SVG icon.
- `tool_id`: 1018 - Unique identifier for the tool.
- `shortcut`: "S" - Keyboard shortcut for activating the tool.
- `description`: "Select Circle Tool" - A brief description of the tool's function.
- `finished`: False - Indicates if the tool's implementation is complete.
'''
ie_tool_select_polygon = ie_tool("Select Polygon", "svgicons/select-polygon.svg", 1019, "S","Select Polygon Tool",False)
'''
Represents the Polygon Selection tool in the image editor.
- `name`: "Select Polygon" - Display name of the tool.
- `icon`: "svgicons/select-polygon.svg" - Path to the tool's SVG icon.
- `tool_id`: 1019 - Unique identifier for the tool.
- `shortcut`: "S" - Keyboard shortcut for activating the tool.
- `description`: "Select Polygon Tool" - A brief description of the tool's function.
- `finished`: False - Indicates if the tool's implementation is complete.
'''
ie_tool_select_lasso = ie_tool("Select Lasso", "svgicons/lasso_select.svg", 1020, "S","Select Lasso Tool",False)
'''
Represents the Lasso Selection tool in the image editor.
- `name`: "Select Lasso" - Display name of the tool.
- `icon`: "svgicons/lasso_select.svg" - Path to the tool's SVG icon.
- `tool_id`: 1020 - Unique identifier for the tool.
- `shortcut`: "S" - Keyboard shortcut for activating the tool.
- `description`: "Select Lasso Tool" - A brief description of the tool's function.
- `finished`: False - Indicates if the tool's implementation is complete.
'''
ie_tool_select_path = ie_tool("Select Path", "svgicons/select-path.svg", 1021, "S","Select Path Tool",False)
'''
Represents the Path Selection tool in the image editor.
- `name`: "Select Path" - Display name of the tool.
- `icon`: "svgicons/select-path.svg" - Path to the tool's SVG icon.
- `tool_id`: 1021 - Unique identifier for the tool.
- `shortcut`: "S" - Keyboard shortcut for activating the tool.
- `description`: "Select Path Tool" - A brief description of the tool's function.
- `finished`: False - Indicates if the tool's implementation is complete.
'''
ie_tool_crop = ie_tool("Crop", "svgicons/crop.svg", 1022, "C", "Crop Tool",False)
'''
Represents the Crop tool in the image editor.
- `name`: "Crop" - Display name of the tool.
- `icon`: "svgicons/crop.svg" - Path to the tool's SVG icon.
- `tool_id`: 1022 - Unique identifier for the tool.
- `shortcut`: "C" - Keyboard shortcut for activating the tool.
- `description`: "Crop Tool" - A brief description of the tool's function.
- `finished`: False - Indicates if the tool's implementation is complete.
'''

ie_tool_circle_outline= ie_tool ("Circle Outline", "svgicons/circle-outline-gray.svg",1023,"C","Circle Outline Tool",False)
'''
Represents the Circle Outline tool in the image editor.
- `name`: "Circle Outline" - Display name of the tool.
- `icon`: "svgicons/circle-outline-gray.svg" - Path to the tool's SVG icon.
- `tool_id`: 1023 - Unique identifier for the tool.
- `shortcut`: "C" - Keyboard shortcut for activating the tool.
- `description`: "Circle Outline Tool" - A brief description of the tool's function.
- `finished`: False - Indicates if the tool's implementation is complete.
'''

tools = [
    ie_tool_pen,
    ie_tool_brush,
    ie_tool_line, 
    ie_tool_rect, 
    ie_tool_circle, 
    ie_tool_spray,
    ie_tool_fill, 
    ie_tool_text, 
    ie_tool_eraser, 
    ie_tool_pan, 
    ie_tool_dropper,
    ie_tool_rounded_rect,
    ie_tool_ellipse,
    ie_tool_wand,
    ie_tool_polygon,
    ie_tool_bezier,
    ie_tool_select_rect,
    ie_tool_select_circle,
    ie_tool_select_polygon,
    ie_tool_select_lasso,
    ie_tool_select_path,
    ie_tool_crop

]
'''
A list containing all defined `ie_tool` instances.
This list serves as a registry of all available tools in the image editor,
allowing for easy iteration and management of tools.
'''


# Default pen and brush
current_pen :PySide6.QtGui.QPen = PySide6.QtGui.QPen()
'''
The currently active QPen object for drawing operations.
'''
current_brush:PySide6.QtGui.QBrush = PySide6.QtGui.QBrush()
'''
The currently active QBrush object for filling shapes.
'''
current_pen.setColor (QColor(0,0,0))

current_pen.color().setAlpha(1)

pen_blur: int = 1
'''
The blur radius for the pen.
'''

current_pen.setStyle(Qt.PenStyle.SolidLine)
current_pen.setCapStyle (Qt.PenCapStyle.RoundCap)
current_pen.setJoinStyle (Qt.PenJoinStyle.RoundJoin)
current_pen.setCosmetic(True)

current_brush.setColor(PySide6.QtGui.QColor(QColor(255,255,255,0)))
current_brush.setStyle(PySide6.QtCore.Qt.BrushStyle.NoBrush)
current_brush.setStyle(PySide6.QtCore.Qt.BrushStyle.TexturePattern)

current_tool:ie_tool = ie_tool_pen
'''
The currently selected drawing tool.
'''
previous_tool:ie_tool = ie_tool_pen
'''
The previously selected drawing tool.
'''

brush_color = "blue"
brush_blur:int = 2
spray_radius = 50
spray_density = 100

zoomInFactor:float = 1.25
zoomOutFactor:float= 1/1.25

image_width:int =1000
image_height:int = 800
image_bg_color = "white"
zooming:bool = False
tool_icon_size = "24px"
filenamecounter = 1

fill_tolerance:float = 1.0

max_undo_steps = 20

# Selection globals
current_selection: set = set()
selection_bounds: PySide6.QtCore.QRect = PySide6.QtCore.QRect()
selection_edge_pixels: set = set()
has_selection: bool = False
selection_colors = [
    QColor(0, 100, 255, 220), QColor(255, 100, 0, 220),
    QColor(0, 200, 100, 220), QColor(200, 0, 255, 220)
]
current_selection_color_index = 0
selection_animation_timer = None
selection_animation_active = False
selection_animation_speed = 500

round_rect_corner_radius = 10

class StatusText:
    def __init__(self, tool, pos, zoom):
        self.tool = tool
        self.pos = pos
        self.zoom = zoom

statusText = StatusText("Tool:", "Pos:", "Zoom:")

class Layer:
    def __init__(self, name:str, visible:bool=True, opacity:int=100, image:PySide6.QtGui.QImage= QImage(image_width, image_height, PySide6.QtGui.QImage.Format.Format_RGBA64), rasterized:bool=True,locked:bool=False):
        self.name = name
        self.active=False
        self.visible = visible
        self.opacity = opacity
        self.image = image
        self.rasterized = rasterized
        self.locked = locked
        self.id=0

# Filter settings
shear_amount = 40
shear_horizontal = True
shear_direction = 1
melt_amount = 30
blur_radius = 3
mosaic_block_size = 10

# Brush settings
brush_size = 30
brush_hardness = 80
brush_density = 100
brush_shape = "circle"
brush_mode = "solid"
brush_image: QImage | None = None
pattern_image: QImage | None = None
brush_dynamic_angle = False
brush_star_points = 5
brush_cylinder_ratio = 0.5

current_pen.setWidth(brush_size)

def save_settings():
    settings = QSettings("ie_settings.ini", QSettings.Format.IniFormat)
    settings.setValue("brush_size", brush_size)
    settings.setValue("brush_hardness", brush_hardness)
    settings.setValue("brush_density", brush_density)
    settings.setValue("brush_shape", brush_shape)
    settings.setValue("brush_mode", brush_mode)
    settings.setValue("brush_dynamic_angle", brush_dynamic_angle)
    settings.setValue("brush_star_points", brush_star_points)
    settings.setValue("brush_cylinder_ratio", brush_cylinder_ratio)
    settings.setValue("pen_blur", pen_blur)
    settings.setValue("spray_radius", spray_radius)
    settings.setValue("spray_density", spray_density)
    settings.setValue("fill_tolerance", fill_tolerance)
    settings.setValue("round_rect_corner_radius", round_rect_corner_radius)
    settings.setValue("shear_amount", shear_amount)
    settings.setValue("shear_horizontal", shear_horizontal)
    settings.setValue("shear_direction", shear_direction)
    settings.setValue("melt_amount", melt_amount)
    settings.setValue("blur_radius", blur_radius)
    settings.setValue("mosaic_block_size", mosaic_block_size)

def _to_int(value, default: int) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default

def _to_float(value, default: float) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default

def _to_bool(value, default: bool) -> bool:
    if isinstance(value, bool):
        return value
    s = str(value).strip().lower()
    if s in {"1", "true", "yes", "on"}:
        return True
    if s in {"0", "false", "no", "off"}:
        return False
    return default

def load_settings():
    global brush_size, brush_hardness, brush_density, brush_shape, brush_mode, brush_dynamic_angle, brush_star_points, brush_cylinder_ratio, pen_blur, spray_radius, spray_density, fill_tolerance, round_rect_corner_radius, shear_amount, shear_horizontal, shear_direction, melt_amount, blur_radius, mosaic_block_size
    settings = QSettings("ie_settings.ini", QSettings.Format.IniFormat)
    brush_size = _to_int(settings.value("brush_size", 30), 30)
    brush_hardness = _to_int(settings.value("brush_hardness", 80), 80)
    brush_density = _to_int(settings.value("brush_density", 100), 100)
    brush_shape = settings.value("brush_shape", "circle")
    brush_mode = settings.value("brush_mode", "solid")
    brush_dynamic_angle = _to_bool(settings.value("brush_dynamic_angle", False), False)
    brush_star_points = _to_int(settings.value("brush_star_points", 5), 5)
    brush_cylinder_ratio = _to_float(settings.value("brush_cylinder_ratio", 0.5), 0.5)
    pen_blur = _to_int(settings.value("pen_blur", 1), 1)
    spray_radius = _to_int(settings.value("spray_radius", 50), 50)
    spray_density = _to_int(settings.value("spray_density", 100), 100)
    fill_tolerance = _to_float(settings.value("fill_tolerance", 1.0), 1.0)
    round_rect_corner_radius = _to_int(settings.value("round_rect_corner_radius", 10), 10)
    shear_amount = _to_int(settings.value("shear_amount", 40), 40)
    shear_horizontal = _to_bool(settings.value("shear_horizontal", True), True)
    shear_direction = _to_int(settings.value("shear_direction", 1), 1)
    melt_amount = _to_int(settings.value("melt_amount", 30), 30)
    blur_radius = _to_int(settings.value("blur_radius", 3), 3)
    mosaic_block_size = _to_int(settings.value("mosaic_block_size", 10), 10)
    current_pen.setWidth(brush_size)
