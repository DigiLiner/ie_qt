import math
import os
import platform
import sys
from logging import exception
#
import PySide6
from PySide6.QtCore import Qt
from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import QPoint,QSize
from PySide6.QtGui import QPen, QColor, QBrush, QImage, QPainter, QMouseEvent, QPixmap,QIcon
import PySide6.QtGui
from PySide6.QtWidgets import QWidget,QApplication, QMainWindow, QGraphicsScene, QSizePolicy, QLabel, QHBoxLayout
from typing import Type, cast

import ie_globals
from main_ui import Ui_MainWindow
from float_window_ui import Ui_floatWindow as float_window_ui
   

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.colorHeight = None
        self.colorWidth = None
        self.colors = None
        self.ui = Ui_MainWindow()
        self.setupUi(self)
       
        print(os.path)
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
        self.dwColorBox.dockLocationChanged.connect(self.colorBox)
        

        self.closeEvent = self.close_event



        #tool buttons
        # self.toolButtonLine.clicked.connect(self.on_line_click)
        # self.toolButtonPen.clicked.connect(self.on_pen_click)
        # self.toolButtonRect.clicked.connect(self.on_rect_click)
        # self.toolButtonRoundRect.clicked.connect(self.on_round_rect_click)
        # self.toolButtonSelectRectangle.clicked.connect(self.on_select_rect_click)
        # self.toolButtonCircle.clicked.connect(self.on_circle_click)
        # self.toolButtonSpray.clicked.connect(self.on_spray_click)
        # self.toolButtonFill.clicked.connect(self.on_fill_click)
        # self.toolButtonEraser.clicked.connect(self.on_eraser_click)
        # self.toolButtonChecker.clicked.connect(self.on_checker_click)
        # self.toolButtonWand.clicked.connect(self.on_wand_click)
        # self.toolButtonZoomIn.clicked.connect(self.on_zoom_in_click)
        # self.toolButtonZoomOut.clicked.connect(self.on_zoom_out_click)
        # self.toolButtonZoomReset.clicked.connect(self.on_zoom_reset_click)
        # self.toolButtonDropper.clicked.connect(self.on_dropper_click)
        #for tool_button in [self.toolButtonLine, self.toolButtonPen, self.toolButtonRect, self.toolButtonRoundRect, self.toolButtonSelectRectangle, self.toolButtonCircle, self.toolButtonSpray, self.toolButtonFill, self.toolButtonEraser, self.toolButtonChecker, self.toolButtonWand, self.toolButtonZoomIn, self.toolButtonZoomOut, self.toolButtonZoomReset, self.toolButtonDropper]:

        #search for all tool buttons in the ui and set events
        for obj in self.dockWidgetContents.children():
            if isinstance(obj, QtWidgets.QToolButton):
                self.set_button_events(obj)
                #print("T1:",obj.objectName())
            for obj1 in obj.children():
                if isinstance(obj1, QtWidgets.QToolButton):
                    self.set_button_events(obj1)
                    #print("T2:", obj1)
                for obj2 in [obj1.children()]:

                    if isinstance(obj2, QtWidgets.QToolButton):
                        self.set_button_events(obj2)
                        #print("T3:", obj2.objectName())
        self.setSvgColors()
        self.widgetColors.setMouseTracking(True)
        self.widgetColors.mousePressEvent = self.colorbox_on_click
        # Slider events
        self.horizontalSlider_1.valueChanged.connect(self.on_slider_change_1)
        self.horizontalSlider_2.valueChanged.connect(self.on_slider_change_2)
        self.horizontalSlider_3.valueChanged.connect(self.on_slider_change_3)
        self.horizontalSlider_4.valueChanged.connect(self.on_slider_change_4)
        self.horizontalSlider_5.valueChanged.connect(self.on_slider_change_5)
        self.horizontalSlider_6.valueChanged.connect(self.on_slider_change_6)

        

        ie_globals.current_tool = ie_globals.ie_tool_pen

        self.statusLabel= QLabel(self.statusbar)
        self.statusLabel.setMinimumSize(500, 20)
        self.colorBox()
        #set a timer update periodically
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.timer_update)
        #refresh every 200ms , status update , repaint etc.
        self.timer.start(200)

        # self.toolButtonEraser = QToolButton(self.gridLayoutWidget)
    #     self.toolButtonEraser.setObjectName(u"toolButtonEraser")
        
      
    #sliders
        self.disable_slider_events=False # Disable slider events while updating them to avoid infinite loop
        self.set_slider_values()

    def set_slider_values(self):
        self.disable_slider_events = True # Disable slider events while updating them to avoid infinite loop
        self.horizontalSlider_1.setMinimum(1)
        self.horizontalSlider_1.setMaximum(100)
        self.horizontalSlider_1.setValue(ie_globals.pen_width)
        self.horizontalSlider_2.setMinimum(1)
        self.horizontalSlider_2.setMaximum(100)
        self.horizontalSlider_2.setValue(ie_globals.spray_radius)
        self.horizontalSlider_3.setMinimum(1)
        self.horizontalSlider_3.setMaximum(100)
        self.horizontalSlider_3.setValue(ie_globals.spray_density)
        #todo change
        self.horizontalSlider_4.setMinimum(1)
        self.horizontalSlider_4.setMaximum(100)
        self.horizontalSlider_4.setValue(ie_globals.pen_opacity)
        self.horizontalSlider_5.setMinimum(1)
        self.horizontalSlider_5.setMaximum(100)
        self.horizontalSlider_5.setValue(ie_globals.pen_blur)
        self.horizontalSlider_6.setMinimum(1)
        self.horizontalSlider_6.setMaximum(255)
        self.horizontalSlider_6.setValue(ie_globals.fill_tolerance)
        self.disable_slider_events = False
        self.toolBar.setIconSize(QtCore.QSize(24, 24))

    def resource_path(self, relative_path):
        try:
            if hasattr(sys, '_MEIPASS'):
                base_path = sys._MEIPASS
            else:
                base_path = os.path.abspath(".")
        except Exception:
            base_path = os.path.abspath(".")
        print("basepath",base_path)
        return os.path.join(base_path, relative_path)
   
    

    ##################################################
    ######################################################
    ##########################################################
    def set_button_events(self,tool_button:QtWidgets.QToolButton):
        tool_button.setMouseTracking(True)
        tool_button.setTabletTracking(True)
        tool_button.mouseMoveEvent = lambda e: self.on_tool_button_move(e, tool_button)
        tool_button.mousePressEvent =lambda e:self.on_tool_button_click(tool_button)
        #print("Tool button text:", tool_button.objectName())


    def on_tool_button_move(self, event,tool_button:QtWidgets.QToolButton):
        if self.disable_slider_events:
            return
        #print("Tool button text:", tool_button.objectName())
    def set_tool_button_uncheck(self, tool_button: QtWidgets.QToolButton):
        tool_button.setCheckable(False)
        tool_button.setChecked(False)
        tool_name = tool_button.objectName().replace("toolButton", "").lower()
        
        tool_button.setStyleSheet("background-color:#AACCCC ;")   
        if self.old_tool_button is not None:
            if self.old_tool_button.objectName() != tool_button.objectName():
                self.old_tool_button.setCheckable(False)
                self.old_tool_button.setChecked(False)                
                self.old_tool_button.setStyleSheet("")
        self.old_tool_button = tool_button
        if not ie_globals.tools:
            print("No tools found in ie_globals.tools.")
            return
        
        

    old_tool_button = None            

    def on_tool_button_click(self, tool_button:QtWidgets.QToolButton):
        self.set_tool_button_uncheck(tool_button)
 
        ctool=ie_globals.current_tool
        if tool_button.objectName() == "toolButtonPen":
            ctool=ie_globals.ie_tool_pen
        elif tool_button.objectName() == "toolButtonLine":
            ctool=ie_globals.ie_tool_line
        elif tool_button.objectName() == "toolButtonRectangle":
            ctool=ie_globals.ie_tool_rect
        elif tool_button.objectName() == "toolButtonRoundRectangle":
            ctool=ie_globals.ie_tool_rounded_rect
        elif tool_button.objectName() == "toolButtonSelectRectangle":
            ctool=ie_globals.ie_select_rect
        elif tool_button.objectName() == "toolButtonCircle":
            ctool=ie_globals.ie_tool_circle
        elif tool_button.objectName() == "toolButtonSpray":
            ctool=ie_globals.ie_tool_spray
        elif tool_button.objectName() == "toolButtonFill":
            ctool=ie_globals.ie_tool_fill
        elif tool_button.objectName() == "toolButtonEraser":
            ctool=ie_globals.ie_tool_eraser
        elif tool_button.objectName() == "toolButtonWand":
            ctool=ie_globals.ie_tool_wand
        elif tool_button.objectName() == "toolButtonZoomIn":
            self.zoom_in()
        elif tool_button.objectName() == "toolButtonZoomOut":
            self.zoom_out()
        elif tool_button.objectName() == "toolButtonZoomReset":
            self.zoom_reset()
        elif tool_button.objectName() == "toolButtonFlipHorizontal":
            self.flipHorizontal()
        elif tool_button.objectName() == "toolButtonFlipVertical":
            self.flipVertical()
        elif tool_button.objectName() == "toolButtonDropper":            
            ie_globals.previous_tool = ie_globals.current_tool
            ctool = ie_globals.ie_tool_dropper
            ie_globals.statusText.tool= "Mode: dropper"
        elif tool_button.objectName() == "toolButtonChecker":
            import ie_editor
            activeDoc:ie_editor.Editor = self.tabWidget.currentWidget()
            activeDoc.is_checkerboard_enabled=not activeDoc.is_checkerboard_enabled
            if activeDoc.is_checkerboard_enabled==True:
                activeDoc.widgetPicture1.setStyleSheet("background-image:url(:/png/resources/images/checker20.png);")
                
            else:
                activeDoc.widgetPicture1.setStyleSheet("")
            print(tool_button.isChecked())
            self.widgetPicture1.update()
        elif tool_button.objectName() == "toolButtonCrop":
            ie_globals.previous_tool = ie_globals.current_tool
            ctool = ie_globals.ie_tool_crop
        
        else:
            exception("Tool button click event not implemented for tool:", ctool)
        ie_globals.current_tool = ctool
        ie_globals.statusText.tool = "Mode: " + ctool.name
        tool_button.setCheckable(True)
        tool_button.setChecked(True)


    def timer_update(self):
        if self.isMinimized():
            float_window.hide()
        else:
            try:
                main_geometry = self.geometry()
                if float_window.enabled==True:
                    float_geometry = float_window.geometry()
                    float_geometry.setLeft(main_geometry.right() - float_geometry.width() - 150)
                    float_geometry.setTop(main_geometry.top())
                    float_geometry.setHeight(60)
                    float_geometry.setWidth(150)
                    # Only show float window when properly positioned
                    float_window.setGeometry(float_geometry)
                    float_window.show()


            except AttributeError as e:
                print(f"An error occurred while setting the geometry of the float window: {e}")



        self.statusLabel.setText(ie_globals.statusText.tool + " Pos: " + str(ie_globals.statusText.pos) + " Zoom: " + str(ie_globals.statusText.zoom))
        self.repaint()

    def on_slider_change_1(self, value):
        if self.disable_slider_events:
            return
        print("Slider 1 value changed to", value)
        ie_globals.current_pen.setWidth(value)
    def on_slider_change_2(self, value):
        if self.disable_slider_events:
            return
        print("Slider 2 value changed to", value)
        ie_globals.spray_radius = value
    def on_slider_change_3(self, value):
        if self.disable_slider_events:
            return
        print("Slider 3 value changed to", value)
        ie_globals.spray_density = value
    def on_slider_change_4(self, value):
        if self.disable_slider_events:
            return
        print("Slider 4 value changed to", value)
        
    def on_slider_change_5(self, value):
        if self.disable_slider_events:
            return
        print("Slider 5 value changed to", value)
    def on_slider_change_6(self, value ):
        if self.disable_slider_events:
            return
        print("Slider 6 value changed to", value)
        ie_globals.fill_tolerance = value
        print("Fill tolerance set to", ie_globals.fill_tolerance)  



    def zoom_in(self):
        import ie_editor
        if isinstance(self.tabWidget.currentWidget(), ie_editor.Editor):
            activeDoc:ie_editor.Editor =  self.tabWidget.currentWidget()
            activeDoc.zoomFactor = activeDoc.zoomFactor * ie_globals.zoomInFactor
            activeDoc.pic1_update()
    def zoom_out(self):
        import ie_editor
        activeDoc: ie_editor.Editor = self.tabWidget.currentWidget()
        activeDoc.zoomFactor = activeDoc.zoomFactor * ie_globals.zoomOutFactor
        activeDoc.pic1_update()
    def zoom_reset(self):
        import ie_editor
        activeDoc: ie_editor.Editor = self.tabWidget.currentWidget()
        activeDoc.zoomFactor = 1.0
        activeDoc.pic1_update()

    def flipVertical(self):
        import ie_editor
        activeDoc:ie_editor.Editor = self.tabWidget.currentWidget()
        activeDoc.picOrg = activeDoc.picOrg.mirrored(False, True)
        activeDoc.appendUndoImage()
        activeDoc.pic1_update()
    def flipHorizontal(self):
        import ie_editor
        activeDoc:ie_editor.Editor = self.tabWidget.currentWidget()
        activeDoc.picOrg = activeDoc.picOrg.mirrored(True, False)
        activeDoc.appendUndoImage()
        activeDoc.pic1_update()

    # def on_line_click(self):
    #     print("Line button clicked")
    #     ie_globals.current_tool = "line"
    #     ie_globals.statusText.tool="Mode: line"
    #
    # def on_pen_click (self):
    #     print("Pen button clicked")
    #     ie_globals.current_tool = "pen"
    #     ie_globals.statusText.tool= "Mode: pen"
    #
    # def on_rect_click(self):
    #     print("Rect button clicked")
    #     ie_globals.current_tool = "rect"
    #     ie_globals.statusText.tool= "Mode: rectangle"
    # def on_round_rect_click(self):
    #     print("RoundRect button clicked")
    #     ie_globals.current_tool = "round_rect"
    #     ie_globals.statusText.tool= "Mode: rounded rectangle"
    #
    # def on_select_rect_click(self):
    #     print("Select button clicked")
    #     ie_globals.current_tool = "select"
    #     ie_globals.statusText.tool= "Mode: rectangle select"
    # def on_circle_click(self):
    #     print("Circle button clicked")
    #     ie_globals.current_tool = "circle"
    #     ie_globals.statusText.tool= "Mode: circle select"
    # def on_spray_click(self):
    #     print("Spray button clicked")
    #     ie_globals.current_tool = "spray"
    #     ie_globals.statusText.tool= "Mode: spray"
    # @staticmethod
    # def on_fill_click():
    #     print("Fill button clicked")
    #     ie_globals.current_tool = "fill"
    # @staticmethod
    # def on_eraser_click():
    #     print("Eraser button clicked")
    #     ie_globals.current_tool = "eraser"
    # def on_wand_click(self):
    #     ie_globals.current_tool = "wand"
    # def on_dropper_click(self):
    #     ie_globals.previous_tool = ie_globals.current_tool
    #     ie_globals.current_tool = "dropper"
    #     ie_globals.statusText.tool= "Mode: dropper"


    def open_file(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", os.getcwd(), "Image Files (*.png *.jpg *.jpeg *.gif)")
        if filename:
            import ie_editor
            doc = ie_editor.Editor("Picture" + str(ie_globals.filenamecounter))
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
        dock_area = self.dockWidgetArea(self.dwColorBox)
        #PyQt6
        if dock_area in (Qt.DockWidgetArea.LeftDockWidgetArea, Qt.DockWidgetArea.RightDockWidgetArea):
            vertical_layout = True
        else:
            vertical_layout = False
        #PySide6
        # if dock_area in (Qt.LeftDockWidgetArea, Qt.RightDockWidgetArea):
        #     vertical_layout = True
        # else:
        #     vertical_layout = False

        #vertical_layout = True
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



    def colorbox_on_click(self, event:QMouseEvent):
        img= self.widgetColors.grab()
        color= img.toImage().pixel(event.pos())
       

        ie_globals.current_pen.setColor(color)
        ie_globals.current_brush.setColor(color)
        ie_globals.pen_color = color
        ie_globals.brush_color = color



# #ff8899 PAINT EVENT
    def paintEvent(self, event):
        ie_globals.statusText.tool= "Tool: "+ str(ie_globals.current_tool.name)
        self.statusLabel.setText("  "+ str(ie_globals.statusText.tool) +" "+ str(ie_globals.statusText.pos))
        float_window.repaint()
        painter = QPainter(self)
        # PySide6
        #painter.setRenderHint(QPainter.Antialiasing)
        # PyQt6
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(QPen(QColor(80, 80, 80), 1))
        #painter.setBrush(QBrush(QColor(180, 180, 180)))
        painter.setBrush(ie_globals.current_pen.color())
        painter.drawRoundedRect(self.rect().right()-100, 5, 20, 20, 2, 2)
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
        self.moveEvent= self.moveEvent
        

    def moveEvent(self, event):
        self.repaint()
        #to update the position of the float window

    def close_event(self, event):
        
        float_window.close()
        float_window.deleteLater()
            # Call the base class implementation to ensure proper cleanup
        super(MainWindow, self).closeEvent(event)
    def setSvgColors(self):
        # Set the color of the SVG icons in the toolbar
        #app.setPalette(PySide6.QtGui.QPalette(QColor("#FFFFFF")))# Dark Mode Linux
        if app.palette().color(PySide6.QtGui.QPalette.ColorRole.Window).value() > QColor("#808080").value():
            themename="ie_light"
            themefolder="lightsvg"
        else:
            themename="ie_dark"
            themefolder="darksvg"
            
        
        print(len(self.dwTools.children()))
        for obj in self.dwTools.children():
            print("T1: ", obj.objectName())
            if isinstance(obj, QtWidgets.QToolButton):
                icon = QIcon()
                iconname= obj.objectName().replace("toolButton","").lower()
                icon.addFile((u":/"+themefolder+"/resources/themes/"+themename+"/" +iconname+".svg"), QSize(), QIcon.Mode.Normal, QIcon.State.Off)
                obj.setIcon(icon)                
            for obj1 in obj.children():
                print("T2:", obj1.objectName())
                if isinstance(obj1, QtWidgets.QToolButton):
                    icon = QIcon()
                    iconname= obj1.objectName().replace("toolButton","").lower()
                    icon.addFile((u":/"+themefolder+"/resources/themes/"+themename+"/" +iconname+".svg"), QSize(), QIcon.Mode.Normal, QIcon.State.Off)
                    obj1.setIcon(icon)
                    
                for obj2 in obj1.children():
                    print("T3:", obj2.objectName(),type(obj2))
                    if isinstance(obj2, QtWidgets.QToolButton):
                        icon = QIcon()
                        iconname= obj2.objectName().replace("toolButton","").lower()
                        icon.addFile(u":/"+themefolder+"/resources/themes/"+themename+"/" +iconname+".svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
                        obj2.setIcon(icon) 
                        

            #if isinstance(obj, QtWidgets.QToolButton):
                btn= obj
                #btn.setStyleSheet("background-color: " + color.name() + ";")
                
                #print("SVG icon:",self.resource_path("resources/icons/" + obj.objectName() + ".svg"))
                #obj.setIconSize(QSize(24, 24))

class FloatWindow(QtWidgets.QMainWindow,float_window_ui):
    def __init__(self):
        QMainWindow.__init__(self)
    
        self.ui = Ui_MainWindow()
        self.setupUi(self)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint |Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.SubWindow| Qt.WindowType.MSWindowsFixedSizeDialogHint|Qt.WindowType.WindowDoesNotAcceptFocus)
        #self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.paintEvent= self.paintEvent
        self.enabled=False

        self.moveEvent= self.moveEvent
    def paintEvent(self,event):
        painter = QPainter(self)
        #PySide6
        #painter.setRenderHint(QPainter.Antialiasing)
        #PyQt6
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(QPen(QColor(80, 80, 80), 1))
        painter.setBrush(QBrush(QColor(180, 180, 180)))
        
        painter.drawRoundedRect(5,5,self.width()-10, self.height()-10, 5, 5)
        painter.setBrush(ie_globals.current_pen.color())
        painter.drawRoundedRect(10,10, 20,20, 2, 2)
    
   


if __name__ == "__main__":
    #Bu kısımda değişiklik yapılırsa çizimler kötüleşiyor. DPI ile alakalı (windows)
    os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "0"
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    os.environ["QT_SCALE_FACTOR"] = "1"
    
    app = QApplication(sys.argv)
    app.setApplicationName("HC Image Editor")
    app.setOrganizationName("HC")
    app.setApplicationDisplayName("HC Image Editor")
    app.setApplicationVersion("2.9.2")
    #PySide6
    #app.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling)
    #app.setAttribute( Qt.ApplicationAttribute.AA_UseHighDpiPixmaps)
    #PyQt6
    app.setAttribute(Qt.ApplicationAttribute.AA_Use96Dpi)
    print(QtWidgets.QStyleFactory.keys()) # Mescut stilleri yazdırıyor galiba
    #['Breeze', 'Oxygen', 'QtCurve', 'Windows', 'Fusion']
    #app.setStyle("Qxygen") #QT Style
    app.setStyle("Breeze")
    
    #app.setPalette(PySide6.QtGui.QPalette(QColor("#FFFFFF")))# Dark Mode Linux
    #QIcon.setThemeName( "ie_light");
    window = MainWindow()
    app.paletteChanged.connect(window.setSvgColors)
    window.show()
    float_window= FloatWindow()
    float_window.enabled=False
    if float_window.enabled:
        float_window.show()
    sys.exit(app.exec())
