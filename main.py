import math
import os
import sys

import PySide6
from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import QPoint
from PySide6.QtGui import QPen, QColor, QBrush, Qt, QImage, QPainter, QMouseEvent, QPixmap
from PySide6.QtWidgets import QWidget,QApplication, QMainWindow, QGraphicsScene, QSizePolicy, QLabel, QHBoxLayout
from typing import Type, cast

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
        # w=1920
        # h=1080

        #self.widgetPicture1.setBaseSize(w,h)
        #policy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        #policy.setHorizontalStretch(2)
        #policy.setVerticalStretch(2)
        #self.widgetPicture1.setSizePolicy(policy)

        # self.widgetPicture1.setFixedSize(w * ie_globals.zoomFactor,h * ie_globals.zoomFactor)
        # self.widgetPicture1.image=PySide6.QtGui.QImage(w,h,QImage.Format.Format_RGBA64)
        # self.pic1=self.widgetPicture1.image
        # #self.widgetPicture1.setStyleSheet('background-image:url(\"checker20.png\");')
        # #col= QColor(255,0,0,255)
        # #self.pic1.fill(col)
        # self.pic2 = PySide6.QtGui.QImage(w, h, QImage.Format.Format_RGBA64)
        # self.picOrg = PySide6.QtGui.QImage(w, h, QImage.Format.Format_RGBA64)
        #self.pic2.fill(QColor(255, 0, 0))
        #self.graphicsView.hide()
        self.tabWidget.removeTab(0)
        import ie_editor
        EditorType = cast(Type[QWidget], ie_editor.Editor)
        doc: Type[QWidget] = EditorType
        self.tabWidget.addTab(doc(QWidget), "Picture" + str(ie_globals.filenamecounter))
        self.tabWidget.setCurrentIndex(self.tabWidget.count() - 1)
        ie_globals.filenamecounter += 1
        #action
        self.actionOpen.triggered.connect(self.open_file)
        self.actionSave.triggered.connect(self.save_file)
        self.actionNew.triggered.connect(self.new_file)
        self.actionUndo.triggered.connect(self.undo)
        self.actionRedo.triggered.connect(self.redo)

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


        # self.widgetPicture1.setMouseTracking(True)
        # self.widgetPicture1.mousePressEvent = self.pic1_mousePressEvent
        # self.widgetPicture1.mouseMoveEvent = self.pic1_mouseMoveEvent
        # self.widgetPicture1.paintEvent = self.pic1_paintEvent
        #self.widgetPicture1.setFixedSize(400, 300)
        # self.widgetPicture1.show()
        # self.widgetPicture1.setAttribute(Qt.WidgetAttribute.WA_SetStyle,True)

        #self.color_scene = GraphicsScene(self.widgetColors,200,300)
        #self.widgetColors.setScene(self.color_scene)

        ie_globals.current_tool = "pen"

        self.statusLabel= QLabel(self.statusbar)
        self.statusLabel.setMinimumSize(500, 20)
        self.colorBox()
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

        import ie_editor
        activeDoc = self.tabWidget.currentWidget()
        activeDoc.zoomFactor = activeDoc.zoomFactor * ie_globals.zoomInFactor
        activeDoc.pic1_update()
    def on_zoom_out_click(self):
        import ie_editor
        activeDoc = self.tabWidget.currentWidget()
        activeDoc.zoomFactor = activeDoc.zoomFactor * ie_globals.zoomOutFactor
        activeDoc.pic1_update()
    def on_zoom_reset_click(self):
        import ie_editor
        activeDoc = self.tabWidget.currentWidget()
        activeDoc.zoomFactor = 1.0
        self.pic1_update()
    def on_line_click(self):
        print("Line button clicked")
        ie_globals.current_tool = "line"
        ie_globals.statusText[0]="Mode: line"

    def on_pen_click (self):
        print("Pen button clicked")
        ie_globals.current_tool = "pen"
        ie_globals.statusText[0]= "Mode: pen"

    def on_rect_click(self):
        print("Rect button clicked")
        ie_globals.current_tool = "rect"
        ie_globals.statusText[0]= "Mode: rectangle"
    def on_select_rect_click(self):
        print("Select button clicked")
        ie_globals.current_tool = "select"
        ie_globals.statusText[0]= "Mode: rectangle select"
    def on_circle_click(self):
        print("Circle button clicked")
        ie_globals.current_tool = "circle"
        ie_globals.statusText[0]= "Mode: circle select"
    def on_spray_click(self):
        print("Spray button clicked")
        ie_globals.current_tool = "spray"
        ie_globals.statusText[0]= "Mode: spray"
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
    def open_file(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", os.getcwd(), "Image Files (*.png *.jpg *.jpeg *.gif)")
        if filename:
            import ie_editor
            doc = ie_editor.Editor(QWidget)
            self.tabWidget.addTab(doc, "Picture" + str(ie_globals.filenamecounter))
            doc.picOrg = PySide6.QtGui.QImage(filename)
            doc.pic1_update()
            #todo : filename will be added to tab name
            self.tabWidget.setCurrentIndex(self.tabWidget.count() - 1)
    def save_file(self):
        #filename will get from tab name
        import ie_editor
        activeDoc = self.tabWidget.currentWidget()

        filename, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save File", os.getcwd(), "Image Files (*.png *.jpg *.jpeg *.gif)")
        if filename:
            activeDoc.picOrg.save(filename)
    def new_file(self):
       
        #init new file dialog
        import dialog_newImage_ui
        dialog = dialog_newImage_ui.Ui_Dialog()
        dialog_instance = QtWidgets.QDialog()  
        dialog.setupUi(dialog_instance)
        dialog.comboBoxSizeList.addItems(["100x100", "500x500", "800x600","1024x768","1280x1024","1600x1200","1920,1080","2048x1536"])
        dialog.comboBoxSizeList.setCurrentIndex(3)
        dialog.plainTextEditWidth.setPlainText("500")
        dialog.plainTextEditHeight.setPlainText("500")
        # Show the dialog
        dialog_instance.exec()

        # Create a new image
        import ie_editor
        EditorType = cast(Type[QWidget], ie_editor.Editor)
        doc = EditorType
        self.tabWidget.addTab(doc(QWidget), "Picture" + str(ie_globals.filenamecounter))
        ie_globals.filenamecounter += 1
        self.tabWidget.setCurrentIndex(self.tabWidget.count()-1)
    def undo(self):
        import ie_editor
        print("Undo")
        activeDoc = self.tabWidget.currentWidget()
        activeDoc.undoImage()
    def redo(self):
        print("Redo")
        import ie_editor
        activeDoc = self.tabWidget.currentWidget()
        activeDoc.redoImage()
    def colorBox(self):

        # Dock the ColorMatrixPanel to the right of the parent window
        self.colors = [  # Standard HCIE colors
            "#FFFFFF", "#FFC0C0", "#FFE0C0", "#FFFFC0",
            "#E0E0E0", "#FF8080", "#FFC080", "#FFFF80",
            "#C0C0C0", "#FF0000", "#FF8000", "#E0E080",
            "#808080", "#C00000", "#C04000", "#C0C000",
            "#404040", "#800000", "#804000", "#808000",
            "#000000", "#400000", "#604000", "#404000",

            "#C0FFC0", "#C0FFFF", "#D3D5F5", "#FFC0FF",
            "#80FF80", "#80FFFF", "#AAAEEB", "#FF80FF",
            "#00FF00", "#00FFFF", "#8389E0", "#FF00FF",
            "#00C000", "#00C0C0", "#5E61b8", "#C000C0",
            "#008000", "#008080", "#2d3c9c", "#800080",
            "#004000", "#004040", "#04051A", "#400040",
        ]


        color_item = QtWidgets.QGraphicsRectItem(QtCore.QRectF(0, 0, 1, 1))
        pen = QPen(QColor(255, 0, 255), 10)
        pen.setCosmetic(True)
        pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        colorscene= QGraphicsScene(0,0,100,100)
        self.widgetColors.setSceneRect(0, 0, 100, 100)
        self.widgetColors.setScene(colorscene)

        colorscene.addItem(color_item)
        #Vertical layout of colors
        vertical_layout = True
        if vertical_layout:
            rows=12
            columns=4
            self.colorWidth = 20
            self.colorHeight = 15
        else:
            rows=4
            columns=12
            self.colorWidth = 20
            self.colorHeight = 20


        self.colorWidth = 20
        self.colorHeight = 20
        for row in range(rows):
            for col in range(columns):
                color_str = ""
                if vertical_layout:
                    color_str = self.colors[row * columns + col]
                else:
                    color_str = self.colors[col * rows + row]
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
                    #print(red,green,blue)

                pen= QPen(QColor(120, 120, 120), 1)
                color_item = QtWidgets.QGraphicsRectItem(
                    QtCore.QRectF(col * self.colorWidth, row * self.colorHeight,
                                  self.colorWidth, self.colorHeight))
                color_item.setPen(pen)
                color_item.setBrush(QBrush(color))
                colorscene.addItem(color_item)

        bottom = self.colorHeight * 12
        self.widgetColors.update()



    def colorbox_on_click(self, event):
        x, y = event.x(), event.y()
        img= self.widgetColors.grab()
        color= img.toImage().pixel(x, y)
       

        ie_globals.pen.setColor(color)
        ie_globals.brush.setColor(color)
        ie_globals.pencolor = color
        ie_globals.brushcolor = color

    def paintEvent(self, event):
        ie_globals.statusText[0]= "Tool: "+ str(ie_globals.current_tool)
        self.statusLabel.setText("  "+ str(ie_globals.statusText[0]) +" "+ str(ie_globals.statusText[1]))

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