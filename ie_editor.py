import math
import time

import PySide6
from PySide6 import QtCore, QtGui
from PySide6.QtCore import QPoint, QPointF, Qt, QRect
from PySide6.QtGui import QPen, QColor, QBrush, QImage, QPainter, QMouseEvent, QPixmap, QPaintEvent
from PySide6.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QSizePolicy, QWidget, QDialog, QVBoxLayout, \
    QLabel, QSlider, QPushButton
import ie_tools
import draw_window_ui
import ie_globals
from ie_functions import melt_image, shear_image, blur_image, mosaic_image


class BrushSettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Brush Settings")
        layout = QVBoxLayout(self)

        # Brush Size
        self.size_label = QLabel(f"Brush Size: {ie_globals.brush_size}")
        layout.addWidget(self.size_label)
        self.size_slider = QSlider(Qt.Orientation.Horizontal)
        self.size_slider.setRange(10, 300)
        self.size_slider.setValue(ie_globals.brush_size)
        self.size_slider.valueChanged.connect(self.update_brush_size)
        layout.addWidget(self.size_slider)

        # Brush Hardness
        self.hardness_label = QLabel(f"Brush Hardness: {ie_globals.brush_hardness}")
        layout.addWidget(self.hardness_label)
        self.hardness_slider = QSlider(Qt.Orientation.Horizontal)
        self.hardness_slider.setRange(0, 100)
        self.hardness_slider.setValue(ie_globals.brush_hardness)
        self.hardness_slider.valueChanged.connect(self.update_brush_hardness)
        layout.addWidget(self.hardness_slider)

        # OK Button
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)
        layout.addWidget(self.ok_button)

    def update_brush_size(self, value):
        ie_globals.brush_size = value
        ie_globals.current_pen.setWidth(value)
        self.size_label.setText(f"Brush Size: {value}")
        ie_globals.save_settings()

    def update_brush_hardness(self, value):
        ie_globals.brush_hardness = value
        self.hardness_label.setText(f"Brush Hardness: {value}")
        ie_globals.save_settings()


class Editor(draw_window_ui.Ui_Form, QWidget):
    def __init__(self, image_path: str, /) -> None:
        super().__init__()

        self.setupUi(self)  # Ensure the UI is set up
        self.image_path = image_path
        '''
        The file path of the image loaded into this editor tab.
        '''
        # You can add more initialization code here
        self.is_checkerboard_enabled = True
        '''
        A boolean flag indicating whether the checkerboard background is currently enabled for this editor.
        '''
        w = ie_globals.image_width
        h = ie_globals.image_height

        self.widgetPicture1.setFixedSize(w, h)
        self.widgetPicture1.setStyleSheet(u"background-image: url(:/png/resources/images/checker20.png);")

        self.pic2 = QImage(w, h, QImage.Format.Format_RGBA64)
        '''
        A temporary QImage used for drawing operations, often to store the image state before a temporary drawing action.
        '''
        self.picOrg = QImage(w, h, QImage.Format.Format_RGBA64)
        '''
        The original or current state of the image being edited. All permanent drawing operations are applied to this image.
        '''
        self.widgetPicture1.setMouseTracking(True)
        self.widgetPicture1.mousePressEvent = self.pic1_mousePressEvent
        self.widgetPicture1.mouseMoveEvent = self.pic1_mouseMoveEvent
        self.widgetPicture1.mouseReleaseEvent = self.pic1_mouseReleaseEvent
        self.widgetPicture1.paintEvent = self.pic1_paintEvent
        self.widgetPicture1.wheelEvent = self.pic1_mouseWheelEvent  # type: ignore
        # self.widgetPicture1.setFixedSize(400, 300)
        self.widgetPicture1.show()

        self.startPos = QPoint(0, 0)
        '''
        The starting position of a mouse press event, used for drawing tools and panning.
        '''
        self.lastPos = QPoint(0, 0)
        '''
        The last recorded position of the mouse, used for continuous drawing.
        '''
        self.docStartPos = QPoint(0, 0)
        '''
        The starting position of the document (widgetPicture1) during a panning operation.
        '''
        self.zoomFactor = 1.0
        '''
        The current zoom level of the image displayed in this editor. 1.0 means actual size.
        '''

        layerbg: ie_globals.Layer = ie_globals.Layer("Background", visible=True, opacity=100,
                                                     image=QImage(w, h, QImage.Format.Format_RGBA64), rasterized=True,
                                                     locked=False)
        self.layers: list = []
        '''
        A list containing all `ie_globals.Layer` objects for this editor document.
        '''
        layerbg.active = True
        layerbg.id = time.time_ns()  # create unique identifier
        print(layerbg.id)
        self.layers.append(layerbg)
        self.currentLayerId: int = layerbg.id  #Layer index of current layer , change when active layer changed
        '''
        The unique identifier (ID) of the currently active layer.
        '''

        self.panning = False
        '''
        A boolean flag indicating whether the user is currently panning the canvas.
        '''
        self.previous_tool = ie_globals.ie_tool_pen
        '''
        Stores the tool that was active before the current one, useful for temporary tool switches (e.g., eyedropper).
        '''

        #undo/redo variables
        self.undoList: list = []  # list of images for each undo operation
        '''
        A list of QImage copies representing the historical states of the `picOrg` for undo operations.
        '''
        self.undoLayerList: list = []  # list of layer numbers for each undo operation
        '''
        A list storing the layer ID associated with each image in the `undoList`,
        indicating which layer was modified at that undo step.
        '''
        self.undoIndex = -1  # index of current undo operation
        '''
        The current index in the `undoList` and `undoLayerList`, pointing to the present state of the image.
        '''
        self.appendUndoImage()  # add original image to undo list

    def open_brush_settings(self):
        dialog = BrushSettingsDialog(self)
        dialog.exec()

    ##region mouse wheel [rgba(222, 100, 222,0.1)]
    def pic1_mouseWheelEvent(self, event: QtGui.QWheelEvent) -> None:
        """
        Handles mouse wheel events for zooming in and out of the image.
        It calculates the new zoom factor and adjusts the scroll bar positions
        to keep the mouse-over point centered.

        Args:
            event (QtGui.QWheelEvent): The mouse wheel event.
        """
        # Get scroll bars
        hbar = self.scrollArea.horizontalScrollBar()
        vbar = self.scrollArea.verticalScrollBar()

        # Get viewport position (use integer values for pixel accuracy)
        viewport_pos = event.position()
        viewport_x = int(viewport_pos.x())
        viewport_y = int(viewport_pos.y())

        # Calculate position in image space before zoom
        img_x = (viewport_x + hbar.value()) / self.zoomFactor
        img_y = (viewport_y + vbar.value()) / self.zoomFactor

        # Calculate new zoom factor
        old_zoom = self.zoomFactor
        if event.angleDelta().y() > 0:
            new_zoom = old_zoom * ie_globals.zoomInFactor
        else:
            new_zoom = old_zoom * ie_globals.zoomOutFactor

        # Clamp zoom factor
        new_zoom = max(0.1, min(10.0, new_zoom))

        # Store current scrollbar values before update
        old_hvalue = hbar.value()
        old_vvalue = vbar.value()

        # Update zoom and widget size
        self.zoomFactor = new_zoom
        self.pic1_update()

        # Get the updated widget size
        widget_size = self.widgetPicture1.size()
        viewport_size = self.scrollArea.viewport().size()

        # Calculate maximum scroll values
        max_hscroll = max(0, widget_size.width() - viewport_size.width())
        max_vscroll = max(0, widget_size.height() - viewport_size.height())

        # Calculate new scroll position to keep the same image point under cursor
        new_scroll_x = int(img_x * new_zoom - viewport_x)
        new_scroll_y = int(img_y * new_zoom - viewport_y)

        # Clamp scroll values to valid range
        new_scroll_x = max(0, min(max_hscroll, new_scroll_x))
        new_scroll_y = max(0, min(max_vscroll, new_scroll_y))

        # Apply scroll positions
        hbar.setValue(new_scroll_x)
        vbar.setValue(new_scroll_y)

        # Debug info
        print("\n=== Zoom Debug Info ===")
        print(f"Mouse viewport: ({viewport_x}, {viewport_y})")
        print(f"Image position: ({img_x:.1f}, {img_y:.1f})")
        print(f"Zoom: {old_zoom:.3f} -> {new_zoom:.3f}")
        print(f"Widget size: {widget_size.width()}x{widget_size.height()}")
        print(f"Viewport size: {viewport_size.width()}x{viewport_size.height()}")
        print(f"Max scroll: ({max_hscroll}, {max_vscroll})")
        print(f"Old scroll: ({old_hvalue}, {old_vvalue})")
        print(f"New scroll: ({new_scroll_x}, {new_scroll_y})")

        # Verify position
        final_img_x = (viewport_x + new_scroll_x) / new_zoom
        final_img_y = (viewport_y + new_scroll_y) / new_zoom
        print(f"Final image pos: ({final_img_x:.1f}, {final_img_y:.1f})")
        print(f"Position error: ({abs(final_img_x - img_x):.3f}, {abs(final_img_y - img_y):.3f})")
        print("=== End Debug Info ===\n")

    #endregion

    #region mouse press [rgba(255, 255, 121,0.1)]
    def pic1_mousePressEvent(self, event: QMouseEvent) -> None:
        """
        Handles mouse press events on the image display widget (`widgetPicture1`).
        Initiates drawing actions based on the currently selected tool.

        Args:
            event (QMouseEvent): The mouse press event.
        """
        # print mouse position
        #print  (event.pos())
        # if left mouse button is pressed
        if event.button() == Qt.MouseButton.LeftButton:
            # make drawing flag true
            eventstr = "down"
            self.pic2 = self.picOrg.copy()
            ie_globals.current_brush.setTexture(QPixmap("textures/texture_01.png"))
            # make last point to the point of cursor
            self.lastPos = event.pos()
            self.startPos = event.pos()
            virtualStartPos: QPoint = QPoint(
                math.trunc(self.startPos.x() / self.zoomFactor),
                math.trunc(self.startPos.y() / self.zoomFactor))
            if ie_globals.current_tool == ie_globals.ie_tool_pen:
                ie_tools.draw_line(self.picOrg, virtualStartPos, virtualStartPos, eventstr)
                self.startPos = event.pos()
            elif ie_globals.current_tool == ie_globals.ie_tool_brush:
                ie_tools.draw_brush(self.picOrg, virtualStartPos)
                self.lastPos = event.pos()
            elif ie_globals.current_tool == ie_globals.ie_tool_fill:
                ie_tools.fill(img1=self.picOrg, pt1=virtualStartPos, task="down", tolerance=ie_globals.fill_tolerance)
            elif ie_globals.current_tool == ie_globals.ie_tool_wand:
                ie_tools.select_wand(img1=self.picOrg, pt1=virtualStartPos, task="down")
            elif ie_globals.current_tool == ie_globals.ie_tool_eraser:
                ie_tools.erase(self.picOrg, pt1=virtualStartPos, task="down")
            elif ie_globals.current_tool == ie_globals.ie_tool_dropper:

                ie_globals.current_pen.setColor(self.picOrg.pixelColor(virtualStartPos))
                ie_globals.current_tool = ie_globals.previous_tool

            self.pic1_update()
        elif event.button() == Qt.MouseButton.MiddleButton:
            self.panning = True
            self.startPos = event.globalPos()
            self.docStartPos = self.widgetPicture1.pos()

    #endregion

    #region mouse move [rgba(255, 152, 121,0.1)]
    def pic1_mouseMoveEvent(self, event: QMouseEvent) -> None:
        """
        Handles mouse move events on the image display widget (`widgetPicture1`).
        Performs continuous drawing actions based on the currently selected tool
        or handles panning if the middle mouse button is pressed.

        Args:
            event (QMouseEvent): The mouse move event.
        """
        eventstr: str = "move"

        if event.buttons() == Qt.MouseButton.LeftButton:
            virtualStartPos: QPoint = QPoint(
                math.trunc(self.startPos.x() / self.zoomFactor),
                math.trunc(self.startPos.y() / self.zoomFactor)
            )
            virtualpos: QPoint = QPoint(
                math.trunc(event.pos().x() / self.zoomFactor),
                math.trunc(event.pos().y() / self.zoomFactor)
            )
            ie_globals.statusText.pos = "Mouse Position: " + str(virtualpos.x()) + ", " + str(virtualpos.y())

            if ie_globals.current_tool == ie_globals.ie_tool_pen:
                ie_globals.current_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
                ie_globals.current_pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
                ie_tools.draw_line(self.picOrg, virtualStartPos, virtualpos, eventstr)
                self.startPos = event.pos()
            
            elif ie_globals.current_tool == ie_globals.ie_tool_brush:
                start_point = self.lastPos
                end_point = event.pos()
                
                dist = math.hypot(end_point.x() - start_point.x(), end_point.y() - start_point.y())
                
                size = ie_globals.brush_size
                density = ie_globals.brush_density / 100.0
                
                if density <= 0: density = 0.01
                spacing = size / (density * 10)
                if spacing < 1: spacing = 1
                
                num_steps = max(1, int(dist / spacing))

                # Calculate angle
                angle = 0.0
                if ie_globals.brush_dynamic_angle:
                    dx = end_point.x() - start_point.x()
                    dy = end_point.y() - start_point.y()
                    if dx != 0 or dy != 0:
                        angle = math.degrees(math.atan2(dy, dx))

                for i in range(num_steps):
                    t = i / float(num_steps)
                    x = start_point.x() * (1.0 - t) + end_point.x() * t
                    y = start_point.y() * (1.0 - t) + end_point.y() * t
                    
                    brush_pos = QPoint(int(x), int(y))
                    
                    virtual_brush_pos = QPoint(
                        math.trunc(brush_pos.x() / self.zoomFactor),
                        math.trunc(brush_pos.y() / self.zoomFactor)
                    )
                    
                    ie_tools.draw_brush(self.picOrg, virtual_brush_pos, angle)

            elif ie_globals.current_tool == ie_globals.ie_tool_line:
                self.picOrg = self.pic2.copy()
                ie_tools.draw_line(self.picOrg, virtualStartPos, virtualpos, eventstr)
            elif ie_globals.current_tool == ie_globals.ie_tool_circle:
                self.picOrg = self.pic2.copy()
                ie_tools.draw_circle(self.picOrg, virtualStartPos, virtualpos, eventstr)
            elif ie_globals.current_tool == ie_globals.ie_tool_circle_outline:
                self.picOrg = self.pic2.copy()
                ie_tools.draw_circle_outline(self.picOrg, virtualStartPos, virtualpos, eventstr)
            elif ie_globals.current_tool == ie_globals.ie_tool_rect:
                self.picOrg = self.pic2.copy()
                ie_tools.draw_rect(self.picOrg, virtualStartPos, virtualpos, eventstr)
            elif ie_globals.current_tool == ie_globals.ie_tool_rounded_rect:
                self.picOrg = self.pic2.copy()
                ie_tools.draw_round_rect(self.picOrg, virtualStartPos, virtualpos, eventstr,
                                         corner_radius=ie_globals.round_rect_corner_radius)
            elif ie_globals.current_tool == ie_globals.ie_tool_spray:
                ie_tools.draw_spray(self.picOrg, virtualpos, eventstr)
            elif ie_globals.current_tool == ie_globals.ie_tool_pan:
                pass
            elif ie_globals.current_tool == ie_globals.ie_tool_eraser:
                virtualpos: QPoint = QPoint(
                    math.trunc(event.pos().x() / self.zoomFactor),
                    math.trunc(event.pos().y() / self.zoomFactor)
                )
                ie_tools.erase(self.picOrg, virtualpos, "move")
                pass
            self.lastPos = event.pos()
            # update
            self.pic1_update()

        elif event.buttons() == Qt.MouseButton.MiddleButton and self.panning:
            deltaX = int(event.globalPosition().x() - self.startPos.x())
            deltaY = int(event.globalPosition().y() - self.startPos.y())
            self.scrollArea.verticalScrollBar().setValue(self.scrollArea.verticalScrollBar().value() - deltaY)
            self.scrollArea.horizontalScrollBar().setValue(self.scrollArea.horizontalScrollBar().value() - deltaX)
            self.startPos = event.globalPosition().toPoint()

    #endregion

    #region mouse release [rgba(255, 255, 121,0.1)]
    def pic1_mouseReleaseEvent(self, event: QMouseEvent) -> None:
        """
        Handles mouse release events on the image display widget (`widgetPicture1`).
        Appends the current image state to the undo history after a drawing operation.

        Args:
            event (QMouseEvent): The mouse release event.
        """
        eventstr: str = "up"
        if event.button() == Qt.MouseButton.LeftButton:
            # if self.undo_index < len(self.undoList) - 1:
            #     del self.undoList[self.undo_index + 1:] 

            self.appendUndoImage()
            #print(self.undo_index, len(self.undoList))
        elif event.button() == Qt.MouseButton.MiddleButton:
            self.panning = False

    #endregion
    def appendUndoImage(self) -> None:
        """
        Appends the current state of `picOrg` and the `currentLayerId` to the undo history.
        If the undo list exceeds `ie_globals.max_undo_steps`, the oldest entry is removed.
        """
        # Geri alma listesi maksimum boyuta ulaştıysa, en eskisini sil
        if len(self.undoList) >= ie_globals.max_undo_steps:
            self.undoList.pop(0)
            self.undoLayerList.pop(0)

        self.undoList.append(self.picOrg.copy())
        layerindex = None

        for layer in self.layers:
            if layer.id == self.currentLayerId:
                layerindex = layer.id
                break  # Exit the loop once the layer is found
        if layerindex is None:
            raise ValueError(f"No layer found with id {self.currentLayerId}")

        self.undoLayerList.append(layerindex)
        self.undoIndex = len(self.undoList) - 1
        print("undo index", self.undoIndex, len(self.undoList))

    def undoImage(self) -> None:
        """
        Reverts the image to the previous state in the undo history.
        Decrements `undoIndex` and calls `drawUndoImage` to update the display.
        """

        if self.undoIndex > 0:
            self.undoIndex -= 1
        self.drawUndoImage()
        print("undo index", self.undoIndex, len(self.undoList))

    def redoImage(self) -> None:
        """
        Advances the image to the next state in the undo history (if available).
        Increments `undoIndex` and calls `drawUndoImage` to update the display.
        """

        if self.undoIndex < len(self.undoList) - 1:
            self.undoIndex += 1
        self.drawUndoImage()
        print("undo index", self.undoIndex, len(self.undoList))

    def drawUndoImage(self) -> None:
        """
        Restores the image and active layer to a state from the undo history
        based on the current `undoIndex`.
        """
        if self.undoIndex < 0 or self.undoIndex >= len(self.undoList):
            return

        # 1. Geri alınacak katman ID'sini al
        layer_id_to_restore = self.undoLayerList[self.undoIndex]

        # 2. İlgili katmanı bul ve resmini geri yükle
        found_layer = False
        for layer in self.layers:
            if layer.id == layer_id_to_restore:
                # QImage'i kopyalayarak atama yap
                layer.image = self.undoList[self.undoIndex].copy()
                found_layer = True

                # 3. Eğer geri yüklenen katman aktif katman ise, ana çizim alanını (picOrg) güncelle
                if layer.id == self.currentLayerId:
                    self.picOrg = layer.image
                break

        if not found_layer:
            print(f"Hata: Geri alma işlemi için {layer_id_to_restore} ID'li katman bulunamadı.")
            # Hata durumunda eski davranışa geri dön (çökmeyi önle)
            self.picOrg = self.undoList[self.undoIndex].copy()

        self.pic1_update()

    #region paint [rgba(125, 152, 200,0.1)]
    #picture 1 view update from original image
    def pic1_update(self) -> None:
        """
        Updates the display of `widgetPicture1` by adjusting its size based on the current zoom factor
        and triggering a repaint event. Also updates the global zoom status text.
        """
        ie_globals.statusText.zoom = "Zoom: " + str(self.zoomFactor)
        w = int(self.picOrg.width() * self.zoomFactor)
        h = int(self.picOrg.height() * self.zoomFactor)
        self.widgetPicture1.setFixedSize(w, h)
        self.scrollArea.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        self.scrollArea.update()
        self.widgetPicture1.update()  #call paint event

    # paint event
    def pic1_paintEvent(self, event: QPaintEvent) -> None:
        """
        Handles the paint event for the `widgetPicture1` (the image display area).
        It draws the main image and, if active, overlays the selection outline and bounding box.

        Args:
            event (QPaintEvent): The paint event.
        """
        canvasPainter = QPainter(self.widgetPicture1)

        # 1. Önce ana resmi çiz
        pixmap = QPixmap.fromImage(self.picOrg)
        canvasPainter.drawPixmap(self.widgetPicture1.rect(), pixmap, pixmap.rect())

        # 2. SEÇİMİ GÖSTER - hem kenarları hem de çerçeveyi çiz
        if hasattr(ie_globals, 'has_selection') and ie_globals.has_selection:
            if hasattr(ie_globals, 'selection_edge_pixels') and ie_globals.selection_edge_pixels:

                # ANİMASYONLU RENK - global color listesinden al
                if hasattr(ie_globals, 'selection_colors') and hasattr(ie_globals, 'current_selection_color_index'):
                    current_color = ie_globals.selection_colors[ie_globals.current_selection_color_index]
                else:
                    current_color = QColor(0, 100, 255, 220)  # Varsayılan mavi

                # SEÇİM KENARLARINI ÇİZ - mor noktalar
                edge_pen = QPen(QColor(current_color))  # Yarı saydam mavi
                edge_pen.setWidth(int(2 * self.zoomFactor))
                edge_pen.setStyle(Qt.PenStyle.SolidLine)
                edge_pen.setDashPattern([4, 4])  # 4 pixel çizgi, 4 pixel boşluk

                canvasPainter.setPen(edge_pen)

                for x, y in ie_globals.selection_edge_pixels:
                    # Zoom faktörüne göre pozisyonları ayarla
                    scaled_x = int((x + 0.5) * self.zoomFactor)
                    scaled_y = int((y + 0.5) * self.zoomFactor)
                    canvasPainter.drawPoint(scaled_x, scaled_y)

            # SEÇİM ÇERÇEVESİNİ ÇİZ - kırmızı dikdörtgen
            if hasattr(ie_globals, 'selection_bounds') and ie_globals.selection_bounds:
                frame_pen = QPen(QColor(255, 0, 0, 200))  # Kırmızı çerçeve
                frame_pen.setWidth(2)
                frame_pen.setStyle(Qt.PenStyle.DashLine)
                frame_pen.setDashPattern([4, 4])  # 4 pixel çizgi, 4 pixel boşluk
                canvasPainter.setPen(frame_pen)
                canvasPainter.setBrush(QColor(0, 0, 0, 0))  # İçi boş

                selection_rect = ie_globals.selection_bounds
                scaled_rect = QRect(
                    int(selection_rect.x() * self.zoomFactor),
                    int(selection_rect.y() * self.zoomFactor),
                    int(selection_rect.width() * self.zoomFactor),
                    int(selection_rect.height() * self.zoomFactor)
                )

                canvasPainter.drawRect(scaled_rect)

        canvasPainter.end()
   
    def apply_melt_filter(self):
        """
        Applies a melt effect to the current image using global parameters.
        """
        if self.picOrg is None:
            return

        self.picOrg = melt_image(self.picOrg, amount=ie_globals.melt_amount)
        self.appendUndoImage()
        self.pic1_update()

    def apply_shear_filter(self):
        """
        Applies a shear effect to the current image using global parameters.
        """
        if self.picOrg is None:
            return

        self.picOrg = shear_image(
            self.picOrg,
            amount=ie_globals.shear_amount,
            horizontal=ie_globals.shear_horizontal,
            direction=ie_globals.shear_direction
        )
        self.appendUndoImage()
        self.pic1_update()

    # -------------- Yeni eklenen filtreler --------------
    def apply_blur_filter(self):
        """
        Applies a box blur to the image using global parameters.
        """
        if getattr(self, "picOrg", None) is None:
            return
        
        self.picOrg = blur_image(self.picOrg, radius=ie_globals.blur_radius)
        self.appendUndoImage()
        self.pic1_update()

    def apply_mosaic_filter(self):
        """
        Applies a mosaic/pixelate effect to the image using global parameters.
        """
        if getattr(self, "picOrg", None) is None:
            return

        self.picOrg = mosaic_image(self.picOrg, block_size=ie_globals.mosaic_block_size)
        self.appendUndoImage()
        self.pic1_update()
