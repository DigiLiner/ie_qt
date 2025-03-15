import math
import random
from PySide6.QtGui import QImage, QPixmap, QPainter
from PySide6.QtCore import QPoint
from PySide6.QtCore import QRect
import ie_globals
import PySide6.QtCore


def draw_line(img1: QImage, pt1:QPoint, pt2:QPoint,task:str):
    if task == "down":
        painter =QPainter(img1)
        print("drawing line", pt1.x(), pt1.y(), pt2.x(), pt2.y())
        painter.setPen(ie_globals.pen)
        # set the brush of the painter
        painter.setBrush(ie_globals.brush)        
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.drawPoint( pt1.x(), pt1.y())
        painter.end()

    elif task == "move":

        painter =QPainter(img1)
        print("drawing line", pt1.x(), pt1.y(), pt2.x(), pt2.y())
        painter.setPen(ie_globals.pen)
        # set the brush of the painter
        painter.setBrush(ie_globals.brush)        
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.drawLine( pt1.x(), pt1.y(), pt2.x(), pt2.y())
        painter.end()
        
        
        #Soft test 1 - Trying to draw softer line
        # img2=QImage(img1.width(),img1.height(),QImage.Format.Format_RGBA64)
        # painter2: PySide6.QtGui.QPainter = PySide6.QtGui.QPainter(img2)
        # painter2.setPen(ie_globals.pen)
        # # set the brush of the painter
        # painter2.setBrush(ie_globals.brush)
        # painter2.setRenderHint(PySide6.QtGui.QPainter.RenderHint.Antialiasing)
        # painter2.drawLine(pt1, pt2)
        # painter.end()


        #Soft test 2
        #painter.drawImage(0, 0, img2)
        # w = painter.pen().width()
        #
        # for i in range(1, w,10):
        #     painter.begin(img1)
        #     painter.pen().setWidth(i)
        #     painter.setOpacity(0.1-(i/w*0.1 ))
        #     t=painter.pen().width()
        #     print(t,   w,i,i/w,painter.opacity())
        #     painter.drawPoint(pt1)
        #     painter.end()


        #Soft test 3
        #surface_width = painter.device().width()
        #surface_height = painter.device().height()
        # for i in range(0, 359, 10):
        #     x = pt1.x() + math.trunc(2 * w * math.cos(i * math.pi / 180)) - w
        #     y = pt1.y() + math.trunc(2 * w * math.sin(i * math.pi / 180)) - w
        #     if 0 <= x < surface_width and 0 <= y < surface_height:
        #         pt3 = QPoint(x, y)
        #         painter.drawPoint(pt3)
        #painter.end()




    


    elif task == "up":
        pass


def draw_circle(img1: QImage,  pt1:QPoint, pt2:QPoint,task:str):
    if task == "down":
        pass
    elif task == "move":

        painter = QPainter(img1)
        print("drawing line")
        painter.setPen(ie_globals.pen)
        # set the brush of the painter
        painter.setBrush(ie_globals.brush)
        painter.setRenderHint(PySide6.QtGui.QPainter.RenderHint.Antialiasing)
        radius =math.trunc( math.hypot(pt1.x() -pt2.x(), pt1.y() - pt2.y()))
        painter.drawEllipse(pt1,radius,radius)
        # painter.drawEllipse(self.startPoint, event.pos().x()-self.startPoint.x(), event.pos().y()-self.startPoint.y())
        painter.end()
    elif task == "up":
        pass


def draw_rect(img1: PySide6.QtGui.QImage,  pt1:QPoint, pt2:QPoint,task:str):
    if task == "down":
        pass
    elif task == "move":

        painter = PySide6.QtGui.QPainter(img1)
        print("drawing line")
        painter.setPen(ie_globals.pen)
        # set the brush of the painter
        painter.setBrush(ie_globals.brush)
        painter.setRenderHint(PySide6.QtGui.QPainter.RenderHint.Antialiasing)
        rect = QRect(pt1,pt2)
        painter.drawRect(rect)
        painter.end()
    elif task == "up":
        pass

    return None
def draw_spray(img1: PySide6.QtGui.QImage, pt1:QPoint,task:str):
    if task == "down":
        pass
    elif task == "move":

        painter = PySide6.QtGui.QPainter(img1)
        print("drawing spray")
        painter.setPen(ie_globals.pen)
        # set the brush of the painter
        painter.setBrush(ie_globals.brush)
        #todo render hint must be in common setting
        painter.setRenderHint(PySide6.QtGui.QPainter.RenderHint.Antialiasing)
        for i in range(ie_globals.spray_density):
            x = int(pt1.x() + random.gauss(0, ie_globals.spray_radius))
            y = int(pt1.y() + random.gauss(0, ie_globals.spray_radius))

            painter.drawPoint(x, y)

        painter.end()
    elif task == "up":
        pass

    return None


def fill(img1: PySide6.QtGui.QImage, pt1: QPoint, task: str) -> None:
    """

    :rtype: object
    """
    if task == "down":
        painter = PySide6.QtGui.QPainter(img1)
        print("Fill")
        painter.setPen(ie_globals.pen)
        # set the brush of the painter
        painter.setBrush(ie_globals.brush)
        # todo render hint must be in common setting
        painter.setRenderHint(PySide6.QtGui.QPainter.RenderHint.Antialiasing)
        # Now perform the search and fill.
        target_color = img1.pixel(pt1.x(), pt1.y())
        #painter.setPen(QPen(QColor(255,0,0)))
        x:int=pt1.x()
        y:int=pt1.y()
        have_seen: set[tuple[int, int]] = set()
        queue = [(x, y)]
        w = img1.width()
        h = img1.height()
        counter=0
        while queue:
            x, y = queue.pop()
            if img1.pixel(x, y) == target_color:
                painter.drawPoint(x, y)
                # Prepend to the queue
                queue[0:0] = get_cardinal_points(have_seen, (x, y), w, h)
                counter+=1


        painter.end()

        pass
def select_wand(img1: PySide6.QtGui.QImage, pt1: QPoint, task: str) -> None:
    """

    :rtype: object
    """
    if task == "down":
        painter = PySide6.QtGui.QPainter(img1)
        print("Fill")
        painter.setPen(ie_globals.pen)
        # set the brush of the painter
        painter.setBrush(ie_globals.brush)
    
        # todo render hint must be in common setting
        painter.setRenderHint(PySide6.QtGui.QPainter.RenderHint.Antialiasing)
        # Now perform the search and fill.
        target_color = img1.pixel(pt1.x(), pt1.y())
        #painter.setPen(QPen(QColor(255,0,0)))
        x:int=pt1.x()
        y:int=pt1.y()
        have_seen: set[tuple[int, int]] = set()
        border=[(x,y)]
        border.remove((x,y))
        queue = [(x, y)]
        w = img1.width()
        h = img1.height()
        counter=0
        while queue:
            x, y = queue.pop()
            if img1.pixel(x, y) == target_color:
                # Prepend to the queue
                queue[0:0] = get_cardinal_points(have_seen, (x, y), w, h)
                counter+=1
            else:
                border.append((x, y))
        painter.setPen(PySide6.QtGui.QPen(PySide6.QtGui.QColor(255, 0, 0),3))
        print(len(border),counter)
        while border:
            x, y = border.pop()
            painter.drawPoint(x, y) #todo draw uppper layer of selection

        painter.end()

        pass
def get_cardinal_points(have_seen, center_pos, w, h):
    points = []
    cx, cy = center_pos
    for x, y in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
        xx, yy = cx + x, cy + y
        if not(0 <= xx < w and 0 <= yy < h and (xx, yy) not in have_seen):
            continue
        points.append((xx, yy))
        have_seen.add((xx, yy))



    return points


def erase(img1: PySide6.QtGui.QImage, pt1: QPoint, task: str):
    return None