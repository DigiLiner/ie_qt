import math
import time

from PySide6 import QtGui
from PySide6.QtCore import QPoint, Qt, QRect, QThread, Signal, QPointF, QRectF
from PySide6.QtGui import QPen, QColor, QImage, QPainter, QMouseEvent, QPixmap, QPaintEvent, QPainterPath, QCursor
from PySide6.QtWidgets import QSizePolicy, QWidget, QDialog, QVBoxLayout, \
    QLabel, QSlider, QPushButton
import ie_tools
import draw_window_ui
import ie_globals
import ie_filters
import ie_utils
from ie_functions import melt_image, shear_image, blur_image, gaussian_blur_image, mosaic_image

# AI kütüphaneleri artık başlangıçta yüklenmiyor.

class GenerationWorker(QThread):
    """
    AI görüntü üretimini ayrı bir iş parçacığında (thread) yürüten işçi sınıfı.
    """
    finished = Signal(QImage)

    def __init__(self, prompt: str, parent=None):
        super().__init__(parent)
        self.prompt = prompt
        self.width = 1024
        self.height = 1024
        self.pipe = None

    def run(self):
        # Tembel Yükleme: Kütüphaneler sadece bu thread çalıştığında yüklenir.
        import torch
        from diffusers import AutoPipelineForText2Image

        if self.pipe is None:
            print("Difüzyon modeli yükleniyor (ilk çalıştırmada uzun sürebilir)...")
            model_id = "stabilityai/stable-diffusion-xl-base-1.0"
            torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
            self.pipe = AutoPipelineForText2Image.from_pretrained(model_id, torch_dtype=torch_dtype)
            if torch.cuda.is_available():
                self.pipe = self.pipe.to("cuda")
                print("cuda bulundu.")
            else:
                print("Uyarı: GPU bulunamadı. Model CPU üzerinde çalışacak ve bu yavaş olabilir.")
            print("Model yüklendi.")

        image = self.pipe(
            prompt=self.prompt,
            num_inference_steps=30,
            guidance_scale=7.5,
            width=self.width,
            height=self.height
        ).images[0]

        q_image = ie_utils._pil_to_qimage(image)
        self.finished.emit(q_image.copy())

class InpaintingWorker(QThread):
    """
    AI nesne silme (inpainting) işlemini yürüten işçi sınıfı.
    """
    finished = Signal(QImage)

    def __init__(self, image: QImage, mask: QImage, prompt: str, parent=None):
        super().__init__(parent)
        self.image = image
        self.mask = mask
        self.prompt = prompt
        self.pipe = None

    def run(self):
        # Tembel Yükleme: Kütüphaneler sadece bu thread çalıştığında yüklenir.
        import torch
        from diffusers import AutoPipelineForInpainting

        if self.pipe is None:
            print("Inpainting modeli yükleniyor...")
            model_id = "diffusers/stable-diffusion-xl-1.0-inpainting-0.1"
            torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
            self.pipe = AutoPipelineForInpainting.from_pretrained(model_id, torch_dtype=torch_dtype)
            if torch.cuda.is_available():
                self.pipe = self.pipe.to("cuda")
                print("cuda bulundu.")
            else:
                print("Uyarı: GPU bulunamadı. Model CPU üzerinde çalışacak.")
            print("Inpainting modeli yüklendi.")

        pil_image = ie_utils._qimage_to_pil(self.image)
        pil_mask = ie_utils._qimage_to_pil(self.mask)

        output = self.pipe(
            prompt=self.prompt,
            image=pil_image,
            mask_image=pil_mask,
            num_inference_steps=30,
            guidance_scale=7.5,
            strength=0.99
        ).images[0]

        q_image = ie_utils._pil_to_qimage(output)
        self.finished.emit(q_image)


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


class Editor(QWidget, draw_window_ui.Ui_Form):
    def __init__(self, image_path: str = None, width: int = -1, height: int = -1) -> None:
        super(Editor, self).__init__()

        self.setupUi(self)
        self.image_path = image_path
        self.is_checkerboard_enabled = True

        # Determine image dimensions
        if width != -1:
            w = width
        else:
            w = ie_globals.image_width
        if height != -1:
            h = height
        else:
            h = ie_globals.image_height

        # Use a more standard image format like ARGB32
        image_format = QImage.Format.Format_ARGB32

        self.widgetPicture1.setFixedSize(w, h)
        self.widgetPicture1.setStyleSheet(u"background-image: url(:/png/resources/images/checker20.png);")

        # Initialize QImages with the chosen format and fill with transparent
        self.pic2 = QImage(w, h, image_format)
        self.pic2.fill(Qt.GlobalColor.transparent)
        '''
        A temporary QImage used for drawing operations.
        '''
        self.picOrg = QImage(w, h, image_format)
        self.picOrg.fill(Qt.GlobalColor.transparent)
        '''
        The main QImage for the current layer.
        '''

        self.widgetPicture1.setMouseTracking(True)
        self.widgetPicture1.mousePressEvent = self.pic1_mousePressEvent
        self.widgetPicture1.mouseMoveEvent = self.pic1_mouseMoveEvent
        self.widgetPicture1.mouseReleaseEvent = self.pic1_mouseReleaseEvent
        self.widgetPicture1.paintEvent = self.pic1_paintEvent
        self.widgetPicture1.wheelEvent = self.pic1_mouseWheelEvent
        self.widgetPicture1.show()

        self.startPos = QPoint(0, 0)
        self.lastPos = QPoint(0, 0)
        self.docStartPos = QPoint(0, 0)
        self.zoomFactor = 1.0

        # Create background layer
        bg_image = QImage(w, h, image_format)
        bg_image.fill(Qt.GlobalColor.transparent)
        layerbg = ie_globals.Layer(
            "Background", visible=True, opacity=100,
            image=bg_image, rasterized=True, locked=False
        )
        self.layers: list = []
        layerbg.active = True
        layerbg.id = time.time_ns()
        self.layers.append(layerbg)
        self.currentLayerId: int = layerbg.id

        self.panning = False
        self.previous_tool = ie_globals.ie_tool_pen

        # Undo/Redo setup
        self.undoList: list = []
        self.undoLayerList: list = []
        self.undoIndex = -1
        self.appendUndoImage()

        # AI workers
        self.generation_worker = None
        self.inpainting_worker = None

    def open_brush_settings(self):
        dialog = BrushSettingsDialog(self)
        dialog.exec()

    def generate_image_from_prompt(self, prompt: str):
        """
        Generates an image based on a text prompt using a diffusion model in a separate thread.
        """
        try:
            import torch
            from diffusers import AutoPipelineForText2Image
        except ImportError:
            print("Gerekli kütüphaneler bulunamadı. Lütfen 'pip install torch transformers diffusers accelerate' komutu ile kurun.")
            self.picOrg.fill(Qt.GlobalColor.black)
            painter = QPainter(self.picOrg)
            painter.setPen(QPen(Qt.GlobalColor.white))
            font = painter.font()
            font.setPointSize(16)
            painter.setFont(font)
            painter.drawText(self.picOrg.rect(), Qt.AlignmentFlag.AlignCenter,
                             "AI Üretimi için kütüphaneler eksik.\nLütfen terminalden kurun:\n"
                             "pip install torch diffusers transformers accelerate")
            painter.end()
            self.pic1_update()
            return

        if self.generation_worker is not None:
            print("Zaten bir görüntü üretiliyor. Lütfen mevcut işlemin bitmesini bekleyin.")
            return

        print("Görüntü üretimi başlıyor... Bu işlem biraz zaman alabilir.")
        self.picOrg.fill(Qt.GlobalColor.black)
        painter = QPainter(self.picOrg)
        painter.setPen(QPen(Qt.GlobalColor.white))
        font = painter.font()
        font.setPointSize(20)
        painter.setFont(font)
        painter.drawText(self.picOrg.rect(), Qt.AlignmentFlag.AlignCenter, f"Üretiliyor...\n'{prompt}'")
        painter.end()
        self.pic1_update()

        self.generation_worker = GenerationWorker(prompt)
        self.generation_worker.finished.connect(self.on_generation_finished)
        self.generation_worker.start()

    def on_generation_finished(self, generated_image: QImage):
        """
        Görüntü üretme iş parçacığı bittiğinde bu slot çağrılır.
        """
        new_pic = QImage(self.picOrg.size(), QImage.Format.Format_ARGB32)
        new_pic.fill(Qt.GlobalColor.transparent)

        painter = QPainter(new_pic)
        target_rect = self.picOrg.rect()
        scaled_image = generated_image.scaled(target_rect.size(), Qt.AspectRatioMode.KeepAspectRatio,
                                              Qt.TransformationMode.SmoothTransformation)
        x = (target_rect.width() - scaled_image.width()) / 2
        y = (target_rect.height() - scaled_image.height()) / 2
        painter.drawImage(QPoint(int(x), int(y)), scaled_image)
        painter.end()

        self.picOrg = new_pic
        self.appendUndoImage()
        self.pic1_update()
        print("Görüntü üretimi tamamlandı.")
        self.generation_worker = None

    ##region mouse wheel [rgba(222, 100, 222,0.1)]
    def pic1_mouseWheelEvent(self, event: QtGui.QWheelEvent) -> None:
        """
        Handles mouse wheel events for zooming in and out of the image, centered on the mouse cursor.
        """
        
        # 1. Yakınlaştırma oranını belirle ve yeni yakınlaştırma faktörünü hesapla
        zoom_delta = 1.25
        old_zoom_factor = self.zoomFactor
        if event.angleDelta().y() > 0:
            new_zoom_factor = old_zoom_factor * zoom_delta
        else:
            new_zoom_factor = old_zoom_factor / zoom_delta
        new_zoom_factor = max(0.1, min(10.0, new_zoom_factor))

        # Eğer yakınlaştırma değişmediyse, bir şey yapma
        if abs(new_zoom_factor - old_zoom_factor) < 0.001:
            return

        # 2. Mevcut durumları al
        hbar = self.scrollArea.horizontalScrollBar()
        vbar = self.scrollArea.verticalScrollBar()
       
        old_scroll_pos = QPointF(hbar.value(), vbar.value())

        # Fare konumunu al. event.position() yerine QCursor.pos() kullanmak
        # genellikle daha güvenilirdir, çünkü mutlak ekran konumunu verir.
        # Sonra bunu widget'ın yerel koordinatlarına çeviririz.
        mouse_pos_on_widget = self.widgetPicture1.mapFromGlobal(QCursor.pos())

        # 3. Gerekli kaydırma miktarını hesapla
        # Formül: YeniKaydırma = EskiKaydırma + FareKonumu * (YakınlaştırmaOranı - 1)
        # Bu formül, fare imlecinin altındaki noktanın ekranda sabit kalmasını sağlar.
        zoom_ratio = new_zoom_factor / old_zoom_factor
        displacement = QPointF(mouse_pos_on_widget) * (zoom_ratio - 1.0)
        new_scroll_pos = old_scroll_pos + displacement

        # 4. Yeni yakınlaştırmayı ve boyutu uygula
        self.zoomFactor = new_zoom_factor
        self.pic1_update()  # Bu, widget'ı yeniden boyutlandırır ve kaydırma çubuklarının aralığını günceller

        # 5. Yeni kaydırma değerlerini uygula
        # Bu, pic1_update çağrıldıktan *sonra* yapılmalıdır ki, kaydırma çubuklarının
        # yeni maksimum değerleri hesaplanmış olsun.
        hbar.setValue(int(new_scroll_pos.x()))
        vbar.setValue(int(new_scroll_pos.y()))

    #endregion

    #region mouse press [rgba(255, 255, 121,0.1)]
    def pic1_mousePressEvent(self, event: QMouseEvent) -> None:
        """
        Handles mouse press events on the image display widget (`widgetPicture1`).
        Initiates drawing actions based on the currently selected tool.

        Args:
            event (QMouseEvent): The mouse press event.
        """
        if event.button() == Qt.MouseButton.LeftButton:
            self.pic2 = self.picOrg.copy()
            self.lastPos = event.pos()
            self.startPos = event.pos()
            virtualStartPos: QPoint = QPoint(
                math.trunc(self.startPos.x() / self.zoomFactor),
                math.trunc(self.startPos.y() / self.zoomFactor))
            
            tool = ie_globals.current_tool
            if tool == ie_globals.ie_tool_pen:
                ie_tools.draw_pen(self.picOrg, virtualStartPos, virtualStartPos)
            elif tool == ie_globals.ie_tool_brush:
                ie_tools.draw_brush(self.picOrg, virtualStartPos)
            elif tool == ie_globals.ie_tool_fill:
                ie_tools.fill(img1=self.picOrg, pt1=virtualStartPos, task="down", tolerance=ie_globals.fill_tolerance)
            elif tool == ie_globals.ie_tool_wand:
                ie_tools.select_wand(img1=self.picOrg, pt1=virtualStartPos, task="down")
            elif tool == ie_globals.ie_tool_select_rect:
                ie_tools.select_rect(pt1=virtualStartPos, pt2=virtualStartPos, task="down")
            elif tool == ie_globals.ie_tool_select_circle:
                ie_tools.select_circle(pt1=virtualStartPos, pt2=virtualStartPos, task="down")
            elif tool == ie_globals.ie_tool_eraser:
                ie_tools.erase(self.picOrg, virtualStartPos, virtualStartPos, "down")
            elif tool == ie_globals.ie_tool_dropper:
                ie_globals.previous_tool = ie_globals.current_tool
                previous_alpha = ie_globals.current_pen.color().alpha()
                ie_globals.current_pen.setColor(self.picOrg.pixelColor(virtualStartPos))
                ie_globals.current_pen.color().setAlpha(previous_alpha)
                ie_globals.current_brush.setColor(ie_globals.current_pen.color())
                ie_globals.current_tool = ie_globals.previous_tool

            self.pic1_update()
        elif event.button() == Qt.MouseButton.MiddleButton:
            self.panning = True
            self.startPos = event.globalPos()

    #endregion

    #region mouse move [rgba(255, 152, 121,0.1)]
    def pic1_mouseMoveEvent(self, event: QMouseEvent) -> None:
        """
        Handles mouse move events on the image display widget (`widgetPicture1`).
        """
        if event.buttons() == Qt.MouseButton.LeftButton:
            virtualStartPos = QPoint(int(self.startPos.x() / self.zoomFactor), int(self.startPos.y() / self.zoomFactor))
            virtualpos = QPoint(int(event.pos().x() / self.zoomFactor), int(event.pos().y() / self.zoomFactor))
            virtualLastPos = QPoint(int(self.lastPos.x() / self.zoomFactor), int(self.lastPos.y() / self.zoomFactor))
            
            ie_globals.statusText.pos = f"Mouse Position: {virtualpos.x()}, {virtualpos.y()}"

            tool = ie_globals.current_tool
            if tool in [ie_globals.ie_tool_pen, ie_globals.ie_tool_brush]:
                ie_tools.draw_pen(self.picOrg, virtualLastPos, virtualpos)
            elif tool == ie_globals.ie_tool_eraser:
                ie_tools.erase(self.picOrg, virtualLastPos, virtualpos, "move")
            elif tool in [ie_globals.ie_tool_line, ie_globals.ie_tool_circle, ie_globals.ie_tool_rect, ie_globals.ie_tool_circle_outline, ie_globals.ie_tool_rounded_rect]:
                self.picOrg = self.pic2.copy()
                if tool == ie_globals.ie_tool_line: ie_tools.draw_line(self.picOrg, virtualStartPos, virtualpos, "move")
                if tool == ie_globals.ie_tool_circle: ie_tools.draw_circle(self.picOrg, virtualStartPos, virtualpos, "move")
                if tool == ie_globals.ie_tool_rect: ie_tools.draw_rect(self.picOrg, virtualStartPos, virtualpos, "move")
                if tool == ie_globals.ie_tool_circle_outline: ie_tools.draw_circle_outline(self.picOrg, virtualStartPos, virtualpos, "move")
                if tool == ie_globals.ie_tool_rounded_rect: ie_tools.draw_round_rect(self.picOrg, virtualStartPos, virtualpos, "move")
            elif tool == ie_globals.ie_tool_spray:
                ie_tools.draw_spray(self.picOrg, virtualpos, "move")
            elif tool == ie_globals.ie_tool_select_rect:
                ie_tools.select_rect(pt1=virtualStartPos, pt2=virtualpos, task="move")
            elif tool == ie_globals.ie_tool_select_circle:
                ie_tools.select_circle(pt1=virtualStartPos, pt2=virtualpos, task="move")

            self.lastPos = event.pos()
            self.pic1_update()

        elif event.buttons() == Qt.MouseButton.MiddleButton and self.panning:
            delta = event.globalPos() - self.startPos
            self.scrollArea.horizontalScrollBar().setValue(self.scrollArea.horizontalScrollBar().value() - delta.x())
            self.scrollArea.verticalScrollBar().setValue(self.scrollArea.verticalScrollBar().value() - delta.y())
            self.startPos = event.globalPos()

    #endregion

    #region mouse release [rgba(255, 255, 121,0.1)]
    def pic1_mouseReleaseEvent(self, event: QMouseEvent) -> None:
        """
        Handles mouse release events.
        """
        if event.button() == Qt.MouseButton.LeftButton:
            virtualStartPos = QPoint(int(self.startPos.x() / self.zoomFactor), int(self.startPos.y() / self.zoomFactor))
            virtualpos = QPoint(int(event.pos().x() / self.zoomFactor), int(event.pos().y() / self.zoomFactor))
            
            tool = ie_globals.current_tool
            if tool == ie_globals.ie_tool_select_rect:
                ie_tools.select_rect(pt1=virtualStartPos, pt2=virtualpos, task="release")
            elif tool == ie_globals.ie_tool_select_circle:
                ie_tools.select_circle(pt1=virtualStartPos, pt2=virtualpos, task="release")
            else:
                self.appendUndoImage()
            
            self.pic1_update()

        elif event.button() == Qt.MouseButton.MiddleButton:
            self.panning = False

    #endregion
    def appendUndoImage(self) -> None:
        """
        Appends the current state of `picOrg` and the `currentLayerId` to the undo history.
        If the undo list exceeds `ie_globals.max_undo_steps`, the oldest entry is removed.
        """
        if len(self.undoList) >= ie_globals.max_undo_steps:
            self.undoList.pop(0)
            self.undoLayerList.pop(0)

        self.undoList.append(self.picOrg.copy())
        layerindex = next((layer.id for layer in self.layers if layer.id == self.currentLayerId), None)
        
        if layerindex is None:
            raise ValueError(f"No layer found with id {self.currentLayerId}")

        self.undoLayerList.append(layerindex)
        self.undoIndex = len(self.undoList) - 1


    def undoImage(self) -> None:
        """
        Reverts the image to the previous state in the undo history.
        """
        if self.undoIndex > 0:
            self.undoIndex -= 1
            self.drawUndoImage()


    def redoImage(self) -> None:
        """
        Advances the image to the next state in the undo history.
        """
        if self.undoIndex < len(self.undoList) - 1:
            self.undoIndex += 1
            self.drawUndoImage()


    def drawUndoImage(self) -> None:
        """
        Restores the image and active layer to a state from the undo history.
        """
        if 0 <= self.undoIndex < len(self.undoList):
            layer_id_to_restore = self.undoLayerList[self.undoIndex]
            layer_to_restore = next((layer for layer in self.layers if layer.id == layer_id_to_restore), None)
            
            if layer_to_restore:
                layer_to_restore.image = self.undoList[self.undoIndex].copy()
                if layer_to_restore.id == self.currentLayerId:
                    self.picOrg = layer_to_restore.image
            else:
                # Fallback for safety
                self.picOrg = self.undoList[self.undoIndex].copy()

            self.pic1_update()

    #region paint [rgba(125, 152, 200,0.1)]
    def pic1_update(self) -> None:
        """
        Updates the display of `widgetPicture1` by adjusting its size and triggering a repaint.
        """
        ie_globals.statusText.zoom = f"Zoom: {self.zoomFactor:.2f}"
        w = int(self.picOrg.width() * self.zoomFactor)
        h = int(self.picOrg.height() * self.zoomFactor)
        self.widgetPicture1.setFixedSize(w, h)
        self.widgetPicture1.update()

    def pic1_paintEvent(self, event: QPaintEvent) -> None:
        """
        Handles the paint event for the image display area.
        """
        canvasPainter = QPainter(self.widgetPicture1)
        canvasPainter.drawPixmap(self.widgetPicture1.rect(), QPixmap.fromImage(self.picOrg))

        if ie_globals.has_selection:
            current_color = ie_globals.selection_colors[ie_globals.current_selection_color_index]
            
            edge_pen = QPen(current_color, 2, Qt.PenStyle.DashLine)
            edge_pen.setDashPattern([4, 4])
            edge_pen.setDashOffset((time.time() * 10) % 8)
            
            canvasPainter.setPen(edge_pen)
            canvasPainter.setBrush(Qt.BrushStyle.NoBrush)

            transform = QtGui.QTransform().scale(self.zoomFactor, self.zoomFactor)

            if ie_globals.selection_type == 'wand' and ie_globals.selection_edge_pixels:
                path = QPainterPath()
                for x, y in ie_globals.selection_edge_pixels:
                    path.addRect(QRectF(x, y, 1, 1))
                canvasPainter.drawPath(transform.map(path))
            elif ie_globals.selection_bounds:
                scaled_rect = transform.mapRect(QRectF(ie_globals.selection_bounds))
                if ie_globals.selection_type == 'circle':
                    canvasPainter.drawEllipse(scaled_rect)
                else:
                    canvasPainter.drawRect(scaled_rect)
        canvasPainter.end()
   
    def apply_melt_filter(self):
        if self.picOrg:
            self.picOrg = melt_image(self.picOrg, amount=ie_globals.melt_amount)
            self.appendUndoImage()
            self.pic1_update()

    def apply_shear_filter(self):
        if self.picOrg:
            self.picOrg = shear_image(self.picOrg, amount=ie_globals.shear_amount, horizontal=ie_globals.shear_horizontal, direction=ie_globals.shear_direction)
            self.appendUndoImage()
            self.pic1_update()

    def apply_blur_filter(self):
        if self.picOrg:
            self.picOrg = blur_image(self.picOrg, radius=ie_globals.blur_radius)
            self.appendUndoImage()
            self.pic1_update()

    def apply_gaussian_blur_filter(self):
        if self.picOrg:
            self.picOrg = gaussian_blur_image(self.picOrg, radius=ie_globals.gaussian_blur_radius)
            self.appendUndoImage()
            self.pic1_update()

    def apply_mosaic_filter(self):
        if self.picOrg:
            self.picOrg = mosaic_image(self.picOrg, block_size=ie_globals.mosaic_block_size)
            self.appendUndoImage()
            self.pic1_update()

    def apply_sepia_filter(self):
        if self.picOrg:
            self.picOrg = ie_filters.apply_sepia(self.picOrg)
            self.appendUndoImage()
            self.pic1_update()

    def remove_object_with_ai(self):
        """
        Removes the selected object using AI inpainting.
        """
        try:
            import torch
            from diffusers import AutoPipelineForInpainting
        except ImportError:
            print("Gerekli AI kütüphaneleri eksik.")
            return
            
        if not ie_globals.has_selection:
            print("Lütfen önce silinecek nesneyi seçin.")
            return

        print("Nesne silme işlemi başlatılıyor...")
        mask = QImage(self.picOrg.size(), QImage.Format.Format_Grayscale8)
        mask.fill(Qt.GlobalColor.black)
        
        painter = QPainter(mask)
        painter.setPen(QColor(255, 255, 255))
        painter.drawPoints([QPoint(x, y) for x, y in ie_globals.current_selection])
        painter.end()

        prompt = "background, clean, empty"
        self.inpainting_worker = InpaintingWorker(self.picOrg, mask, prompt)
        self.inpainting_worker.finished.connect(self.on_inpainting_finished)
        self.inpainting_worker.start()

    def on_inpainting_finished(self, new_image: QImage):
        self.picOrg = new_image
        self.appendUndoImage()
        self.pic1_update()
        print("Nesne silme tamamlandı.")
        self.inpainting_worker = None
