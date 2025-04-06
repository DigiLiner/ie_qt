# This file contains global variables used by the image editor.
import PySide6
import PySide6.QtGui
import PySide6.QtCore
import PySide6.QtWidgets
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtGui import QPen, QColor, QBrush, QImage, QPainter, QMouseEvent, QPixmap

# Default pen and brush
pen :PySide6.QtGui.QPen = PySide6.QtGui.QPen()
brush:PySide6.QtGui.QBrush = PySide6.QtGui.QBrush()
# Pen and Brush properties set glabally in mainwindow
# with using colorbox and property sliders

#todo app wide options only
#current tool for drawing string= line, circle, rect, pen, brush, spray, fill
current_tool:str = 'pen'
previous_tool:str = 'pen'
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

brush.setColor(PySide6.QtGui.QColor(brush_color))
brush.setStyle(PySide6.QtCore.Qt.BrushStyle.NoBrush)
brush.setStyle(PySide6.QtCore.Qt.BrushStyle.TexturePattern)
brush.setT


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


