import math
import os
import sys
import time

import PySide6
from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtCore import QPoint, QPointF,Qt
from PySide6.QtGui import QPen, QColor, QBrush, QImage, QPainter, QMouseEvent, QPixmap
from PySide6.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QSizePolicy, QLabel, QHBoxLayout, QScrollArea, \
    QGridLayout, QWidget
from PySide6.QtWidgets import QFrame
import ie_tools
import draw_window_ui
import ie_globals, ie_mouse_events

class Editor(draw_window_ui.Ui_Form, QWidget):
    def __init__(self, image_path: str, /) -> None:
        super().__init__()

        self.setupUi(self)  # Ensure the UI is set up
        self.image_path = image_path
        # You can add more initialization code here
        self.is_checkerboard_enabled = True
        w=ie_globals.image_width
        h=ie_globals.image_height
 
        self.widgetPicture1.setFixedSize(w , h )
        self.widgetPicture1.image = PySide6.QtGui.QImage(w, h, QImage.Format.Format_RGBA64)
        self.pic1 = self.widgetPicture1.image
        self.pic1.fill(QColor(255, 0, 255))


        self.pic2 = PySide6.QtGui.QImage(w, h, QImage.Format.Format_RGBA64)
        self.picOrg = PySide6.QtGui.QImage(w, h, QImage.Format.Format_RGBA64)
        self.widgetPicture1.setMouseTracking(True)
        self.widgetPicture1.mousePressEvent = self.pic1_mousePressEvent
        self.widgetPicture1.mouseMoveEvent = self.pic1_mouseMoveEvent
        self.widgetPicture1.mouseReleaseEvent = self.pic1_mouseReleaseEvent
        self.widgetPicture1.paintEvent = self.pic1_paintEvent
        self.widgetPicture1.wheelEvent = self.pic1_mouseWheelEvent # type: ignore
        # self.widgetPicture1.setFixedSize(400, 300)
        self.widgetPicture1.show()
        self.widgetPicture1.setAttribute(Qt.WidgetAttribute.WA_SetStyle, True)

       
        self.startPos = QPoint(0, 0)
        self.lastPos = QPoint(0, 0)
        self.docStartPos = QPoint(0, 0)
        self.zoomFactor = 1.0



        layerbg: ie_globals.Layer=ie_globals.Layer("Background", visible=True, opacity=100, image=PySide6.QtGui.QImage(w, h, QImage.Format.Format_RGBA64), rasterized=True,locked=False)
        self.layers: list = []
        layerbg.active=True
        layerbg.id= time.time_ns()  # create unique identifier
        print (layerbg.id)
        self.layers.append(layerbg)
        self.currentLayerId:int = layerbg.id     #Layer index of current layer , change when active layer changed

        self.panning = False
        self.previous_tool = "pen"

         #undo/redo variables
        self.undoList : list = [] # list of images for each undo operation
        self.undoLayerList : list = []# list of layer numbers for each undo operation
        self.undoIndex = -1 # index of current undo operation
        self.appendUndoImage()# add original image to undo list
    



#region mouse wheel [rgba(222, 100, 222,0.1)]
    def pic1_mouseWheelEvent(self, event: QtGui.QWheelEvent) -> None:
        hbar = self.scrollArea.horizontalScrollBar()
        vbar = self.scrollArea.verticalScrollBar()

        # Mouse position relative to viewport
        event_pos = event.position()


        # Apply zoom delta
        if event.angleDelta().y() > 0:
            self.zoomFactor *= ie_globals.zoomInFactor
        else:
            self.zoomFactor *= ie_globals.zoomOutFactor

        self.zoomFactor = max(0.1, min(10.0, self.zoomFactor))

        # Update widget size (this changes scroll bar ranges)
        self.pic1_update()
        hbar.setValue((event_pos.x())/self.pic1.width(
        vbar.setValue( event_pos.y()*self.zoomFactor/ie_globals.image_height)




#endregion

#region mouse press [rgba(255, 255, 121,0.1)]
    def pic1_mousePressEvent(self, event: QMouseEvent) -> None:
        # print mouse position
        #print  (event.pos())
        # if left mouse button is pressed
        if event.button() == Qt.MouseButton.LeftButton:
            # make drawing flag true
            eventstr="down"
            self.pic2 = self.picOrg.copy()

            # make last point to the point of cursor
            self.lastPos = event.pos()
            self.startPos = event.pos()
            virtualStartPos: QPoint = QPoint(
                math.trunc(self.startPos.x() / self.zoomFactor),
                math.trunc(self.startPos.y() / self.zoomFactor))
            if ie_globals.current_tool == 'pen':
                    ie_tools.draw_line(self.picOrg,  virtualStartPos, virtualStartPos, eventstr)
                    self.startPos = event.pos()
            elif ie_globals.current_tool == 'fill':
                ie_tools.fill(img1=self.picOrg, pt1= virtualStartPos,task="down")
            elif ie_globals.current_tool == 'wand':
                ie_tools.select_wand(img1=self.picOrg, pt1= virtualStartPos,task="down")
            elif ie_globals.current_tool == 'eraser':
                ie_tools.erase(self.picOrg, pt1= virtualStartPos, task="down")
            elif ie_globals.current_tool == 'dropper':
                ie_globals.pen_color= self.picOrg.pixelColor(virtualStartPos)
                ie_globals.pen.setColor(ie_globals.pen_color)
                ie_globals.current_tool=ie_globals.previous_tool
                

            self.pic1_update()
        elif event.button() == Qt.MouseButton.MiddleButton:
            self.panning = True
            self.startPos = event.globalPos()
            self.docStartPos = self.widgetPicture1.pos()

#endregion

#region mouse move [rgba(255, 152, 121,0.1)]
    def pic1_mouseMoveEvent(self, event: QMouseEvent) -> None:
        eventstr: str = "move"

        if event.buttons() == Qt.MouseButton.LeftButton :
            virtualStartPos: QPoint = QPoint(
                math.trunc(self.startPos.x() / self.zoomFactor),
                math.trunc(self.startPos.y() / self.zoomFactor)
            )
            virtualpos: QPoint = QPoint(
                math.trunc(event.pos().x() / self.zoomFactor),
                math.trunc(event.pos().y() / self.zoomFactor)
            )
            ie_globals.statusText.pos= "Mouse Position: " + str(virtualpos.x()) + ", " + str(virtualpos.y())
           
            if ie_globals.current_tool == 'pen':
                ie_globals.pen.setCapStyle(Qt.PenCapStyle.RoundCap)
                ie_globals.pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
                ie_tools.draw_line(self.picOrg,  virtualStartPos, virtualpos, eventstr)
                self.startPos = event.pos()

            elif ie_globals.current_tool == 'line':
                self.picOrg=self.pic2.copy()
                ie_tools.draw_line(self.picOrg, virtualStartPos, virtualpos, eventstr)
            elif ie_globals.current_tool == 'circle':
                self.picOrg = self.pic2.copy()
                ie_tools.draw_circle(self.picOrg, virtualStartPos, virtualpos, eventstr)
            elif ie_globals.current_tool == 'rect':
                self.picOrg = self.pic2.copy()
                ie_tools.draw_rect(self.picOrg, virtualStartPos, virtualpos, eventstr)
            elif ie_globals.current_tool == 'round_rect':
                self.picOrg = self.pic2.copy()
                ie_tools.draw_round_rect(self.picOrg, virtualStartPos, virtualpos, eventstr, corner_radius=ie_globals.round_rect_corner_radius)
            elif ie_globals.current_tool == 'spray':
                ie_tools.draw_spray(self.picOrg, virtualpos,eventstr)
            elif ie_globals.current_tool == 'pan':
                # deltaX = event.x() - self.startPos.x()
                # deltaY = event.y() - self.startPos.y()
                # self.widgetPicture1.move(self.widgetPicture1.x() + deltaX, self.widgetPicture1.y() + deltaY)
                # self.startPos = event.pos()
                pass
            self.lastPos = event.pos()
            # update
            self.pic1_update()

        elif event.buttons() == Qt.MouseButton.MiddleButton and self.panning:
            deltaX = event.globalPosition().x() - self.startPos.x()
            deltaY = event.globalPosition().y() - self.startPos.y()
            #self.widgetPicture1.move(self.docStartPos.x() + deltaX, self.docStartPos.y() + deltaY)
            self.scrollArea.verticalScrollBar().setValue(self.scrollArea.verticalScrollBar().value() - deltaY)
            self.scrollArea.horizontalScrollBar().setValue(self.scrollArea.horizontalScrollBar().value() - deltaX)
            self.startPos = event.globalPosition().toPoint()


#endregion

#region mouse release [rgba(255, 255, 121,0.1)]
    def pic1_mouseReleaseEvent(self, event: QMouseEvent) -> None:
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
        #try:
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
            print("undo index", self.undoIndex, len(self.undoList))  # Consider using logging instead
        #except Exception as e:
        #    print(f"Error appending undo image: {e}")  # Consider using logging instead
            # Optionally, you might want to roll back changes or handle the error in a specific way

    
    def undoImage(self) -> None:
        
        if self.undoIndex > 0:
            self.undoIndex -= 1
        self.drawUndoImage()
        print("undo index", self.undoIndex, len(self.undoList))


    def redoImage(self) -> None:

        if self.undoIndex < len(self.undoList) - 1:
            self.undoIndex += 1
        self.drawUndoImage()
        print("undo index", self.undoIndex, len(self.undoList))

    def drawUndoImage(self) -> None:
        if self.undoIndex < 0 or self.undoIndex >= len(self.undoList):
            return
        self.picOrg = self.undoList[self.undoIndex].copy()
        self.pic1_update()
        #todo : find active layer and draw undo image on it


   #region paint [rgba(125, 152, 200,0.1)]
    #picture 1 view update from original image
    def pic1_update(self) -> None:
        ie_globals.statusText.zoom = "Zoom: " + str(self.zoomFactor)
        w=int(self.picOrg.width()*self.zoomFactor)
        h=int(self.picOrg.height()*self.zoomFactor)
        self.widgetPicture1.setFixedSize(w, h)

        #self.pic1 = self.picOrg.scaled(w, h,Qt.AspectRatioMode.KeepAspectRatio)

        #self.widgetPicture1.image=self.pic1

        self.scrollArea.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        self.scrollArea.minimumWidth= w
        self.scrollArea.minimumHeight= h
        self.scrollArea.width =w
        self.scrollArea.height =h
        self.scrollArea.update()

        
        self.widgetPicture1.update() #call paint event
    # paint event
    def pic1_paintEvent(self, event: QtGui.QPaintEvent) -> None:
        # create a canvas
        canvasPainter = QPainter(self.widgetPicture1)
        #print(self.widgetPicture1.size(),self.picOrg.size(),event.rect().size())
        # draw rectangle  on the canvas
        w=self.widgetPicture1.width()
        h=self.widgetPicture1.height()
        # Assuming self.picOrg is a QImage object
        pixmap = QPixmap.fromImage(self.picOrg)
        #draw scaled pixmap on canvas in event rect
        canvasPainter.drawPixmap(self.widgetPicture1.rect(), pixmap, pixmap.rect())



        #canvasPainter.drawPixmap(0, 0, pixmap, 0, 0,500,500)
        # pix_size = event.rect().size()
        # pix_size.scale(self.widgetPicture1.size(), Qt.AspectRatioMode.KeepAspectRatio)
        # scaledPix: QPixmap= pixmap.scaled(pix_size,Qt.AspectRatioMode.KeepAspectRatio,Qt.TransformationMode.SmoothTransformation )
        # canvasPainter.drawPixmap(event.rect(),scaledPix, scaledPix.rect())

        canvasPainter.end()