import math
import random
from collections import deque
from typing import Set,Tuple

from PySide6.QtGui import QImage, QPixmap, QPainter, QColor
from PySide6.QtCore import QPoint
from PySide6.QtCore import QRect
import ie_globals
import PySide6.QtCore


# import the module
#from ctypes import cdll

# load the library
#lib = cdll.LoadLibrary('./libgeek.so')
#https://www.geeksforgeeks.org/how-to-call-c-c-from-python/

def draw_line(img1: QImage, pt1:QPoint, pt2:QPoint,task:str):
    if task == "down":
        painter =QPainter(img1)
        print("drawing line", pt1.x(), pt1.y(), pt2.x(), pt2.y())
        painter.setPen(ie_globals.current_pen)
        # set the brush of the painter
        painter.setBrush(ie_globals.current_brush)        
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.drawPoint( pt1.x(), pt1.y())
        painter.end()

    elif task == "move":

        painter =QPainter(img1)
        print("drawing line", pt1.x(), pt1.y(), pt2.x(), pt2.y())
        painter.setPen(ie_globals.current_pen)
        # set the brush of the painter
        painter.setBrush(ie_globals.current_brush)        
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.drawLine( pt1.x(), pt1.y(), pt2.x(), pt2.y())
        painter.end()
        
        
        #Soft test 1 - Trying to draw softer line
        # img2=QImage(img1.width(),img1.height(),QImage.Format.Format_RGBA64)
        # painter2: PySide6.QtGui.QPainter = PySide6.QtGui.QPainter(img2)
        # painter2.setPen(ie_globals.current_pen)
        # # set the brush of the painter
        # painter2.setBrush(ie_globals.current_brush)
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
        painter.setPen(ie_globals.current_pen)
        # set the brush of the painter
        painter.setBrush(ie_globals.current_brush)
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
        painter.setPen(ie_globals.current_pen)
        # set the brush of the painter
        painter.setBrush(ie_globals.current_brush)
        painter.setRenderHint(PySide6.QtGui.QPainter.RenderHint.Antialiasing)
        rect = QRect(pt1,pt2)
        painter.drawRect(rect)
        painter.end()
    elif task == "up":
        pass

    return None
def draw_round_rect(img1: PySide6.QtGui.QImage,  pt1:QPoint, pt2:QPoint,task:str,corner_radius:int=10):
    if task == "move":
        painter= PySide6.QtGui.QPainter(img1)
        print("drawing round rect")
        painter.setPen(ie_globals.current_pen)
        # set the brush of the painter
        painter.setBrush(ie_globals.current_brush)
        painter.setRenderHint(PySide6.QtGui.QPainter.RenderHint.Antialiasing)
        rect = QRect(pt1,pt2)
        painter.drawRoundedRect(rect,corner_radius,corner_radius)
        painter.end()

    elif task == "up":
        pass

def draw_spray(img1: PySide6.QtGui.QImage, pt1:QPoint,task:str):
    if task == "down":
        pass
    elif task == "move":

        painter = PySide6.QtGui.QPainter(img1)
        print("drawing spray")
        painter.setPen(ie_globals.current_pen)
        # set the brush of the painter
        painter.setBrush(ie_globals.current_brush)
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


def select_wand(img1: PySide6.QtGui.QImage, pt1: QPoint, task: str) -> None:
    """

    :rtype: object
    """
    if task == "down":
        painter = PySide6.QtGui.QPainter(img1)
        print("Wand")
        temp_pen = PySide6.QtGui.QPen(QColor(255, 0, 0) ,1, PySide6.QtCore.Qt.PenStyle.DotLine)

        painter.setPen(temp_pen)
        # set the brush of the painter
        painter.setBrush(ie_globals.current_brush)
        # todo render hint must be in common setting
        painter.setRenderHint(PySide6.QtGui.QPainter.RenderHint.Antialiasing)
        # Now perform the search and fill.
        target_color = img1.pixel(pt1.x(), pt1.y())
        # painter.setPen(QPen(QColor(255,0,0)))

        x: int = pt1.x()
        y: int = pt1.y()
        have_seen: set[tuple[int, int]] = set()
        border = [(x, y)]
        border.remove((x, y))
        queue = [(x, y)]
        w = img1.width()
        h = img1.height()
        counter = 0
        while queue:
            x, y = queue.pop()
            if img1.pixel(x, y) == target_color:

                # Prepend to the queue
                queue[0:0] = get_cardinal_points(have_seen, (x, y), w, h)
                counter += 1
            else:
                border.append((x, y))



        painter.setPen(PySide6.QtGui.QPen(PySide6.QtGui.QColor(255, 0, 0), 3))
        print(len(border), counter)
        while border:
            x, y = border.pop()
            #add points to the path
            painter.drawPoint(x, y)  # todo draw uppper layer of selection

        painter.end()

        pass
def fill(img1: PySide6.QtGui.QImage, pt1: QPoint, task: str,tolerance:int=100) -> None:
    """
    Fills an area of the image starting from the point `pt1` with the specified `task`.
    Currently supports the "down" task which uses flood fill algorithm to fill connected pixels
    of similar color.

    :param img1: The image to be filled.
    :param pt1: The starting point for the fill operation.
    :param task: The task to perform, currently only "down" is supported.
    :param tolerance: The tolerance for the color comparison.
    :rtype: None
    """
    if task == "down":
        painter = PySide6.QtGui.QPainter(img1)
        print("Fill")

        temp_pen = ie_globals.current_pen ## todo: dikkat
        temp_pen.setWidth(1)  # important
        painter.setPen(temp_pen)

        # set the brush of the painter
        painter.setBrush(ie_globals.current_brush)
        # todo render hint must be in common setting
        painter.setRenderHint(PySide6.QtGui.QPainter.RenderHint.Antialiasing)
        # Now perform the search and fill.
        target_color = QColor(img1.pixelColor(pt1.x(), pt1.y()))

        x = int(pt1.x())
        y = int(pt1.y())
        have_seen: Set[Tuple[int, int]] = set()  # Added type hint here
        queue = deque([(x, y)])
        w = img1.width()
        h = img1.height()
        counter = 0
        tolerance= ie_globals.fill_tolerance
        r2, g2, b2, a2 = target_color.red(), target_color.green(), target_color.blue(), target_color.alpha()
        while queue:
            x, y = queue.popleft()
            color1 = QColor(img1.pixelColor(x, y))
            

            if  (tolerance == 0) :                
                if (color1 == target_color ):
                    painter.drawPoint(x, y)
                    # Prepend to the queue
                    queue.extend(get_cardinal_points(have_seen, (x, y), w, h))  # Use extend to append multiple elements
            
            else:
                r1, g1, b1, a1 = color1.red(), color1.green(), color1.blue(), color1.alpha()
                if (abs(r1 - r2) <= tolerance) and (abs(g1 - g2) <= tolerance) and \
                    (abs(b1 - b2) <= tolerance) and (abs(a1 - a2) <= tolerance) :
                    painter.drawPoint(x, y)
                    # Prepend to the queue
                    queue.extend(get_cardinal_points(have_seen, (x, y), w, h))  # Use extend to append multiple elements    

        painter.end()
        del temp_pen 

def get_cardinal_points(have_seen, center_pos, w, h):
    """
    Returns the cardinal points around the center position that are within the image bounds and not yet seen.

    :param have_seen: A set of points that have already been processed.
    :param center_pos: A tuple representing the center position (x, y).
    :param w: Width of the image.
    :param h: Height of the image.
    :return: A list of cardinal points that are within bounds and not seen.
    """
    try:
        points = []
        cx, cy = center_pos

        # Define the cardinal directions
        cardinal_directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]

        for x, y in cardinal_directions:
            xx, yy = cx + x, cy + y

            # Check if the point is within the image bounds and not in have_seen
            if 0 <= xx < w and 0 <= yy < h and (xx, yy) not in have_seen:
                points.append((xx, yy))
                have_seen.add((xx, yy))

        return points

    except Exception as e:
        print(f"An error occurred in get_cardinal_points: {e}")
        return []



def erase(img1: PySide6.QtGui.QImage, pt1: QPoint, task: str):
    return None