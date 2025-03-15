import math
import os
import sys

import PySide6
from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import QPoint
from PySide6.QtGui import QPen, QColor, QBrush, Qt, QImage, QPainter, QMouseEvent
from PySide6.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QSizePolicy, QLabel, QHBoxLayout

import ie_functions
import ie_globals
from main_ui import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)


        self.colorHeight = None
        self.colorWidth = None
        self.colors = None
        self.ui = Ui_MainWindow()
        self.setupUi(self)

        # creating image object
        #self.image = PySide6.QtGui.QImage(self.size(), PySide6.QtGui.QImage.Format_RGB32)


        # <editor-fold desc="Vector graphics scene">
        # Vector graphics scene
        # graphics_scene = scene.GraphicsScene(self.graphicsView,300,300)
        # self.graphicsView.setScene(graphics_scene)
        # self.graphicsView.setMouseTracking(False)
        # self.graphicsView.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform )
        # </editor-fold>


        # making image color to white
        w=3000
        h=3000

        #self.widgetPicture1.setBaseSize(w,h)
        #policy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        #policy.setHorizontalStretch(2)
        #policy.setVerticalStretch(2)
        #self.widgetPicture1.setSizePolicy(policy)

        self.widgetPicture1.setFixedSize(w * ie_globals.zoomFactor,h * ie_globals.zoomFactor)
        self.widgetPicture1.image=PySide6.QtGui.QImage(w,h,QImage.Format.Format_RGBA64)
        self.pic1=self.widgetPicture1.image
        #self.widgetPicture1.setStyleSheet('background-image:url(\"checker20.png\");')
        #col= QColor(255,0,0,255)
        #self.pic1.fill(col)
        self.pic2 = PySide6.QtGui.QImage(w, h, QImage.Format.Format_RGBA64)
        self.picOrg = PySide6.QtGui.QImage(w, h, QImage.Format.Format_RGBA64)
        #self.pic2.fill(QColor(255, 0, 0))
        #self.graphicsView.hide()

        #tool buttons
        self.toolButtonLine.clicked.connect(self.on_line_click)
        self.toolButtonPen.clicked.connect(self.on_pen_click)
        self.toolButtonRect.clicked.connect(self.on_rect_click)
        self.toolButtonSelectRectangle.clicked.connect(self.on_select_rect_click)
        self.toolButtonCircle.clicked.connect(self.on_circle_click)
        self.toolButtonSpray.clicked.connect(self.on_spray_click)
        self.toolButtonFill.clicked.connect(self.on_fill_click)
        self.toolButtonEraser.clicked.connect(self.on_eraser_click)
        self.toolButtonChecker.clicked.connect(self.on_checker_click)
        self.toolButtonWand.clicked.connect(self.on_wand_click)
        self.toolButtonZoomIn.clicked.connect(self.on_zoom_in_click)
        self.toolButtonZoomOut.clicked.connect(self.on_zoom_out_click)
        self.toolButtonZoomReset.clicked.connect(self.on_zoom_reset_click)




        self.widgetColors.setMouseTracking(True)
        self.widgetColors.mousePressEvent = self.colorbox_on_click

        self.horizontalSlider_1.valueChanged.connect(self.on_slider_change_1)
        self.horizontalSlider_2.valueChanged.connect(self.on_slider_change_2)
        self.horizontalSlider_3.valueChanged.connect(self.on_slider_change_3)


        self.widgetPicture1.setMouseTracking(True)
        self.widgetPicture1.mousePressEvent = self.pic1_mousePressEvent
        self.widgetPicture1.mouseMoveEvent = self.pic1_mouseMoveEvent
        self.widgetPicture1.paintEvent = self.pic1_paintEvent
        #self.widgetPicture1.setFixedSize(400, 300)
        self.widgetPicture1.show()
        self.widgetPicture1.setAttribute(Qt.WidgetAttribute.WA_SetStyle,True)
        self.colorBox()
        #self.color_scene = GraphicsScene(self.widgetColors,200,300)
        #self.widgetColors.setScene(self.color_scene)
        self.statusText=["",""]


        self.statusLabel= QLabel(self.statusbar)
        self.statusLabel.setMinimumSize(500, 20)
    #sliders
    def on_slider_change_1(self, value):
        print("Slider 1 value changed to", value)
        ie_globals.pen.setWidth(value)
    def on_slider_change_2(self, value):
        print("Slider 2 value changed to", value)
        ie_globals.spray_radius = value
    def on_slider_change_3(self, value):
        print("Slider 3 value changed to", value)
        ie_globals.spray_density = value

    def on_zoom_in_click(self):
        ie_globals.zoomFactor *= 1.25
        self.pic1_update()
    def on_zoom_out_click(self):
        ie_globals.zoomFactor /= 1.25
        self.pic1_update()
    def on_zoom_reset_click(self):
        ie_globals.zoomFactor = 1.0
        self.pic1_update()



    def on_line_click(self):
        print("Line button clicked")
        ie_globals.current_tool = "line"
        self.statusText[0]="Mode: line"

    def on_pen_click (self):
        print("Pen button clicked")
        ie_globals.current_tool = "pen"
        self.statusText[0]= "Mode: pen"

    def on_rect_click(self):
        print("Rect button clicked")
        ie_globals.current_tool = "rect"
        self.statusText[0]= "Mode: rectangle"
    def on_select_rect_click(self):
        print("Select button clicked")
        ie_globals.current_tool = "select"
        self.statusText[0]= "Mode: rectangle select"
    def on_circle_click(self):
        print("Circle button clicked")
        ie_globals.current_tool = "circle"
        self.statusText[0]= "Mode: circle select"
    def on_spray_click(self):
        print("Spray button clicked")
        ie_globals.current_tool = "spray"
        self.statusText[0]= "Mode: spray"
    @staticmethod
    def on_fill_click():
        print("Fill button clicked")
        ie_globals.current_tool = "fill"
    @staticmethod
    def on_eraser_click():
        print("Eraser button clicked")
        ie_globals.current_tool = "eraser"
    def on_wand_click(self):
        ie_globals.current_tool = "wand"

    def on_checker_click(self):
        print("Checker button clicked")
        if self.toolButtonChecker.isChecked():
            self.widgetPicture1.setStyleSheet("background-image:url(\"checker20.png\");")
        else:
            self.widgetPicture1.setStyleSheet("")

    def colorBox(self):

        # Dock the ColorMatrixPanel to the right of the parent window
        self.colors = [  # Standard HCIE colors
            "#FFFFFF", "#FFC0C0", "#FFE0C0", "#FFFFC0",
            "#E0E0E0", "#FF8080", "#FFC080", "#FFFF80",
            "#C0C0C0", "#FF0000", "#FF8000", "#FFFF00",
            "#808080", "#C00000", "#C04000", "#C0C000",
            "#404040", "#800000", "#804000", "#808000",
            "#000000", "#400000", "#646464", "#404000",

            "#C0FFC0", "#C0FFFF", "#D3D5F5", "#FFC0FF",
            "#80FF80", "#80FFFF", "#AAAEEB", "#FF80FF",
            "#00FF00", "#00FFFF", "#8389E0", "#FF00FF",
            "#00C000", "#00C0C0", "#232B99", "#C000C0",
            "#008000", "#008080", "#101566", "#800080",
            "#004000", "#004040", "#04051A", "#400040",
        ]


        color_item = QtWidgets.QGraphicsRectItem(QtCore.QRectF(0, 0, 1, 1))
        pen = QPen(QColor(255, 0, 255), 10)
        pen.setCosmetic(True)
        pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        colorscene= QGraphicsScene()
        self.widgetColors.setSceneRect(0, 0, 100, 100)
        self.widgetColors.setScene(colorscene)

        colorscene.addItem(color_item)

        self.colorWidth = 20
        self.colorHeight = 15
        for i in range(12):
            for j in range(4):
                color_str = self.colors[i * 4 + j]
                if len(color_str) == 9:  # Check if it's in ARGB format #AARRGGBB
                    alpha = int(color_str[1:3], 16)
                    red = int(color_str[3:5], 16)
                    green = int(color_str[5:7], 16)
                    blue = int(color_str[7:9], 16)
                    color = QColor(red, green, blue, alpha)
                    print(red, green, blue, alpha)
                else: #RRGGBB

                    red = int(color_str[1:3], 16)
                    green = int(color_str[3:5], 16)
                    blue = int(color_str[5:7], 16)

                    color = QColor(red, green, blue,255)
                    print(red,green,blue)


                pen= QPen(QColor(120, 120, 120), 1)


                color_item = QtWidgets.QGraphicsRectItem(
                    QtCore.QRectF(j * self.colorWidth-1, i * self.colorHeight-1,
                                  self.colorWidth, self.colorHeight))
                color_item.setPen(pen)
                color_item.setBrush(QBrush(color))
                colorscene.addItem(color_item)

        bottom = self.colorHeight * 12
        self.widgetColors.update()



    def colorbox_on_click(self, event):
        x, y = event.x(), event.y()
        painter = QPainter(self.widgetColors)
        img= self.widgetColors.grab()
        color= img.toImage().pixel(x, y)
        # color_index = (y // self.colorHeight) * 4 + (x // self.colorWidth)
        # print(x,y,color_index)
        # if 0 <= color_index < len(self.colors):
        #     color_str=self.colors[color_index]
        #     if len(color_str) == 9:  # Check if it's in ARGB format #AARRGGBB
        #         alpha = int(color_str[1:3], 16)
        #         red = int(color_str[3:5], 16)
        #         green = int(color_str[5:7], 16)
        #         blue = int(color_str[7:9], 16)
        #         color = QColor(red, green, blue, alpha)
        #         print(red, green, blue, alpha)
        #     else:  # RRGGBB
        #
        #         red = int(color_str[1:3], 16)
        #         green = int(color_str[3:5], 16)
        #         blue = int(color_str[5:7], 16)
        #
        #         color = QColor(red, green, blue, 255)
        #         print(red, green, blue)

        ie_globals.pen.setColor(color)
        ie_globals.brush.setColor(color)
        ie_globals.pencolor = color
        ie_globals.brushcolor = color
#region mouse events [rgba(255, 152, 121,0.3)]

    def pic1_mousePressEvent(self, event):
        # print mouse position
        print  (event.pos())
        # if left mouse button is pressed
        if event.button() == Qt.MouseButton.LeftButton:
            # make drawing flag true
            eventstr="down"
            self.pic2 = self.picOrg.copy()

            ie_globals.drawing = True
            # make last point to the point of cursor
            ie_globals.lastPos = event.pos()
            ie_globals.startPos = event.pos()
            virtualStartPos: QPoint = QPoint(
                math.trunc(ie_globals.startPos.x() / ie_globals.zoomFactor),
                math.trunc(ie_globals.startPos.y() / ie_globals.zoomFactor))
            if ie_globals.current_tool == 'pen':
                    ie_functions.draw_line(self.picOrg,  virtualStartPos, virtualStartPos, eventstr)
                    ie_globals.startPos = event.pos()
            elif ie_globals.current_tool == 'fill':
                ie_functions.fill(img1=self.pic1, pt1= event.pos(),task="down")
            elif ie_globals.current_tool == 'wand':
                ie_functions.select_wand(img1=self.pic1, pt1= event.pos(),task="down")
            elif ie_globals.current_tool == 'eraser':
                ie_functions.erase(self.pic1, event.pos(), "down")
            
            self.pic1_update()
    def pic1_mouseMoveEvent(self, event:QMouseEvent):
        eventstr:str="move"

        if event.buttons() == Qt.MouseButton.LeftButton :
            virtualStartPos: QPoint = QPoint(
                math.trunc(ie_globals.startPos.x() / ie_globals.zoomFactor),
                math.trunc(ie_globals.startPos.y() / ie_globals.zoomFactor)
            )
            virtualpos: QPoint = QPoint(
                math.trunc(event.pos().x() / ie_globals.zoomFactor),
                math.trunc(event.pos().y() / ie_globals.zoomFactor)

            )
            self.statusText[1]= "Mouse Position: " + str(virtualpos.x()) + ", " + str(virtualpos.y())
            if ie_globals.drawing:
                if ie_globals.current_tool == 'pen':
                    ie_functions.draw_line(self.picOrg,  virtualStartPos, virtualpos, eventstr)
                    ie_globals.startPos = event.pos()
                elif ie_globals.current_tool == 'line':
                    self.picOrg=self.pic2.copy()
                    ie_functions.draw_line(self.picOrg, virtualStartPos, virtualpos, eventstr)
                elif ie_globals.current_tool == 'circle':
                    self.picOrg = self.pic2.copy()
                    ie_functions.draw_circle(self.picOrg, virtualStartPos, virtualpos, eventstr)
                elif ie_globals.current_tool == 'rect':
                    self.picOrg = self.pic2.copy()
                    ie_functions.draw_rect(self.picOrg, virtualStartPos, virtualpos, eventstr)
                elif ie_globals.current_tool == 'spray':
                    ie_functions.draw_spray(self.picOrg, virtualpos,eventstr)

                ie_globals.lastPos = event.pos()
                # update
                self.pic1_update()
                
#endregion
#region paint event [rgba(150, 150, 225,0.3)]
    #picture 1 view update from original image
    def pic1_update(self):
        self.statusLabel.setText("  "+ str(self.statusText[0]) +" "+ str(self.statusText[1]))
        w=self.picOrg.width()*ie_globals.zoomFactor
        h=self.picOrg.height()*ie_globals.zoomFactor
        #policy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        #policy.setHorizontalStretch(1)
        #policy.setVerticalStretch(1)
        #self.widgetPicture1.setSizePolicy(policy)
        #self.widgetPicture1.minimumWidth= w
        #self.widgetPicture1.minimumHeight= h
        #self.widgetPicture1.width =w
        #self.widgetPicture1.height =h

        self.widgetPicture1.setFixedSize(w, h)

        self.pic1 = self.picOrg.scaled(w, h,Qt.AspectRatioMode.KeepAspectRatio)
        self.widgetPicture1.image=self.pic1

        self.scrollArea.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        self.scrollArea.minimumWidth= w
        self.scrollArea.minimumHeight= h
        self.scrollArea.width =w
        self.scrollArea.height =h
        self.scrollArea.update()

        
        self.widgetPicture1.update() #call paint event
    # paint event
    def pic1_paintEvent(self, event):
        # create a canvas
        canvasPainter = QPainter(self.widgetPicture1)
        
        # draw rectangle  on the canvas
        canvasPainter.drawImage(0,0,  self.pic1)
        canvasPainter.end()
        canvasPainter = None

    #def paintEvent(self, event):

        #pass
        #örnek painter
        # painter = QPainter(self)
        # painter.setPen(QPen(Qt.red, 4))
        # painter.setRenderHint(QPainter.Antialiasing)
        #
        # polyline = QPolygonF()
        # h_div_2 = self.height() // 2
        # samples = self.width() * 10
        #
        # for x in range(samples):
        #     y = h_div_2 + math.sin(x * 6.28 / samples) * h_div_2
        #     polyline.append(QPointF(x * self.width() / samples, y))
        #
        # painter.drawPolyline(polyline)

#endregion
if __name__ == "__main__":
    #Bu kısımda değişiklik yapılırsa çizimler kötüleşiyor. DPI ile alakalı
    os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "0"
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    os.environ["QT_SCALE_FACTOR"] = "1"

    app = QApplication(sys.argv)
    app.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling)
    app.setAttribute( Qt.ApplicationAttribute.AA_UseHighDpiPixmaps)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())