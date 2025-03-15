# This file contains global variables used by the image editor.
import PySide6
import PySide6.QtGui
import PySide6.QtCore

# Default pen and brush
pen :PySide6.QtGui.QPen = PySide6.QtGui.QPen()
brush:PySide6.QtGui.QBrush = PySide6.QtGui.QBrush()
# Pen and Brush properties set glabally in mainwindow
# with using colorbox and property sliders

#todo app wide options only
#current tool for drawing string= line, circle, rect, pen, brush, spray, fill
current_tool:str = 'pen'
#color of pencil
pen_color:str = '#000000'
#width of pencil
pen_width:int = 1
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
#radius of circle for spray tool
spray_radius = 50
#density of spray tool
spray_density = 100
#Start position of mouse
startPos:PySide6.QtCore.QPoint
#End position of mouse
lastPos:PySide6.QtCore.QPoint
#Zoom of canvas
zoom = 1
#Zoom factor for zoom in/out
zoomFactor=2
#Image width of original canvas
image_width =400
#Image height of original canvas
image_height = 300
#image background color
image_bg_color = "white"
#flag for zooming true/false
zooming = False
#tool icon size
tool_icon_size = "24px"
#flag for erasing true/false
erasing = False
#flag for drawing true/false
drawing = False
counter = 0
undo_index = -1

pen.setColor(PySide6.QtGui.QColor(pen_color))
pen.setWidth(pen_width)
pen.setCapStyle(PySide6.QtCore.Qt.PenCapStyle.RoundCap)
pen.setJoinStyle(PySide6.QtCore.Qt.PenJoinStyle.RoundJoin)
pen.setStyle(PySide6.QtCore.Qt.PenStyle.SolidLine)
pen.setCosmetic(True)

brush.setColor(PySide6.QtGui.QColor(brush_color))
brush.setStyle(PySide6.QtCore.Qt.BrushStyle.SolidPattern)