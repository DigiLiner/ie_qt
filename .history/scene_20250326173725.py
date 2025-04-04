import math
import random
import sys

import PyQt6
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtCore import SIGNAL, QPoint
from PyQt6.QtGui import QPen, QColor, QBrush, Qt, QTransform, QPainter, QPixmap
from PyQt6.QtWidgets import  QGraphicsScene, QGraphicsItem, QGraphicsRectItem

from PyQt6.QtWidgets import QStyleOptionGraphicsItem

from main_ui import Ui_MainWindow
import ie_globals
class GraphicsScene(QGraphicsScene ):
    def __init__(self, parent, width, height):
        super().__init__(parent)
        self.setSceneRect(0, 0, width, height)
        rect_item = QGraphicsRectItem(0, 0, width, height)
        rect_item.setPen(QPen(QColor(0, 0, 0), 1))
        rect_item.setBrush(QBrush(QColor(255, 255, 255)))

        self.addItem(rect_item)
        self.drawing=False
        self.selected = None
        self.selected_offset_x = 0
        self.selected_offset_y = 0
        self.start_pos :QPoint = QPoint(0, 0)  # type: ignore
        self.pen = QPen(QColor(0, 255, 0), 5)
        self.pen.setCosmetic(True)
        self.pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)


    def mousePressEvent(self, event) -> None:

        if event.button() == Qt.MouseButton.LeftButton:
            if self.sceneRect().contains(event.scenePos()):
                print("Mouse clicked inside the scene at:", event.scenePos())
                self.drawing = True
                super().mousePressEvent(event)
            else:
                print("Mouse clicked outside the scene at:", event.scenePos())
            if self.drawing:
                x = event.scenePos().x()
                y = event.scenePos().y()
                self.selected_offset_x = x
                self.selected_offset_y = y
                self.start_pos=event.scenePos()
                self.start_pos=event.scenePos()
                if ie_globals.current_tool == "line":
                    line_item = QtWidgets.QGraphicsLineItem(QtCore.QLineF(self.start_pos, event.scenePos()))

                    pen = QPen(QColor(255, 0, 255), 10)
                    pen.setCosmetic(True)
                    pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
                    pen.setCapStyle(Qt.PenCapStyle.RoundCap)
                    line_item.setPen(pen)
                    self.selected = line_item
                    self.addItem(line_item)
                elif ie_globals.current_tool == "pen":
                    pen_item = QtWidgets.QGraphicsLineItem(QtCore.QLineF(self.start_pos, event.scenePos()))
                    self.selected = pen_item
                    self.addItem(pen_item)
                elif ie_globals.current_tool == "rect":
                    # rect_width = 1
                    # rect_height = 1
                    # rect_item = QtWidgets.QGraphicsRectItem(QtCore.QRectF(self.start_pos.x(), self.start_pos.y(), rect_width, rect_height))
                    # rect_item.setPen(self.pen)
                    # rect_item.setBrush(QBrush(QColor(255, 0, 0, 255)))
                    # self.selected = rect_item
                    # self.addItem(rect_item)
                    pass
                elif ie_globals.current_tool == "select":
                    pass
                elif ie_globals.current_tool == "circle":
                    center_x = (self.start_pos.x() + event.scenePos().x())/2
                    center_y = (self.start_pos.y() + event.scenePos().y())/2
                    #radius = (center_x - event.scenePos().x())/2
                    radius = math.hypot(self.start_pos.x() - event.scenePos().x(), self.start_pos.y() - event.scenePos().y())
                    print (radius)
                    circle_item = QtWidgets.QGraphicsEllipseItem(QtCore.QRectF(self.start_pos.x()-radius,self.start_pos.y()-radius, radius*2, radius*2))
                    circle_item.setPen(self.pen)
                    circle_item.setBrush(QBrush(QColor(255, 0, 0, 255)))
                    self.addItem(circle_item)
                    self.selected = circle_item
                elif ie_globals.current_tool == "spray":
                    pass
                elif ie_globals.current_tool == "fill":
                    pass




        elif event.button() ==  PyQt6.QtCore.Qt.MouseButton.RightButton:
            x = event.scenePos().x()
            y = event.scenePos().y()

            if not self.selected:
                item = self.itemAt(event.scenePos(), QTransform())
                # print(item)

                if item:
                    print('selected:', item)
                    self.selected = item
                    self.selected.setBrush(QBrush(QColor(255, 0, 0, 255)))
                    self.selected_offset_x = x - item.pos().x()
                    self.selected_offset_y = y - item.pos().y()
                    # self.selected_offset_x = 5  # rect_width/2   # to keep center of rect
                    # self.selected_offset_y = 5  # rect_height/2  # to keep center of rect
        # super().mousePressEvent(event)

    def convert(self, item: QGraphicsItem) -> QPixmap:
        pixmap = QPixmap(int(item.boundingRect().width())+self.pen.width(),int( item.boundingRect().height()+self.pen.width()))
        pixmap.fill(PyQt6.QtGui.QColor(255, 0, 0, 0))
        painter = QPainter(pixmap)
        # this line seems to be needed for all items except of a LineItem...
        #painter.translate(-item.boundingRect().topLeft())

        opt = QStyleOptionGraphicsItem()
        item.paint(painter, opt, None)  # here in some cases the self is needed
        print(item.boundingRect())
        painter.end()
        return pixmap

    def mouseMoveEvent(self, event):
        # print('move:', event.button())
        # print('move:', event.buttons())
        if event.buttons() == PyQt6.QtCore.Qt.MouseButton.LeftButton and self.drawing:  # `buttons()` instead of `button()`
            if  self.selected:
                if ie_globals.current_tool == "pen":
                    pen_item = QtWidgets.QGraphicsLineItem(QtCore.QLineF(self.start_pos, event.scenePos()))
                    self.selected = pen_item
                    self.addItem(pen_item)
                    self.start_pos = event.scenePos()
                elif ie_globals.current_tool == "line":
                    x = event.scenePos().x()
                    y = event.scenePos().y()
                    self.selected.setLine(QtCore.QLineF(self.start_pos, event.scenePos()))
                    #self.selected.setPos(x - self.selected_offset_x, y - self.selected_offset_y)
                    #rect_item = QtWidgets.QGraphicsRectItem(QtCore.QRectF(x, y, 100, 100))
                    #rect_item.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, True)
                    #line_item = self.selected
                    #line_item= (QtWidgets.QGraphicsLineItem(QtCore.QLineF(self.start_pos, event.scenePos())))
                elif ie_globals.current_tool=="rect":
                    item = self.items()[0]
                    print(item)
                    self.removeItem(item)
                    del item  # Ensure the item is deleted

                    #self.selected.setPos(event.scenePos().x() - self.selected_offset_x, event.scenePos().y() - self.selected_offset_y)
                    width = event.scenePos().x() - self.start_pos.x()
                    height = event.scenePos().y() - self.start_pos.y()
                    rect_item = QtWidgets.QGraphicsRectItem(QtCore.QRectF(self.start_pos.x(), self.start_pos.y(), width, height))
                    # todo : set pen and brush of rect
                    rect_item.setPen(self.pen)
                    rect_item.setBrush(QBrush(QColor(255, 0, 0, 255)))
                    #self.addItem(rect_item)
                    #self.selected = rect_item
                    pixmap:QPixmap = self.convert(rect_item)
                    del rect_item  # Ensure the item is deleted
                    self.addPixmap(pixmap)


                elif ie_globals.current_tool=="circle":
                    self.selected.removeFromIndex() #delete previous circle
                    center_x = (self.start_pos.x() + event.scenePos().x())/2
                    center_y = (self.start_pos.y() + event.scenePos().y())/2
                    radius = math.hypot(self.start_pos.x() - event.scenePos().x(), self.start_pos.y() - event.scenePos().y())
                    print(radius)
                    circle_item = QtWidgets.QGraphicsEllipseItem(
                        QtCore.QRectF(self.start_pos.x() - radius, self.start_pos.y() - radius, radius * 2, radius * 2))
                    #todo : set pen and brush of circle
                    circle_item.setPen(self.pen)
                    circle_item.setBrush(QBrush(QColor(255, 0, 0, 255)))
                    self.addItem(circle_item)
                    self.selected = circle_item

                elif ie_globals.current_tool=="spray":
                    r = int(50 / 2) #todo : set radius of spray
                    x1 = event.scenePos().x()
                    y1 = event.scenePos().y()
                    dens = 100 #todo : set density
                    #todo : set pen and brush of spray

                    for _ in range(dens):
                        x = int(x1 + random.gauss(0, r))
                        y = int(y1 + random.gauss(0, r))
                        #set point to x and y

                        spray_item = QtWidgets.QGraphicsLineItem(QtCore.QLineF(QPoint(x, y), QPoint(x, y)))


                        self.addItem(spray_item)
                    pass

                counter:int=len(self.items())  # type: ignore
                print(counter)
                self.update()


        # super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        # print('release:', event.button())
        # print('release:', event.buttons())
        if event.button() == PyQt6.QtCore.Qt.MouseButton.RightButton:
            if self.selected:
                print('released')
                self.selected.setBrush(QBrush(QColor(255, 255, 255, 255)))
                self.selected = None
        elif event.button() == PyQt6.QtCore.Qt.MouseButton.LeftButton:
            if ie_globals.current_tool == "rect":
                # self.selected.setPos(event.scenePos().x() - self.selected_offset_x, event.scenePos().y() - self.selected_offset_y)
                width = event.scenePos().x() - self.start_pos.x()
                height = event.scenePos().y() - self.start_pos.y()
                rect_item = QtWidgets.QGraphicsRectItem(
                    QtCore.QRectF(self.start_pos.x(), self.start_pos.y(), width, height))
                # todo : set pen and brush of rect
                rect_item.setPen(self.pen)
                rect_item.setBrush(QBrush(QColor(255, 0, 0, 255)))
                # self.addItem(rect_item)
                # self.selected = rect_item
                pixmap: QPixmap = self.convert(rect_item)
                del rect_item  # Ensure the item is deleted
                self.addPixmap(pixmap)
                self.update()
                self.lastindex = -1  # reset last index of added item
        # super().mouseReleaseEvent(event)