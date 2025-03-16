import math
import os
import sys

import PySide6
from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import QPoint
from PySide6.QtGui import QPen, QColor, QBrush, Qt, QImage, QPainter, QMouseEvent, QPixmap
from PySide6.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QSizePolicy, QLabel, QHBoxLayout, QScrollArea, \
    QGridLayout
from PySide6.QtWidgets import QFrame
import ie_functions
import ie_globals
from main_ui import Ui_MainWindow
class IEditor(QFrame()):
    def __init__(self, image_path):
        self.image_path = image_path
        # You can add more initialization code here
        self.scrollarea = QScrollArea()
        scrollareacontent = QtWidgets.QWidget()
        gridLayout = QGridLayout(scrollareacontent)
        widgetPicture = QFrame(scrollareacontent)


