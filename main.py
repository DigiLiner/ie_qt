import math
import os
import platform
import sys
from logging import exception
import PySide6
from PySide6.QtCore import Qt
from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import QPoint, QSize, QRect
from PySide6.QtGui import QPen, QColor, QBrush, QImage, QPainter, QMouseEvent, QPixmap,QIcon
import PySide6.QtGui
from PySide6.QtWidgets import (QWidget,QApplication, QMainWindow, QGraphicsScene, QSizePolicy, QLabel, QHBoxLayout,
                               QDialog, QVBoxLayout, QGroupBox, QRadioButton, QSlider, QSpinBox, QDialogButtonBox)
from typing import Type, cast

import ie_globals,ie_editor
from main_ui import Ui_MainWindow
from float_window_ui import Ui_floatWindow as float_window_ui
   

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.colorHeight = None
        '''
        The height of individual color swatches in the color palette.
        '''
        self.colorWidth = None
        '''
        The width of individual color swatches in the color palette.
        '''
        self.colors = None
        '''
        A list of color strings (hex codes) used to populate the color palette.
        '''
        self.ui = Ui_MainWindow()
        '''
        An instance of the UI generated from `main_ui.py`, containing the main window's widgets.
        '''
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
        self.tabWidget.addTab(EditorType(QWidget()), "Picture" + str(ie_globals.filenamecounter))
        self.tabWidget.setCurrentIndex(self.tabWidget.count() - 1)
        ie_globals.filenamecounter += 1
        #action
        self.actionOpen.triggered.connect(self.open_file)
        self.actionSave.triggered.connect(self.save_file)
        self.actionNew.triggered.connect(self.new_file)
        self.actionUndo.triggered.connect(self.undo)
        self.actionRedo.triggered.connect(self.redo)
        self.dwColorBox.dockLocationChanged.connect(self.colorBox)
        self.actionBlur_2.triggered.connect(self.filter_blur)
        self.actionMelt.triggered.connect(self.filter_melt)
        self.actionMosaic.triggered.connect(self.filter_mosaic)
        self.actionShear.triggered.connect(self.filter_shear)

        self.closeEvent = self.close_event

        # Seçim animasyon timer'ı
        self.selection_timer = QtCore.QTimer(self)
        '''
        A QTimer instance used to control the animation of the selection outline.
        '''
        self.selection_timer.timeout.connect(self.animate_selection)
        self.selection_animation_speed = 500  # ms
        '''
        The interval (in milliseconds) at which the selection animation updates.
        '''

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
        self.horizontalSlider_width.valueChanged.connect(self.on_slider_change_width)
        self.horizontalSlider_radius.valueChanged.connect(self.on_slider_change_radius)
        self.horizontalSlider_density.valueChanged.connect(self.on_slider_change_density)
        self.horizontalSlider_softness.valueChanged.connect(self.on_slider_change_softness)
        self.horizontalSlider_opacity.valueChanged.connect(self.on_slider_change_opacity)
        self.horizontalSlider_tolerance.valueChanged.connect(self.on_slider_change_tolerance)

        #sliders
        self.disable_slider_events=False # Disable slider events while updating them to avoid infinite loop
        '''
        A boolean flag to temporarily disable slider `valueChanged` events.
        This is used to prevent infinite loops when programmatically setting slider values.
        '''
        self.set_slider_values()

        

        ie_globals.current_tool = ie_globals.ie_tool_pen

        self.statusLabel= QLabel(self.statusbar)
        '''
        A QLabel widget displayed in the status bar to show current tool, mouse position, and zoom level.
        '''
        self.statusLabel.setMinimumSize(500, 20)
        self.colorBox()
        #set a timer update periodically
        self.timer = QtCore.QTimer(self)
        '''
        A QTimer instance used for periodic updates of the application's status and UI.
        '''
        self.timer.timeout.connect(self.timer_update)
        #refresh every 200ms , status update , repaint etc.
        self.timer.start(200)

        # self.toolButtonEraser = QToolButton(self.gridLayoutWidget)
    #     self.toolButtonEraser.setObjectName(u"toolButtonEraser")
    def animate_selection(self):
        """
        Animates the selection outline by cycling through predefined colors.
        This method is connected to a QTimer and updates the color index,
        then triggers a repaint for all active editor tabs.
        """
        if ie_globals.has_selection:
            ie_globals.current_selection_color_index = (
                (ie_globals.current_selection_color_index + 1) % 
                len(ie_globals.selection_colors)
            )
            # Tüm açık editor tab'larını güncelle
            for i in range(self.tabWidget.count()):
                widget = self.tabWidget.widget(i)
                if hasattr(widget, 'update'):
                    widget.update()

    def start_selection_animation(self):
        """
        Starts the QTimer responsible for animating the selection outline.
        The animation will only start if the timer is not already active.
        """
        if not self.selection_timer.isActive():
            self.selection_timer.start(self.selection_animation_speed)

    def stop_selection_animation(self):
        """
        Stops the QTimer responsible for animating the selection outline.
        The animation will only stop if the timer is currently active.
        """
        if self.selection_timer.isActive():
            self.selection_timer.stop()   

        

    # Seçim yapıldığında bu fonksiyonu çağır
    def on_selection_created(self):
        """
        Callback function triggered when a new selection is created.
        It initiates the selection animation.
        """
        self.start_selection_animation()        
      
    def set_slider_values(self):
        """
        Sets the initial values and ranges for the various sliders in the UI.
        It temporarily disables slider events to prevent unintended triggers during initialization.
        """
        self.disable_slider_events = True # Disable slider events while updating them to avoid infinite loop
        self.horizontalSlider_width.setMinimum(1)
        self.horizontalSlider_width.setMaximum(100)
        self.horizontalSlider_width.setValue(ie_globals.current_pen.width())
        self.horizontalSlider_radius.setMinimum(1)
        self.horizontalSlider_radius.setMaximum(100)
        self.horizontalSlider_radius.setValue(ie_globals.spray_radius)
        self.horizontalSlider_density.setMinimum(1)
        self.horizontalSlider_density.setMaximum(100)
        self.horizontalSlider_density.setValue(ie_globals.spray_density)
        #todo change
        self.horizontalSlider_softness.setMinimum(0) # Hardness - Opposite of Blur
        self.horizontalSlider_softness.setMaximum(100)
        self.horizontalSlider_softness.setValue(50)
        
        self.horizontalSlider_opacity.setMinimum(0)#opacity
        self.horizontalSlider_opacity.setMaximum(100)
        self.horizontalSlider_opacity.setValue(ie_globals.current_pen.color().alpha()*100) 
        self.horizontalSlider_tolerance.setMinimum(0)
        self.horizontalSlider_tolerance.setMaximum(255)
        self.horizontalSlider_tolerance.setValue(int(ie_globals.fill_tolerance*255))
        self.disable_slider_events = False
        self.toolBar.setIconSize(QtCore.QSize(24, 24))

    def resource_path(self, relative_path):
        """
        Determines the correct path for resources, especially when the application is bundled
        as an executable (e.g., with PyInstaller).

        Args:
            relative_path (str): The path to the resource relative to the application's base directory.

        Returns:
            str: The absolute path to the resource.
        """
        try:
            if hasattr(sys, '_MEIPASS'):
                base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
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
        """
        Sets up mouse tracking and click events for a given QToolButton.

        Args:
            tool_button (QtWidgets.QToolButton): The tool button to configure.
        """
        tool_button.setMouseTracking(True)
        tool_button.setTabletTracking(True)
        tool_button.mouseMoveEvent = lambda e: self.on_tool_button_move(e, tool_button)
        tool_button.mousePressEvent =lambda e:self.on_tool_button_click(tool_button)
        #print("Tool button text:", tool_button.objectName())


    def on_tool_button_move(self, event,tool_button:QtWidgets.QToolButton):
        """
        Handles mouse move events over tool buttons.
        Currently, it primarily prevents actions if slider events are disabled.

        Args:
            event (QMouseEvent): The mouse move event.
            tool_button (QtWidgets.QToolButton): The tool button that triggered the event.
        """
        if self.disable_slider_events:
            return
        #print("Tool button text:", tool_button.objectName())
    def set_tool_button_uncheck(self, tool_button: QtWidgets.QToolButton):
        """
        Unchecks and resets the style of the previously active tool button,
        and sets the style for the newly active one.

        Args:
            tool_button (QtWidgets.QToolButton): The tool button that is currently being activated.
        """
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
    '''
    Stores a reference to the previously clicked QToolButton.
    Used to manage the checked state and styling of tool buttons.
    '''

    def on_tool_button_click(self, tool_button:QtWidgets.QToolButton):
        """
        Handles the click event for tool buttons.
        It sets the `ie_globals.current_tool` based on the clicked button
        and updates the status text. It also handles specific tool actions
        like clearing selection, zooming, flipping, and enabling checkerboard.

        Args:
            tool_button (QtWidgets.QToolButton): The tool button that was clicked.
        """
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
            ctool=ie_globals.ie_tool_select_rect
        elif tool_button.objectName() == "toolButtonCircle":
            ctool=ie_globals.ie_tool_circle
        elif tool_button.objectName() == "toolButtonCircleOutline":
            ctool=ie_globals.ie_tool_circle_outline
        elif tool_button.objectName() == "toolButtonSpray":
            ctool=ie_globals.ie_tool_spray
        elif tool_button.objectName() == "toolButtonFill":
            ctool=ie_globals.ie_tool_fill
        elif tool_button.objectName() == "toolButtonEraser":
            ctool=ie_globals.ie_tool_eraser
        elif tool_button.objectName() == "toolButtonWand":
            ctool=ie_globals.ie_tool_wand
        elif tool_button.objectName() == "toolButtonClearSelection":
            self.clear_selection()
            ie_globals.statusText.tool = "Seçim temizlendi"            
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
            from typing import cast

            if isinstance(self.tabWidget.currentWidget(), ie_editor.Editor):
                activeDoc = cast(ie_editor.Editor, self.tabWidget.currentWidget())
                activeDoc.is_checkerboard_enabled = not activeDoc.is_checkerboard_enabled
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

        # Yeni seçilen araç damlalık değilse, mevcut aracı "önceki araç" olarak kaydet
        if ctool != ie_globals.ie_tool_dropper:
            if ie_globals.current_tool != ie_globals.ie_tool_dropper:
                 ie_globals.previous_tool = ie_globals.current_tool
        
        ie_globals.current_tool = ctool
        ie_globals.statusText.tool = "Mode: " + ctool.name
        tool_button.setCheckable(True)
        tool_button.setChecked(True)
    def clear_selection(self):
        """
        Clears the current selection, resetting all selection-related global variables
        and stopping any active selection animation.
        """
        ie_globals.current_selection = set()
        ie_globals.selection_bounds = QRect()
        ie_globals.selection_edge_pixels = set()
        ie_globals.has_selection = False
        ie_globals.current_selection_color_index = 0  # Reset color
        ie_globals.selection_animation_active = False  # ANİMASYONU DURDUR
        # Animasyonu durdur
        self.stop_selection_animation()
    
        # Aktif editor'ü güncelle
        import ie_editor
        current_widget = self.tabWidget.currentWidget()
        if isinstance(current_widget, ie_editor.Editor):
            current_widget.update()

    # ESC tuşu ile seçimi temizleme
    def keyPressEvent(self, event):
        """
        Handles key press events for the main window.
        Specifically, it clears the current selection if the Escape key is pressed and a selection exists.

        Args:
            event (QKeyEvent): The key press event.
        """
        if event.key() ==  Qt.Key.Key_Escape and ie_globals.has_selection:
            self.clear_selection()
            print("🗑️ Seçim temizlendi")
        super().keyPressEvent(event)

    def timer_update(self):
        """
        Periodically updates the application's UI elements, such as the status bar,
        and manages the position and visibility of the float window.
        It also handles the selection animation update if active.
        """
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
            # SEÇİM ANİMASYON KONTROLÜ - Global değişkeni izle
                if hasattr(ie_globals, 'selection_animation_active') and ie_globals.selection_animation_active:
                    if ie_globals.has_selection:
                        # Renk index'ini güncelle
                        ie_globals.current_selection_color_index = (
                            (ie_globals.current_selection_color_index + 1) % 
                            len(ie_globals.selection_colors)
                        )
                        
                        # Aktif editor'ü güncelle
                        current_widget = self.tabWidget.currentWidget()
                        if current_widget and hasattr(current_widget, 'update'):
                            current_widget.update()
                        import ie_editor
                        if isinstance(self.tabWidget.currentWidget(), ie_editor.Editor):
                            activeDoc = cast(ie_editor.Editor, self.tabWidget.currentWidget())
                            activeDoc.pic1_update()
                            self.repaint()
                    else:
                        # Seçim yoksa animasyonu durdur
                        ie_globals.selection_animation_active = False

            except AttributeError as e:
                print(f"An error occurred while setting the geometry of the float window: {e}")



        self.statusLabel.setText(ie_globals.statusText.tool + " Pos: " + str(ie_globals.statusText.pos) + " Zoom: " + str(ie_globals.statusText.zoom))
        self.repaint()

    def on_slider_change_width(self, value):
        """
        Handles the value change of horizontalSlider_1.
        Updates the global pen width if slider events are not disabled.

        Args:
            value (int): The new value of the slider.
        """
        if self.disable_slider_events:
            return
        print("Slider 1 value changed to", value)
        ie_globals.current_pen.setWidth(value)
    def on_slider_change_radius(self, value):
        """
        Handles the value change of horizontalSlider_radius.
        Updates the global spray radius if slider events are not disabled.

        Args:
            value (int): The new value of the slider.
        """
        if self.disable_slider_events:
            return
        print("Slider 2 value changed to", value)
        ie_globals.spray_radius = value
    def on_slider_change_density(self, value):
        """
        Handles the value change of horizontalSlider_density.
        Updates the global spray density if slider events are not disabled.

        Args:
            value (int): The new value of the slider.
        """
        if self.disable_slider_events:
            return
        print("Slider 3 value changed to", value)
        ie_globals.spray_density = value

    def on_slider_change_softness(self, value):
        """
        Handles the value change of horizontalSlider_softness.
        Updates the global pen blur if slider events are not disabled.
        Args:
            value (int): The new value of the slider (1-100).
        """

        if self.disable_slider_events:
            return
        ie_globals.pen_blur= value
        self.repaint()
        
    def on_slider_change_opacity(self, value):
        """
        Handles the value change of horizontalSlider_softness.
        Updates the global pen opacity and applies it to the current pen's color.

        Args:
            value (int): The new value of the slider (1-100).
        """
        if self.disable_slider_events:
            return

        # Calculate new alpha value (0-255) from slider value (0-100)
        # Ensure value is not 0 to avoid division by zero, though slider min is 1
        alpha:float= value /100
        tempcolor:QColor=ie_globals.current_pen.color()
        tempcolor.setAlphaF(alpha)
        ie_globals.current_pen.setColor( tempcolor)
        # Set the new alpha to the pen's color
        print("Slider 5 (Pen Opacity) value changed to", alpha)     
        # Repaint the main window to reflect the change in the color indicator
        
        self.repaint()
        
    def on_slider_change_tolerance(self, value):
        """
        Handles the value change of horizontalSlider_tolerance.
        Updates the global fill tolerance if slider events are not disabled.

        Args:
            value (int): The new value of the slider.
        """
        if self.disable_slider_events:
            return
        print("Slider 6 value changed to", value)
        ie_globals.fill_tolerance = value
        print("Fill tolerance set to", ie_globals.fill_tolerance)  
        self.repaint()
    

    def zoom_in(self):
        """
        Increases the zoom level of the currently active editor document.
        """
        import ie_editor       

        if isinstance(self.tabWidget.currentWidget(), ie_editor.Editor):
            activeDoc = cast(ie_editor.Editor, self.tabWidget.currentWidget())

            activeDoc.zoomFactor = activeDoc.zoomFactor * ie_globals.zoomInFactor
            activeDoc.pic1_update()
    def zoom_out(self):
        """
        Decreases the zoom level of the currently active editor document.
        """
        import ie_editor
        if isinstance(self.tabWidget.currentWidget(), ie_editor.Editor):
            activeDoc = cast(ie_editor.Editor, self.tabWidget.currentWidget())
        activeDoc.zoomFactor = activeDoc.zoomFactor * ie_globals.zoomOutFactor
        activeDoc.pic1_update()
    def zoom_reset(self):
        """
        Resets the zoom level of the currently active editor document to 1.0 (actual size).
        """
        import ie_editor
        if isinstance(self.tabWidget.currentWidget(), ie_editor.Editor):
            activeDoc = cast(ie_editor.Editor, self.tabWidget.currentWidget())
        activeDoc.zoomFactor = 1.0
        activeDoc.pic1_update()

    def flipVertical(self):
        """
        Flips the image of the currently active editor document vertically.
        The original image is mirrored, and the change is added to the undo history.
        """
        import ie_editor
        if isinstance(self.tabWidget.currentWidget(), ie_editor.Editor):
            activeDoc = cast(ie_editor.Editor, self.tabWidget.currentWidget())
        activeDoc.picOrg = activeDoc.picOrg.mirrored(False, True)
        activeDoc.appendUndoImage()
        activeDoc.pic1_update()
    def flipHorizontal(self):
        """
        Flips the image of the currently active editor document horizontally.
        The original image is mirrored, and the change is added to the undo history.
        """
        import ie_editor
        if isinstance(self.tabWidget.currentWidget(), ie_editor.Editor):
            activeDoc = cast(ie_editor.Editor, self.tabWidget.currentWidget())
        activeDoc.picOrg = activeDoc.picOrg.mirrored(True, False)
        activeDoc.appendUndoImage()
        activeDoc.pic1_update()
    def rotate(self):
        """
        Placeholder for image rotation functionality.
        """
        
        
        
        pass    

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
        """
        Opens a file dialog to select image files.
        If a file is selected, it creates a new editor tab and loads the image into it.
        """
        dialog = QtWidgets.QFileDialog( self,"Open File",".", "Image Files (*.png *.jpg *.jpeg *.gif)")
        dialog.setFileMode(QtWidgets.QFileDialog.FileMode.ExistingFiles)  # Multiple files
        dialog.setAcceptMode(QtWidgets.QFileDialog.AcceptMode.AcceptOpen)
        
        # Dialog will stay open until user clicks "Open" or "Cancel"
        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            filenames = dialog.selectedFiles()
        filename= filenames[0]  # Get the first selected file
      
        # Process the file here
       
        if filename:
                import ie_editor
                doc = ie_editor.Editor("Picture" + str(ie_globals.filenamecounter))
                self.tabWidget.addTab(doc, "Picture" + str(ie_globals.filenamecounter))
                ie_globals.filenamecounter += 1
                doc.picOrg = PySide6.QtGui.QImage(filename)
                doc.pic1_update()
                #todo : filename will be added to tab name
                self.tabWidget.setCurrentIndex(self.tabWidget.count() - 1)
    def save_file(self):
        """
        Opens a file dialog to save the image from the currently active editor document.
        The image is saved to the selected file path.
        """
        #filename will get from tab name
        import ie_editor
        if isinstance(self.tabWidget.currentWidget(), ie_editor.Editor):
            activeDoc = cast(ie_editor.Editor, self.tabWidget.currentWidget())
            filename, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save File", os.getcwd(), "Image Files (*.png *.jpg *.jpeg *.gif)")
            if filename:
                activeDoc.picOrg.save(filename)
    def new_file(self):
        """
        Opens a dialog to create a new image file with specified dimensions.
        A new editor tab is created for the new image.
        """
       
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
        doc = ie_editor.Editor("Picture" + str(ie_globals.filenamecounter))
        if isinstance(self.tabWidget.currentWidget(), ie_editor.Editor):
            activeDoc = cast(ie_editor.Editor, self.tabWidget.currentWidget())
            self.tabWidget.addTab(doc, "Picture" + str(ie_globals.filenamecounter))
            ie_globals.filenamecounter += 1
            self.tabWidget.setCurrentIndex(self.tabWidget.count()-1)
    def undo(self):
        """
        Performs an undo operation on the currently active editor document,
        reverting to the previous state in the undo history.
        """
        import ie_editor
        print("Undo")
        if isinstance(self.tabWidget.currentWidget(), ie_editor.Editor):
            activeDoc = cast(ie_editor.Editor, self.tabWidget.currentWidget())
        
            activeDoc.undoImage()
    def redo(self):
        """
        Performs a redo operation on the currently active editor document,
        advancing to the next state in the undo history.
        """
        print("Redo")
        import ie_editor
        if isinstance(self.tabWidget.currentWidget(), ie_editor.Editor):
            activeDoc = cast(ie_editor.Editor, self.tabWidget.currentWidget())
            activeDoc.redoImage()

    def _create_slider_dialog(self, title, label, min_val, max_val, initial_val):
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle(title)
        layout = QtWidgets.QVBoxLayout(dialog)

        group = QtWidgets.QGroupBox(label)
        h_layout = QtWidgets.QHBoxLayout()
        
        slider = QtWidgets.QSlider(Qt.Orientation.Horizontal)
        slider.setRange(min_val, max_val)
        slider.setValue(initial_val)
        
        spinbox = QtWidgets.QSpinBox()
        spinbox.setRange(min_val, max_val)
        spinbox.setValue(initial_val)
        
        slider.valueChanged.connect(spinbox.setValue)
        spinbox.valueChanged.connect(slider.setValue)
        
        h_layout.addWidget(slider)
        h_layout.addWidget(spinbox)
        group.setLayout(h_layout)
        layout.addWidget(group)

        button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.StandardButton.Ok | QtWidgets.QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)

        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            return slider.value()
        return None

    def filter_blur(self):
        """
        Applies a blur filter to the currently active editor document.
        """
        activeDoc = self.tabWidget.currentWidget()
        if not isinstance(activeDoc, ie_editor.Editor):
            return

        val = self._create_slider_dialog("Blur Filter", "Radius", 1, 100, ie_globals.blur_radius)
        if val is not None:
            ie_globals.blur_radius = val
            print("Blur filter applied with radius:", val)
            activeDoc.apply_blur_filter()

    def filter_melt(self):
        """
        Applies a melt filter to the currently active editor document.
        """
        activeDoc = self.tabWidget.currentWidget()
        if not isinstance(activeDoc, ie_editor.Editor):
            return
            
        val = self._create_slider_dialog("Melt Filter", "Amount", 1, 100, ie_globals.melt_amount)
        if val is not None:
            ie_globals.melt_amount = val
            print("Melt filter applied with amount:", val)
            activeDoc.apply_melt_filter()

    def filter_mosaic(self):
        """
        Applies a mosaic filter to the currently active editor document.
        """
        activeDoc = self.tabWidget.currentWidget()
        if not isinstance(activeDoc, ie_editor.Editor):
            return

        val = self._create_slider_dialog("Mosaic Filter", "Block Size", 2, 100, ie_globals.mosaic_block_size)
        if val is not None:
            ie_globals.mosaic_block_size = val
            print("Mosaic filter applied with block size:", val)
            activeDoc.apply_mosaic_filter()

    def filter_shear(self):
        """
        Opens a dialog to set shear parameters and then applies the filter.
        """
        import ie_editor
        activeDoc = self.tabWidget.currentWidget()
        if not isinstance(activeDoc, ie_editor.Editor):
            return

        # --- Create Dialog ---
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Shear Filter Options")
        layout = QtWidgets.QVBoxLayout(dialog)

        # Amount Slider
        amount_group = QtWidgets.QGroupBox("Shear Amount")
        amount_layout = QtWidgets.QHBoxLayout()
        slider = QtWidgets.QSlider(Qt.Orientation.Horizontal)
        slider.setRange(1, 200)
        slider.setValue(ie_globals.shear_amount)
        spinbox = QtWidgets.QSpinBox()
        spinbox.setRange(1, 200)
        spinbox.setValue(ie_globals.shear_amount)
        slider.valueChanged.connect(spinbox.setValue)
        spinbox.valueChanged.connect(slider.setValue)
        amount_layout.addWidget(slider)
        amount_layout.addWidget(spinbox)
        amount_group.setLayout(amount_layout)
        layout.addWidget(amount_group)

        # Orientation Radios
        orientation_group = QtWidgets.QGroupBox("Orientation")
        orientation_layout = QtWidgets.QHBoxLayout()
        rb_horiz = QtWidgets.QRadioButton("Horizontal")
        rb_vert = QtWidgets.QRadioButton("Vertical")
        if ie_globals.shear_horizontal:
            rb_horiz.setChecked(True)
        else:
            rb_vert.setChecked(True)
        orientation_layout.addWidget(rb_horiz)
        orientation_layout.addWidget(rb_vert)
        orientation_group.setLayout(orientation_layout)
        layout.addWidget(orientation_group)

        # Direction Radios
        direction_group = QtWidgets.QGroupBox("Direction")
        direction_layout = QtWidgets.QHBoxLayout()
        rb_pos = QtWidgets.QRadioButton("Right / Down")
        rb_neg = QtWidgets.QRadioButton("Left / Up")
        if ie_globals.shear_direction == 1:
            rb_pos.setChecked(True)
        else:
            rb_neg.setChecked(True)
        direction_layout.addWidget(rb_pos)
        direction_layout.addWidget(rb_neg)
        direction_group.setLayout(direction_layout)
        layout.addWidget(direction_group)

        # OK/Cancel Buttons
        button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.StandardButton.Ok | QtWidgets.QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)

        # --- Show Dialog and Get Result ---
        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            # Update globals
            ie_globals.shear_amount = slider.value()
            ie_globals.shear_horizontal = rb_horiz.isChecked()
            ie_globals.shear_direction = 1 if rb_pos.isChecked() else -1

            # Apply filter
            print("Shear filter applied with custom settings")
            activeDoc.apply_shear_filter()


    def colorBox(self):
        """
        Configures and displays the color palette in the `dwColorBox` dock widget.
        It dynamically adjusts the layout (rows/columns) and size of color swatches
        based on the dock widget's orientation (vertical or horizontal).
        """
        # Renk paletini ve boyutlarını ayarlar
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

        # 1. Yerleşime göre boyutları belirle
        dock_area = self.dockWidgetArea(self.dwColorBox)
        is_vertical = dock_area in (Qt.DockWidgetArea.LeftDockWidgetArea, Qt.DockWidgetArea.RightDockWidgetArea)

        if is_vertical:
            rows, columns = 12, 4
            self.colorWidth, self.colorHeight = 20, 15
        else:
            rows, columns = 4, 12
            self.colorWidth, self.colorHeight = 20, 20

        total_width = columns * self.colorWidth
        total_height = rows * self.colorHeight

        # 2. Sahneyi oluştur ve boyutunu içeriğe göre ayarla
        colorscene = QGraphicsScene()
        colorscene.setSceneRect(0, 0, total_width, total_height)

        # 3. Renk kutucuklarını sahneye ekle
        for row in range(rows):
            for col in range(columns):
                color_str = self.colors[row * columns + col] if is_vertical else self.colors[col * rows + row]
                
                if len(color_str) == 9:
                    color = QColor(color_str)
                else:
                    color = QColor(color_str)
                    color.setAlpha(255)

                pen = QPen(QColor(120, 120, 120), 1)
                color_item = QtWidgets.QGraphicsRectItem(
                    QtCore.QRectF(col * self.colorWidth, row * self.colorHeight, self.colorWidth, self.colorHeight)
                )
                color_item.setPen(pen)
                color_item.setBrush(QBrush(color))
                colorscene.addItem(color_item)

        # 4. QGraphicsView'i (widgetColors) ayarla
        view = self.widgetColors
        view.setScene(colorscene)
        
        # Kaydırma çubuklarını kapat
        view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        # Boyutunu içeriğe tam uyacak şekilde sabitle (çerçeve için 2px pay)
        view.setFixedSize(total_width + 2, total_height + 2)
        
        
        # Dock'un kendisini içeriğe uyacak şekilde ayarla
        self.dwColorBox.adjustSize()



    def colorbox_on_click(self, event:QMouseEvent):
        """
        Handles click events on the color palette.
        When a color swatch is clicked, it sets the global current pen and brush colors.

        Args:
            event (QMouseEvent): The mouse event that occurred.
        """
        img= self.widgetColors.grab()
        color= img.toImage().pixel(event.pos())
    
       

        ie_globals.current_pen.setColor(color)
        ie_globals.current_brush.setColor(color)
        ie_globals.brush_color = color



    def paintEvent(self, event):
        """
        Handles the paint event for the main window.
        Updates the status bar text and repaints the float window.
        Also draws a small color indicator in the top-right corner.

        Args:
            event (QPaintEvent): The paint event.
        """
        ie_globals.statusText.tool= "Tool: "+ str(ie_globals.current_tool.name)
        self.statusLabel.setText("  "+ str(ie_globals.statusText.tool) +" "+ str(ie_globals.statusText.pos))
        float_window.repaint()
        painter = QPainter(self)
        # PySide6
        #painter.setRenderHint(QPainter.Antialiasing)
        # PyQt6
   
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
        """
        Handles the move event for the main window.
        Triggers a repaint to update the UI and ensures the float window's position is updated.

        Args:
            event (QMoveEvent): The move event.
        """
        self.repaint()
        #to update the position of the float window

    def close_event(self, event):
        """
        Handles the close event for the main window.
        Ensures the float window is properly closed and cleaned up before the main window closes.

        Args:
            event (QCloseEvent): The close event.
        """
        
        float_window.close()
        float_window.deleteLater()
            # Call the base class implementation to ensure proper cleanup
        super(MainWindow, self).closeEvent(event)
    def setSvgColors(self):
        """
        Sets the color of SVG icons in the toolbar based on the application's current theme (light or dark).
        It iterates through tool buttons in the `dwTools` dock widget and applies the appropriate SVG icon.
        """
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
    '''
    A small, frameless, always-on-top window used to display auxiliary information,
    such as the current pen color.
    '''
    def __init__(self):
        QMainWindow.__init__(self)
    
        self.ui = Ui_MainWindow()
        self.setupUi(self)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint |Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.SubWindow| Qt.WindowType.MSWindowsFixedSizeDialogHint|Qt.WindowType.WindowDoesNotAcceptFocus)
        #self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.paintEvent= self.paintEvent
        self.enabled=False
        '''
        A boolean flag indicating whether the float window is enabled and should be shown.
        '''

        self.moveEvent= self.moveEvent
    def paintEvent(self,event):
        """
        Handles the paint event for the float window.
        Draws a rounded rectangle background and a color indicator representing the current pen color.

        Args:
            event (QPaintEvent): The paint event.
        """
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

    