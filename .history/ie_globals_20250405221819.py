# This file contains global variables used by the image editor.
import PySide6
import PySide6.QtGui
import PySide6.QtCore
import PySide6.QtWidgets
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtGui import QPen, QColor, QBrush, QImage, QPainter, QMouseEvent, QPixmap


class ie_tool:
    def __init__(self, name:str, icon:str, tool_id:int, shortcut:str=None):
        self.name = name
        self.icon = icon
        self.tool_id = tool_id
        self.shortcut = shortcut
        self.description = ""

ie_pen = ie_tool("Pen", "svgicons/pen-gray.svg", 1000, "P")
ie_brush = ie_tool("Brush", "svgicons/brush.svg", 1001, "B")
ie_line = ie_tool("Line", "svgicons/line-gray.svg", 1002, "L")
ie_rect = ie_tool("Rectangle", "svgicons/rectangle.svg", 1003, "R")
ie_circle = ie_tool("Circle", "svgicons/circle-gray.svg", 1004, "C")
ie_spray = ie_tool("Spray", "svgicons/spray-gray.svg", 1005, "S")
ie_fill = ie_tool("Fill", "svgicons/fill.svg", 1006, "F")
ie_text = ie_tool("Text", "svgicons/text.svg", 1007, "T")
ie_eraser = ie_tool("Eraser", "svgicons/eraser-gray.svg", 1008, "E")
ie_pan = ie_tool("Pan", "svgicons/pan-gray.svg", 1010, "P")
ie_dropper = ie_tool("Dropper", "svgicons/dropper.svg", 1011, "D")
ie_rounded_rect = ie_tool("Rounded Rectangle", "svgicons/rounded-rectangle.svg", 1012, "O")
ie_ellipse = ie_tool("Ellipse", "svgicons/ellipse-gray.svg", 1013, "L")
ie_wand = ie_tool("Wand", "svgicons/wand-gray.svg", 1014, "W")
ie_polygon = ie_tool("Polygon", "svgicons/polygon-gray.svg", 1015, "G")
ie_bezier = ie_tool("Bezier", "svgicons/bezier-gray.svg", 1016, "B")



# Default pen and brush
pen :PySide6.QtGui.QPen = PySide6.QtGui.QPen()
brush:PySide6.QtGui.QBrush = PySide6.QtGui.QBrush()
# Pen and Brush properties set glabally in mainwindow
# with using colorbox and property sliders

#todo app wide options only
#current tool for drawing string= line, circle, rect, pen, brush, spray, fill
current_tool:int = TOOL_PEN
previous_tool:int = TOOL_PEN
#color of pencil
pen_color: QColor = QColor(0,0,0)

#width of pencil
pen_width:int = 15
#Opacity of pencil 0-Transparent to 1-Opaque
pen_opacity :int= 1
#pen blur radius
pen_blur: int = 1
#pen type solid or dashed
pen_type : str= "solid"
#pen cap type round or square
pen_cap = "round"
#pen join type round or bevel
pen_join = "round"
#color of brush
brush_color = "blue"
#Brush blur radius
brush_blur:int = 2
# radius of circle for spray tool
spray_radius = 50
#density of spray tool
spray_density = 100

#Zoom factor for zoom in/ou
zoomInFactor:float = 1.25
zoomOutFactor:float= 1/1.25

#Image width of original canvas
image_width:int =1000
#Image height of original canvas
image_height:int = 800
#image background color
image_bg_color = "white"
#flag for zooming true/false
zooming:bool = False
#tool icon size
tool_icon_size = "24px"
#file name counter
filenamecounter = 1
#flood fill color tolerance
fill_tolerance = 30

round_rect_corner_radius = 10
#status bar text
class StatusText:
    def __init__(self, tool, pos, zoom):
        self.tool = tool
        self.pos = pos
        self.zoom = zoom

statusText = StatusText("Tool:", "Pos:", "Zoom:")




pen.setColor(PySide6.QtGui.QColor(pen_color))
pen.setWidth(pen_width)
pen.setCapStyle(PySide6.QtCore.Qt.PenCapStyle.RoundCap)
pen.setJoinStyle(PySide6.QtCore.Qt.PenJoinStyle.RoundJoin)
pen.setStyle(PySide6.QtCore.Qt.PenStyle.SolidLine)
pen.setCosmetic(True)

brush.setColor(PySide6.QtGui.QColor(QColor(255,255,255,0)))
brush.setStyle(PySide6.QtCore.Qt.BrushStyle.NoBrush)
brush.setStyle(PySide6.QtCore.Qt.BrushStyle.TexturePattern)



class Layer:
    def __init__(self, name:str, visible:bool=True, opacity:int=100, image:PySide6.QtGui.QImage=None, rasterized:bool=True,locked:bool=False):
        self.name = name
        self.active=False
        self.visible = visible
        self.opacity = opacity
        self.image = image
        self.rasterized = rasterized
        self.locked = locked
        self.id=0


