# This file contains global variables used by the image editor.
import PySide6
import PySide6.QtGui
import PySide6.QtCore
import PySide6.QtWidgets
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt
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

ie_tool_circle_outline= ie_tool ("Circle Outline",1023,"C","Circle Outline Tool",False)

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
The currently active QPen object used for drawing operations.
Its properties (color, width, style, etc.) are dynamically set
through the application's UI, such as color boxes and property sliders.
'''
current_brush:PySide6.QtGui.QBrush = PySide6.QtGui.QBrush()
'''
The currently active QBrush object used for filling shapes and areas.
Its properties are dynamically set through the application's UI.
'''
current_pen.setColor (QColor(0,0,0))
'''
The current color of the pen, represented as a QColor object.
Initialized to black (RGB: 0,0,0).
'''
current_pen.setWidth(15)
'''
The current width of the pen stroke in pixels.
'''
current_pen.color().setAlpha(1)
'''
The opacity of the pen, ranging from 0 (fully transparent) to 1 (fully opaque).
'''

#todo blur
pen_blur: int = 1
'''
The blur radius applied to the pen stroke.
'''

current_pen.setStyle(Qt.PenStyle.SolidLine)
'''
The style of the pen line, e.g., "solid", "dashed", "dotted".
'''
current_pen.setCapStyle (Qt.PenCapStyle.RoundCap)
'''
The style of the pen cap, e.g., "round", "square", "flat".
'''
current_pen.setJoinStyle (Qt.PenJoinStyle.RoundJoin)
'''
The style of the pen join, e.g., "round", "bevel", "miter".
'''

current_pen.setCosmetic(True)

current_brush.setColor(PySide6.QtGui.QColor(QColor(255,255,255,0)))
current_brush.setStyle(PySide6.QtCore.Qt.BrushStyle.NoBrush)
current_brush.setStyle(PySide6.QtCore.Qt.BrushStyle.TexturePattern)

# Pen and Brush properties set glabally in mainwindow
# with using colorbox and property sliders

#todo app wide options only
#current tool for drawing string= line, circle, rect, pen, brush, spray, fill
current_tool:ie_tool = ie_tool_pen
'''
The currently selected drawing tool, represented by an `ie_tool` object.
This variable dictates which drawing or editing action is active.
'''
previous_tool:ie_tool = ie_tool_pen
'''
Stores the previously selected drawing tool, represented by an `ie_tool` object.
Useful for quickly switching back to the last used tool.
'''




#color of brush
brush_color = "blue"
'''
The current color of the brush, represented as a string (e.g., "blue").
'''
brush_blur:int = 2
'''
The blur radius applied to the brush stroke.
'''
spray_radius = 50
'''
The radius of the circle for the spray tool, defining the area of effect.
'''
spray_density = 100
'''
The density of the spray tool, controlling how many "spray" particles are applied within the radius.
'''

#Zoom factor for zoom in/ou
zoomInFactor:float = 1.25
'''
The factor by which the canvas zoom level increases during a zoom-in operation.
'''
zoomOutFactor:float= 1/1.25
'''
The factor by which the canvas zoom level decreases during a zoom-out operation.
Calculated as the inverse of `zoomInFactor`.
'''

#Image width of original canvas
image_width:int =1000
'''
The default width of the image canvas in pixels.
'''
image_height:int = 800
'''
The default height of the image canvas in pixels.
'''
image_bg_color = "white"
'''
The default background color of the image canvas.
'''
zooming:bool = False
'''
A boolean flag indicating whether a zoom operation is currently active.
'''
tool_icon_size = "24px"
'''
The preferred size for tool icons, specified as a string (e.g., "24px").
'''
filenamecounter = 1
'''
A counter used for generating default filenames for new images or saves.
'''

fill_tolerance:float = 1.0
'''
The tolerance level for the flood fill tool, ranging from 0.0 to 1.0.
A higher tolerance allows the fill to spread to colors that are less similar to the target color.
'''

#max undo steps
max_undo_steps = 20
'''
The maximum number of undoable actions stored in the history stack.
'''

# Seçim için yeni global değişkenler
current_selection: set = set()
'''
A set storing the pixel coordinates (e.g., as tuples (x, y)) that are currently selected.
'''
selection_bounds: PySide6.QtCore.QRect = PySide6.QtCore.QRect()
'''
A QRect object representing the bounding box of the current selection.
'''
selection_edge_pixels: set = set()  # Kenar pikselleri
'''
A set storing the pixel coordinates that form the edge of the current selection.
These pixels are typically used for rendering the selection outline.
'''
has_selection: bool = False  # Seçim var mı?
'''
A boolean flag indicating whether there is an active selection on the canvas.
'''
# Seçim animasyonu için
selection_colors = [
    QColor(0, 100, 255, 220),    # Mavi
    QColor(255, 100, 0, 220),    # Turuncu
    QColor(0, 200, 100, 220),    # Yeşil
    QColor(200, 0, 255, 220)     # Mor
]
'''
A list of QColor objects used for animating the selection outline.
The colors cycle to create a visual effect.
'''
current_selection_color_index = 0
'''
The index of the currently active color in the `selection_colors` list.
Used to cycle through colors for selection animation.
'''
selection_animation_timer = None
'''
The timer object responsible for triggering selection animation updates.
'''
selection_animation_active = False  # Animasyon aktif mi?
'''
A boolean flag indicating whether the selection animation is currently active.
'''
selection_animation_speed = 500     # ms cinsinden hız
'''
The speed of the selection animation in milliseconds.
This determines how frequently the selection color changes.
'''

round_rect_corner_radius = 10
'''
The corner radius for drawing rounded rectangles.
'''
#status bar text
class StatusText:
    '''
    A simple class to hold and manage the text displayed in the application's status bar.
    It encapsulates information about the active tool, mouse position, and zoom level.
    '''
    def __init__(self, tool, pos, zoom):
        self.tool = tool
        self.pos = pos
        self.zoom = zoom

statusText = StatusText("Tool:", "Pos:", "Zoom:")
'''
An instance of `StatusText` that holds the current status bar information.
This object is updated dynamically to reflect the application's state.
'''





class Layer:
    '''
    Represents a single layer in the image editor.
    Each layer has its own image, visibility, opacity, and other properties.

    Attributes:
        name (str): The name of the layer.
        active (bool): True if this layer is currently selected/active for editing.
        visible (bool): True if the layer is visible, False otherwise.
        opacity (int): The opacity level of the layer (0-100).
        image (PySide6.QtGui.QImage): The QImage object containing the layer's pixel data.
        rasterized (bool): True if the layer is rasterized, False if it's a vector layer (though current implementation might be primarily raster).
        locked (bool): True if the layer is locked and cannot be edited.
        id (int): A unique identifier for the layer.
    '''
    def __init__(self, name:str, visible:bool=True, opacity:int=100, image:PySide6.QtGui.QImage= QImage(image_width, image_height, PySide6.QtGui.QImage.Format.Format_RGBA64), rasterized:bool=True,locked:bool=False):
        self.name = name
        self.active=False
        self.visible = visible
        self.opacity = opacity
        self.image = image
        self.rasterized = rasterized
        self.locked = locked
        self.id=0

shear_amount = 40
shear_horizontal = True
shear_direction = 1

melt_amount = 30
blur_radius = 3
mosaic_block_size = 10
