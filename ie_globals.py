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
ie_tool_brush = ie_tool("Brush", "svgicons/brush.svg", 1001, "B", "Brush Tool",False)
ie_tool_line = ie_tool("Line", "svgicons/line-gray.svg", 1002, "L", "Line Tool",True)
ie_tool_rect = ie_tool("Rectangle", "svgicons/rectangle.svg", 1003, "R", "Rectangle Tool",True)
ie_tool_circle = ie_tool("Circle", "svgicons/circle-gray.svg", 1004, "C", "Circle Tool",True)
ie_tool_spray = ie_tool("Spray", "svgicons/spray-gray.svg", 1005, "S", "Spray Tool",True)
ie_tool_fill = ie_tool("Fill", "svgicons/fill.svg", 1006, "F", "Fill Tool",True)
ie_tool_text = ie_tool("Text", "svgicons/text.svg", 1007, "T", "Text Tool",False)
ie_tool_eraser = ie_tool("Eraser", "svgicons/eraser-gray.svg", 1008, "E", "Eraser Tool",False)
ie_tool_pan = ie_tool("Pan", "svgicons/pan-gray.svg", 1010, "P", "Pan Tool",False)
ie_tool_dropper = ie_tool("Dropper", "svgicons/dropper.svg", 1011, "D", "Dropper Tool",True)
ie_tool_rounded_rect = ie_tool("Rounded Rectangle", "svgicons/rounded-rectangle.svg", 1012, "O","Rounded Rectangle Tool",True)
ie_tool_ellipse = ie_tool("Ellipse", "svgicons/ellipse-gray.svg", 1013, "L", "Ellipse Tool",True)
ie_tool_wand = ie_tool("Wand", "svgicons/wand.svg", 1014, "W", "Wand Tool",False)
ie_tool_polygon = ie_tool("Polygon", "svgicons/polygon-gray.svg", 1015, "G","Polygon Tool",False)
ie_tool_bezier = ie_tool("Bezier", "svgicons/bezier-gray.svg", 1016, "B", "Bezier Tool",False)
ie_tool_select_rect = ie_tool("Select Rectangle", "svgicons/select-rectangle-gray.svg", 1017, "S","Select Rectangle Tool",False)
ie_tool_select_circle = ie_tool("Select Circle", "svgicons/select-circle-gray.svg", 1018, "S","Select Circle Tool",False)
ie_tool_select_polygon = ie_tool("Select Polygon", "svgicons/select-polygon.svg", 1019, "S","Select Polygon Tool",False)
ie_tool_select_lasso = ie_tool("Select Lasso", "svgicons/lasso_select.svg", 1020, "S","Select Lasso Tool",False)
ie_tool_select_path = ie_tool("Select Path", "svgicons/select-path.svg", 1021, "S","Select Path Tool",False)
ie_tool_crop = ie_tool("Crop", "svgicons/crop.svg", 1022, "C", "Crop Tool",False)


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


# Default pen and brush
current_pen :PySide6.QtGui.QPen = PySide6.QtGui.QPen()
current_brush:PySide6.QtGui.QBrush = PySide6.QtGui.QBrush()
# Pen and Brush properties set glabally in mainwindow
# with using colorbox and property sliders

#todo app wide options only
#current tool for drawing string= line, circle, rect, pen, brush, spray, fill
current_tool:ie_tool = ie_tool_pen
previous_tool:ie_tool = ie_tool_pen
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
fill_tolerance = 200

round_rect_corner_radius = 10
#status bar text
class StatusText:
    def __init__(self, tool, pos, zoom):
        self.tool = tool
        self.pos = pos
        self.zoom = zoom

statusText = StatusText("Tool:", "Pos:", "Zoom:")


current_pen.setColor(PySide6.QtGui.QColor(pen_color))
current_pen.setWidth(pen_width)
current_pen.setCapStyle(PySide6.QtCore.Qt.PenCapStyle.RoundCap)
current_pen.setJoinStyle(PySide6.QtCore.Qt.PenJoinStyle.RoundJoin)
current_pen.setStyle(PySide6.QtCore.Qt.PenStyle.SolidLine)
current_pen.setCosmetic(True)

current_brush.setColor(PySide6.QtGui.QColor(QColor(255,255,255,0)))
current_brush.setStyle(PySide6.QtCore.Qt.BrushStyle.NoBrush)
current_brush.setStyle(PySide6.QtCore.Qt.BrushStyle.TexturePattern)



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


