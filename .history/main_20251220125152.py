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
                               QDialog, QVBoxLayout, QGroupBox, QRadioButton, QSlider, QSpinBox, QDialogButtonBox, QCheckBox, QFileDialog)
from typing import Type, cast

import ie_globals,ie_editor
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

        ie_globals.load_settings()

        print(os.path)

        self.tabWidget.removeTab(0)
        import ie_editor
        EditorType = cast(Type[QWidget], ie_editor.Editor)
        doc: Type[QWidget] = EditorType
        self.tabWidget.addTab(EditorType(QWidget()), "Picture" + str(ie_globals.filenamecounter))
        self.tabWidget.setCurrentIndex(self.tabWidget.count() - 1)
        ie_globals.filenamecounter += 1


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

        self.selection_timer = QtCore.QTimer(self)
        self.selection_timer.timeout.connect(self.animate_selection)
        self.selection_animation_speed = 500

        for obj in self.dockWidgetContents.children():
            if isinstance(obj, QtWidgets.QToolButton):
                self.set_button_events(obj)
            for obj1 in obj.children():
                if isinstance(obj1, QtWidgets.QToolButton):
                    self.set_button_events(obj1)
                for obj2 in [obj1.children()]:
                    if isinstance(obj2, QtWidgets.QToolButton):
                        self.set_button_events(obj2)

        self.setSvgColors()
        self.widgetColors.setMouseTracking(True)
        self.widgetColors.mousePressEvent = self.colorbox_on_click

        self.horizontalSlider_width.valueChanged.connect(self.on_slider_change_width)
        self.horizontalSlider_radius.valueChanged.connect(self.on_slider_change_radius)
        self.horizontalSlider_density.valueChanged.connect(self.on_slider_change_density)
        self.horizontalSlider_softness.valueChanged.connect(self.on_slider_change_softness)
        self.horizontalSlider_opacity.valueChanged.connect(self.on_slider_change_opacity)
        self.horizontalSlider_tolerance.valueChanged.connect(self.on_slider_change_tolerance)

        self.disable_slider_events=False
        self.set_slider_values()

        # Add new brush controls
        self.add_brush_controls()

        ie_globals.current_tool = ie_globals.ie_tool_pen

        self.statusLabel= QLabel(self.statusbar)
        self.statusLabel.setMinimumSize(500, 20)
        self.colorBox()

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.timer_update)
        self.timer.start(200)

    def add_brush_controls(self):
        # Brush Dialog Button
        #self.toolButtonBrushSettings = QtWidgets.QPushButton("Brush Settings...")
        self.toolButtonBrushSettings.clicked.connect(self.open_brush_dialog)
        #self.verticalLayout_Top.addWidget(self.toolButtonBrushSettings)

    def open_brush_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Brush Settings")
        layout = QVBoxLayout(dialog)

        # Brush Shape
        shape_group = QGroupBox("Brush Shape")
        shape_layout = QHBoxLayout()
        self.rb_circle = QRadioButton("Circle")
        self.rb_square = QRadioButton("Square")
        self.rb_star = QRadioButton("Star")
        self.rb_cylinder = QRadioButton("Cylinder")

        shape_map = {
            "circle": self.rb_circle, "square": self.rb_square,
            "star": self.rb_star, "cylinder": self.rb_cylinder
        }
        if str(ie_globals.brush_shape) in shape_map:
            shape_map[str(ie_globals.brush_shape)].setChecked(True)

        self.rb_circle.toggled.connect(lambda: self.set_brush_shape("circle"))
        self.rb_square.toggled.connect(lambda: self.set_brush_shape("square"))
        self.rb_star.toggled.connect(lambda: self.set_brush_shape("star"))
        self.rb_cylinder.toggled.connect(lambda: self.set_brush_shape("cylinder"))

        shape_layout.addWidget(self.rb_circle)
        shape_layout.addWidget(self.rb_square)
        shape_layout.addWidget(self.rb_star)
        shape_layout.addWidget(self.rb_cylinder)
        shape_group.setLayout(shape_layout)
        layout.addWidget(shape_group)

        # Dynamic Angle
        self.cb_dynamic_angle = QCheckBox("Dynamic Angle (Follows Mouse)")
        self.cb_dynamic_angle.setChecked(ie_globals.brush_dynamic_angle)
        self.cb_dynamic_angle.stateChanged.connect(self.set_dynamic_angle)
        layout.addWidget(self.cb_dynamic_angle)

        # Image Brush
        self.btn_load_image_brush = QtWidgets.QPushButton("Load Image Brush")
        self.btn_load_image_brush.clicked.connect(self.load_image_brush)
        layout.addWidget(self.btn_load_image_brush)

        # Dialog Buttons
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        button_box.accepted.connect(dialog.accept)
        layout.addWidget(button_box)

        dialog.exec()

    def set_brush_shape(self, shape):
        ie_globals.brush_shape = shape
        ie_globals.save_settings()

    def set_dynamic_angle(self, state):
        ie_globals.brush_dynamic_angle = (state == Qt.CheckState.Checked.value)
        ie_globals.save_settings()

    def load_image_brush(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open Image for Brush", "", "Image Files (*.png *.jpg *.jpeg)")
        if filename:
            ie_globals.brush_image = QImage(filename)
            ie_globals.brush_mode = "image"
            print(f"Image brush loaded from {filename}")

    def animate_selection(self):
        if ie_globals.has_selection:
            ie_globals.current_selection_color_index = (
                (ie_globals.current_selection_color_index + 1) %
                len(ie_globals.selection_colors)
            )
            for i in range(self.tabWidget.count()):
                widget = self.tabWidget.widget(i)
                if hasattr(widget, 'update'):
                    widget.update()

    def start_selection_animation(self):
        if not self.selection_timer.isActive():
            self.selection_timer.start(self.selection_animation_speed)

    def stop_selection_animation(self):
        if self.selection_timer.isActive():
            self.selection_timer.stop()

    def on_selection_created(self):
        self.start_selection_animation()

    def set_slider_values(self):
        self.disable_slider_events = True
        self.horizontalSlider_width.setMinimum(1)
        self.horizontalSlider_width.setMaximum(300)
        self.horizontalSlider_width.setValue(ie_globals.brush_size)
        self.horizontalSlider_radius.setMinimum(1)
        self.horizontalSlider_radius.setMaximum(100)
        self.horizontalSlider_radius.setValue(ie_globals.spray_radius)
        self.horizontalSlider_density.setMinimum(1)
        self.horizontalSlider_density.setMaximum(100)
        self.horizontalSlider_density.setValue(ie_globals.spray_density)
        self.horizontalSlider_softness.setMinimum(0)
        self.horizontalSlider_softness.setMaximum(100)
        self.horizontalSlider_softness.setValue(50)
        self.horizontalSlider_opacity.setMinimum(0)
        self.horizontalSlider_opacity.setMaximum(100)
        self.horizontalSlider_opacity.setValue(ie_globals.current_pen.color().alpha()*100)
        self.horizontalSlider_tolerance.setMinimum(0)
        self.horizontalSlider_tolerance.setMaximum(255)
        self.horizontalSlider_tolerance.setValue(int(ie_globals.fill_tolerance*255))
        self.disable_slider_events = False
        self.toolBar.setIconSize(QtCore.QSize(24, 24))

    def resource_path(self, relative_path):
        try:
            if hasattr(sys, '_MEIPASS'):
                base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
            else:
                base_path = os.path.abspath(".")
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    def set_button_events(self,tool_button:QtWidgets.QToolButton):
        tool_button.setMouseTracking(True)
        tool_button.setTabletTracking(True)
        tool_button.mouseMoveEvent = lambda e: self.on_tool_button_move(e, tool_button)
        tool_button.mousePressEvent =lambda e:self.on_tool_button_click(tool_button)

    def on_tool_button_move(self, event,tool_button:QtWidgets.QToolButton):
        if self.disable_slider_events:
            return

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
            return

    old_tool_button = None

    def on_tool_button_click(self, tool_button:QtWidgets.QToolButton):
        self.set_tool_button_uncheck(tool_button)

        import ie_editor
        ctool=ie_globals.current_tool
        if tool_button.objectName() == "toolButtonPen":
            ctool=ie_globals.ie_tool_pen
        elif tool_button.objectName() == "toolButtonBrush":
            if ctool == ie_globals.ie_tool_brush:
                active_editor = self.tabWidget.currentWidget()
                if isinstance(active_editor, ie_editor.Editor):
                    active_editor.open_brush_settings()
            ctool=ie_globals.ie_tool_brush
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
        elif tool_button.objectName()=="toolButtonBrushSettings":
            self.open_brush_dialog()

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
            self.widgetPicture1.update()
        elif tool_button.objectName() == "toolButtonCrop":
            ie_globals.previous_tool = ie_globals.current_tool
            ctool = ie_globals.ie_tool_crop
        else:
            exception("Tool button click event not implemented for tool:", ctool)

        if ctool != ie_globals.ie_tool_dropper:
            if ie_globals.current_tool != ie_globals.ie_tool_dropper:
                 ie_globals.previous_tool = ie_globals.current_tool

        ie_globals.current_tool = ctool
        ie_globals.statusText.tool = "Mode: " + ctool.name
        tool_button.setCheckable(True)
        tool_button.setChecked(True)

    def clear_selection(self):
        ie_globals.current_selection = set()
        ie_globals.selection_bounds = QRect()
        ie_globals.selection_edge_pixels = set()
        ie_globals.has_selection = False
        ie_globals.current_selection_color_index = 0
        ie_globals.selection_animation_active = False
        self.stop_selection_animation()

        import ie_editor
        current_widget = self.tabWidget.currentWidget()
        if isinstance(current_widget, ie_editor.Editor):
            current_widget.update()

    def keyPressEvent(self, event):
        if event.key() ==  Qt.Key.Key_Escape and ie_globals.has_selection:
            self.clear_selection()
            print("🗑️ Seçim temizlendi")
        super().keyPressEvent(event)

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
                    float_window.setGeometry(float_geometry)
                    float_window.show()
                if hasattr(ie_globals, 'selection_animation_active') and ie_globals.selection_animation_active:
                    if ie_globals.has_selection:
                        ie_globals.current_selection_color_index = (
                            (ie_globals.current_selection_color_index + 1) %
                            len(ie_globals.selection_colors)
                        )

                        current_widget = self.tabWidget.currentWidget()
                        if current_widget and hasattr(current_widget, 'update'):
                            current_widget.update()
                        import ie_editor
                        if isinstance(self.tabWidget.currentWidget(), ie_editor.Editor):
                            activeDoc = cast(ie_editor.Editor, self.tabWidget.currentWidget())
                            activeDoc.pic1_update()
                            self.repaint()
                    else:
                        ie_globals.selection_animation_active = False

            except AttributeError as e:
                print(f"An error occurred while setting the geometry of the float window: {e}")

        self.statusLabel.setText(ie_globals.statusText.tool + " Pos: " + str(ie_globals.statusText.pos) + " Zoom: " + str(ie_globals.statusText.zoom))
        self.repaint()

    def on_slider_change_width(self, value):
        if self.disable_slider_events: return
        ie_globals.current_pen.setWidth(value)
        ie_globals.brush_size = value
        ie_globals.save_settings()
    def on_slider_change_radius(self, value):
        if self.disable_slider_events: return
        ie_globals.spray_radius = value
        ie_globals.save_settings()
    def on_slider_change_density(self, value):
        if self.disable_slider_events: return
        ie_globals.spray_density = value
        ie_globals.save_settings()
    def on_slider_change_softness(self, value):
        if self.disable_slider_events: return
        ie_globals.pen_blur= value
        self.repaint()
        ie_globals.save_settings()
    def on_slider_change_opacity(self, value):
        if self.disable_slider_events: return
        alpha:float= value /100
        tempcolor:QColor=ie_globals.current_pen.color()
        tempcolor.setAlphaF(alpha)
        ie_globals.current_pen.setColor( tempcolor)
        ie_globals.current_brush.setColor( tempcolor)
        self.repaint()
    def on_slider_change_tolerance(self, value):
        if self.disable_slider_events: return
        ie_globals.fill_tolerance = value
        self.repaint()
        ie_globals.save_settings()
    def on_slider_change_brush_size(self, value):
        if self.disable_slider_events: return
        ie_globals.brush_size = value
        self.repaint()
        ie_globals.save_settings()
    def on_brush_shape_change(self, shape):
        ie_globals.brush_shape = shape
        ie_globals.save_settings()
    def on_brush_mode_change(self, mode):
        ie_globals.brush_mode = mode
        ie_globals.save_settings()
    def on_load_brush_image(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open Brush Image", ".", "Image Files (*.png *.jpg *.jpeg)")
        if filename:
            ie_globals.brush_image = QImage(filename)
            print(f"Brush image loaded from {filename}")
    def on_load_pattern_image(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open Pattern Image", ".", "Image Files (*.png *.jpg *.jpeg)")
        if filename:
            ie_globals.pattern_image = QImage(filename)
            print(f"Pattern image loaded from {filename}")

    def zoom_in(self):
        import ie_editor
        if isinstance(self.tabWidget.currentWidget(), ie_editor.Editor):
            activeDoc = cast(ie_editor.Editor, self.tabWidget.currentWidget())
            activeDoc.zoomFactor = activeDoc.zoomFactor * ie_globals.zoomInFactor
            activeDoc.pic1_update()
    def zoom_out(self):
        import ie_editor
        if isinstance(self.tabWidget.currentWidget(), ie_editor.Editor):
            activeDoc = cast(ie_editor.Editor, self.tabWidget.currentWidget())
            activeDoc.zoomFactor = activeDoc.zoomFactor * ie_globals.zoomOutFactor
            activeDoc.pic1_update()
    def zoom_reset(self):
        import ie_editor
        if isinstance(self.tabWidget.currentWidget(), ie_editor.Editor):
            activeDoc = cast(ie_editor.Editor, self.tabWidget.currentWidget())
            activeDoc.zoomFactor = 1.0
            activeDoc.pic1_update()

    def flipVertical(self):
        import ie_editor
        if isinstance(self.tabWidget.currentWidget(), ie_editor.Editor):
            activeDoc = cast(ie_editor.Editor, self.tabWidget.currentWidget())
            activeDoc.picOrg = activeDoc.picOrg.mirrored(False, True)
            activeDoc.appendUndoImage()
            activeDoc.pic1_update()
    def flipHorizontal(self):
        import ie_editor
        if isinstance(self.tabWidget.currentWidget(), ie_editor.Editor):
            activeDoc = cast(ie_editor.Editor, self.tabWidget.currentWidget())
            activeDoc.picOrg = activeDoc.picOrg.mirrored(True, False)
            activeDoc.appendUndoImage()
            activeDoc.pic1_update()
    def rotate(self):
        pass

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open File", ".", "Image Files (*.png *.jpg *.jpeg *.gif)")
        if filename:
            import ie_editor
            doc = ie_editor.Editor("Picture" + str(ie_globals.filenamecounter))
            self.tabWidget.addTab(doc, "Picture" + str(ie_globals.filenamecounter))
            ie_globals.filenamecounter += 1
            doc.picOrg = PySide6.QtGui.QImage(filename)
            doc.pic1_update()
            self.tabWidget.setCurrentIndex(self.tabWidget.count() - 1)
    def save_file(self):
        import ie_editor
        if isinstance(self.tabWidget.currentWidget(), ie_editor.Editor):
            activeDoc = cast(ie_editor.Editor, self.tabWidget.currentWidget())
            filename, _ = QFileDialog.getSaveFileName(self, "Save File", os.getcwd(), "Image Files (*.png *.jpg *.jpeg *.gif)")
            if filename:
                activeDoc.picOrg.save(filename)
    def new_file(self):
        import dialog_newImage_ui
        dialog = dialog_newImage_ui.Ui_Dialog()
        dialog_instance = QtWidgets.QDialog()
        dialog.setupUi(dialog_instance)
        dialog.comboBoxSizeList.addItems(["100x100", "500x500", "800x600","1024x768","1280x1024","1600x1200","1920,1080","2048x1536"])
        dialog.comboBoxSizeList.setCurrentIndex(3)
        dialog.plainTextEditWidth.setPlainText("500")
        dialog.plainTextEditHeight.setPlainText("500")
        dialog_instance.exec()

        import ie_editor
        EditorType = cast(Type[QWidget], ie_editor.Editor)
        doc = ie_editor.Editor("Picture" + str(ie_globals.filenamecounter))
        if isinstance(self.tabWidget.currentWidget(), ie_editor.Editor):
            activeDoc = cast(ie_editor.Editor, self.tabWidget.currentWidget())
            self.tabWidget.addTab(doc, "Picture" + str(ie_globals.filenamecounter))
            ie_globals.filenamecounter += 1
            self.tabWidget.setCurrentIndex(self.tabWidget.count()-1)
    def undo(self):
        import ie_editor
        if isinstance(self.tabWidget.currentWidget(), ie_editor.Editor):
            activeDoc = cast(ie_editor.Editor, self.tabWidget.currentWidget())
            activeDoc.undoImage()
    def redo(self):
        import ie_editor
        if isinstance(self.tabWidget.currentWidget(), ie_editor.Editor):
            activeDoc = cast(ie_editor.Editor, self.tabWidget.currentWidget())
            activeDoc.redoImage()

    def _create_slider_dialog(self, title, label, min_val, max_val, initial_val):
        dialog = QDialog(self)
        dialog.setWindowTitle(title)
        layout = QVBoxLayout(dialog)
        group = QGroupBox(label)
        h_layout = QHBoxLayout()
        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setRange(min_val, max_val)
        slider.setValue(initial_val)
        spinbox = QSpinBox()
        spinbox.setRange(min_val, max_val)
        spinbox.setValue(initial_val)
        slider.valueChanged.connect(spinbox.setValue)
        spinbox.valueChanged.connect(slider.setValue)
        h_layout.addWidget(slider)
        h_layout.addWidget(spinbox)
        group.setLayout(h_layout)
        layout.addWidget(group)
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            return slider.value()
        return None

    def filter_blur(self):
        activeDoc = self.tabWidget.currentWidget()
        if not isinstance(activeDoc, ie_editor.Editor): return
        val = self._create_slider_dialog("Blur Filter", "Radius", 1, 100, ie_globals.blur_radius)
        if val is not None:
            ie_globals.blur_radius = val
            activeDoc.apply_blur_filter()

    def filter_melt(self):
        activeDoc = self.tabWidget.currentWidget()
        if not isinstance(activeDoc, ie_editor.Editor): return
        val = self._create_slider_dialog("Melt Filter", "Amount", 1, 100, ie_globals.melt_amount)
        if val is not None:
            ie_globals.melt_amount = val
            activeDoc.apply_melt_filter()

    def filter_mosaic(self):
        activeDoc = self.tabWidget.currentWidget()
        if not isinstance(activeDoc, ie_editor.Editor): return
        val = self._create_slider_dialog("Mosaic Filter", "Block Size", 2, 100, ie_globals.mosaic_block_size)
        if val is not None:
            ie_globals.mosaic_block_size = val
            activeDoc.apply_mosaic_filter()

    def filter_shear(self):
        import ie_editor
        activeDoc = self.tabWidget.currentWidget()
        if not isinstance(activeDoc, ie_editor.Editor): return
        dialog = QDialog(self)
        dialog.setWindowTitle("Shear Filter Options")
        layout = QVBoxLayout(dialog)
        amount_group = QGroupBox("Shear Amount")
        amount_layout = QHBoxLayout()
        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setRange(1, 200)
        slider.setValue(ie_globals.shear_amount)
        spinbox = QSpinBox()
        spinbox.setRange(1, 200)
        spinbox.setValue(ie_globals.shear_amount)
        slider.valueChanged.connect(spinbox.setValue)
        spinbox.valueChanged.connect(slider.setValue)
        amount_layout.addWidget(slider)
        amount_layout.addWidget(spinbox)
        amount_group.setLayout(amount_layout)
        layout.addWidget(amount_group)
        orientation_group = QGroupBox("Orientation")
        orientation_layout = QHBoxLayout()
        rb_horiz = QRadioButton("Horizontal")
        rb_vert = QRadioButton("Vertical")
        if ie_globals.shear_horizontal: rb_horiz.setChecked(True)
        else: rb_vert.setChecked(True)
        orientation_layout.addWidget(rb_horiz)
        orientation_layout.addWidget(rb_vert)
        orientation_group.setLayout(orientation_layout)
        layout.addWidget(orientation_group)
        direction_group = QGroupBox("Direction")
        direction_layout = QHBoxLayout()
        rb_pos = QRadioButton("Right / Down")
        rb_neg = QRadioButton("Left / Up")
        if ie_globals.shear_direction == 1: rb_pos.setChecked(True)
        else: rb_neg.setChecked(True)
        direction_layout.addWidget(rb_pos)
        direction_layout.addWidget(rb_neg)
        direction_group.setLayout(direction_layout)
        layout.addWidget(direction_group)
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            ie_globals.shear_amount = slider.value()
            ie_globals.shear_horizontal = rb_horiz.isChecked()
            ie_globals.shear_direction = 1 if rb_pos.isChecked() else -1
            activeDoc.apply_shear_filter()

    def colorBox(self):
        self.colors = [
            "#FFFFFF", "#FFC0C0", "#FFE0C0", "#FFFFC0", "#E0E0E0", "#FF8080", "#FFC080", "#FFFF80",
            "#C0C0C0", "#FF0000", "#FF8000", "#E0E080", "#808080", "#C00000", "#C04000", "#C0C000",
            "#404040", "#800000", "#804000", "#808000", "#000000", "#400000", "#604000", "#404000",
            "#C0FFC0", "#C0FFFF", "#D3D5F5", "#FFC0FF", "#80FF80", "#80FFFF", "#AAAEEB", "#FF80FF",
            "#00FF00", "#00FFFF", "#8389E0", "#FF00FF", "#00C000", "#00C0C0", "#5E61b8", "#C000C0",
            "#008000", "#008080", "#2d3c9c", "#800080", "#004000", "#004040", "#04051A", "#400040",
        ]
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
        colorscene = QGraphicsScene()
        colorscene.setSceneRect(0, 0, total_width, total_height)
        for row in range(rows):
            for col in range(columns):
                color_str = self.colors[row * columns + col] if is_vertical else self.colors[col * rows + row]
                color = QColor(color_str)
                if len(color_str) != 9: color.setAlpha(255)
                pen = QPen(QColor(120, 120, 120), 1)
                color_item = QtWidgets.QGraphicsRectItem(QtCore.QRectF(col * self.colorWidth, row * self.colorHeight, self.colorWidth, self.colorHeight))
                color_item.setPen(pen)
                color_item.setBrush(QBrush(color))
                colorscene.addItem(color_item)
        view = self.widgetColors
        view.setScene(colorscene)
        view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        view.setFixedSize(total_width + 2, total_height + 2)
        self.dwColorBox.adjustSize()

    def colorbox_on_click(self, event:QMouseEvent):
        img= self.widgetColors.grab()
        color= img.toImage().pixel(event.pos())
        ie_globals.previous_tool = ie_globals.current_tool        
        previous_alpha = ie_globals.current_pen.color().alpha()
        qcolor= QColor(color)
        qcolor.setAlpha(previous_alpha)
        ie_globals.current_pen.setColor(qcolor)
        ie_globals.current_brush.setColor(qcolor)     
        ie_globals.current_tool = ie_globals.previous_tool

    def paintEvent(self, event):
        ie_globals.statusText.tool= "Tool: "+ str(ie_globals.current_tool.name)
        self.statusLabel.setText("  "+ str(ie_globals.statusText.tool) +" "+ str(ie_globals.statusText.pos))
        float_window.repaint()
        painter = QPainter(self)
        painter.setPen(QPen(QColor(80, 80, 80), 1))
        painter.setBrush(ie_globals.current_pen.color())
        painter.drawRoundedRect(self.rect().right()-100, 5, 20, 20, 2, 2)
        self.moveEvent= self.moveEvent

    def moveEvent(self, event):
        self.repaint()

    def close_event(self, event):
        float_window.close()
        float_window.deleteLater()
        super(MainWindow, self).closeEvent(event)

    def setSvgColors(self):
        #şimdilik simgeler
        return
        if app.palette().color(PySide6.QtGui.QPalette.ColorRole.Window).value() > QColor("#808080").value():
            themename="ie_light"    
        else:
            themename="ie_dark"
        for obj in self.dwTools.children():
            if isinstance(obj, QtWidgets.QToolButton):
                icon = QIcon()
                iconname= obj.objectName().replace("toolButton","").lower()
                icon_relative_path = os.path.join("resources", "themes", themename, f"{iconname}.svg")
                icon_absolute_path = self.resource_path(icon_relative_path)
                icon.addFile(icon_absolute_path, QSize(), QIcon.Mode.Normal, QIcon.State.Off)
                
                #icon.addFile((u"./resources/themes/"+themename+"/" +iconname+".svg"), QSize(), QIcon.Mode.Normal, QIcon.State.Off)
                obj.setIcon(icon)
            for obj1 in obj.children():
                if isinstance(obj1, QtWidgets.QToolButton):
                    icon = QIcon()
                    iconname= obj1.objectName().replace("toolButton","").lower()
                    icon_relative_path = os.path.join("resources", "themes", themename, f"{iconname}.svg")
                    icon_absolute_path = self.resource_path(icon_relative_path)
                    icon.addFile(icon_absolute_path, QSize(), QIcon.Mode.Normal, QIcon.State.Off)

                    #icon.addFile((u"./resources/themes/"+themename+"/" +iconname+".svg"), QSize(), QIcon.Mode.Normal, QIcon.State.Off)
                    obj1.setIcon(icon)
                for obj2 in obj1.children():
                    if isinstance(obj2, QtWidgets.QToolButton):
                        icon = QIcon()
                        iconname= obj2.objectName().replace("toolButton","").lower()
                        icon_relative_path = os.path.join("resources", "themes", themename, f"{iconname}.svg")
                        icon_absolute_path = self.resource_path(icon_relative_path)
                        icon.addFile(icon_absolute_path, QSize(), QIcon.Mode.Normal, QIcon.State.Off)
                        #icon.addFile(u"./resources/themes/"+themename+"/" +iconname+".svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
                        obj2.setIcon(icon)
        
        for obj in self.menuBar().children():
            if isinstance(obj, QtWidgets.QMenu):
                icon = QIcon()
                iconname= obj.objectName().replace("menu","").lower()
                icon_relative_path = os.path.join("resources", "themes", themename, f"{iconname}.svg")
                icon_absolute_path = self.resource_path(icon_relative_path)
                icon.addFile(icon_absolute_path, QSize(), QIcon.Mode.Normal, QIcon.State.Off)
                #icon.addFile(u"./resources/themes/"+themename+"/" +iconname+".svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
                obj.setIcon(icon)
class FloatWindow(QtWidgets.QMainWindow,float_window_ui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.setupUi(self)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint |Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.SubWindow| Qt.WindowType.MSWindowsFixedSizeDialogHint|Qt.WindowType.WindowDoesNotAcceptFocus)
        self.paintEvent= self.paintEvent
        self.enabled=False
        self.moveEvent= self.moveEvent
    def paintEvent(self,event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(QPen(QColor(80, 80, 80), 1))
        painter.setBrush(QBrush(QColor(180, 180, 180)))
        painter.drawRoundedRect(5,5,self.width()-10, self.height()-10, 5, 5)
        painter.setBrush(ie_globals.current_pen.color())
        painter.drawRoundedRect(10,10, 20,20, 2, 2)

if __name__ == "__main__":
    os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "0"
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    os.environ["QT_SCALE_FACTOR"] = "1"
    app = QApplication(sys.argv)
    app.setApplicationName("HC Image Editor")
    app.setOrganizationName("HC")
    app.setApplicationDisplayName("HC Image Editor")
    app.setApplicationVersion("2.9.3")
    app.setAttribute(Qt.ApplicationAttribute.AA_Use96Dpi)
    app.setStyle("macOS") #"Fusion" "WindowsVista" "Breeze"  "Windows" "macOS"
    window = MainWindow()
    app.paletteChanged.connect(window.setSvgColors)
    window.show()
    float_window= FloatWindow()
    float_window.enabled=False
    if float_window.enabled:
        float_window.show()
    sys.exit(app.exec())
