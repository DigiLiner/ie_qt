import math
from tracemalloc import Frame

import PySide6
from PySide6.QtCore import QPointF
from PySide6.QtGui import QPainter, QPen, Qt, QPolygonF
from PySide6.QtWidgets import QFrame

import ie_globals
from ui_main import Ui_MainWindow


class ColorMatrixPanel:
    def __init__(self, parent):

# Dock the ColorMatrixPanel to the right of the parent window
        self.colors = [ # Standard HCIE colors
     "#FFFFFF", "#FFC0C0", "#FFE0C0", "#FFFFC0",
     "#E0E0E0", "#FF8080", "#FFC080", "#FFFF80",
     "#C0C0C0", "#FF0000", "#FF8000", "#FFFF00",
     "#808080", "#C00000", "#C04000", "#C0C000",
     "#404040", "#800000", "#804000", "#808000",
     "#000000", "#400000", "#646464", "#404000",

     "#C0FFC0", "#C0FFFF", "#D3D5F5", "#FFC0FF",
     "#80FF80", "#80FFFF", "#AAAEEB", "#FF80FF",
     "#00FF00", "#00FFFF", "#8389E0", "#FF00FF",
     "#00C000", "#00C0C0", "#232B99", "#C000C0",
     "#008000", "#008080", "#101566", "#800080",
     "#004000", "#004040", "#04051A", "#400040",
      ]
        self.mw= Ui_MainWindow
        self.mw.lineWidth=1 #
        #SetBackgroundColour(wx.WHITE)
        self.colorWidth = 21
        self.colorHeight = 25
        self.frameColors.width=self.colorWidth*4+4
        self.frameColors.height=self.colorHeight*12+4+30

        #self.Bind(wx.EVT_PAINT, self.on_paint)
        #self.Bind(wx.EVT_LEFT_DOWN, self.on_click)

    def on_click(self, event):
        x, y = event.GetPosition()
        color_index = (y // self.colorHeight) * 4 + (x // self.colorWidth)
        if 0 <= color_index < len(self.colors):
            ie_globals.pen.Colour = self.colors[color_index]
        self.Refresh()

    def on_paint(self, event):

        painter = QPainter(self.frameColors)
        painter.setPen(QPen(Qt.red, 4))
        painter.setRenderHint(QPainter.Antialiasing)
        #
        polyline = QPolygonF()
        h_div_2 = self.height() // 2
        samples = self.width() * 10
        #
        for x in range(samples):
             y = h_div_2 + math.sin(x * 6.28 / samples) * h_div_2
             polyline.append(QPointF(x * self.width() / samples, y))
        #
        painter.drawPolyline(polyline)

        #
        # dc = wx.PaintDC(self)
        # for i in range(12):
        #     for j in range(4):
        #         color_str = self.colors[i * 4 + j]
        #         if len(color_str) == 9:  # Check if it's in ARGB format #AARRGGBB
        #             alpha = int(color_str[1:3], 16)
        #             red = int(color_str[3:5], 16)
        #             green = int(color_str[5:7], 16)
        #             blue = int(color_str[7:9], 16)
        #             color = wx.Colour(red, green, blue, alpha)
        #         else: #RRGGBB
        #             color = wx.Colour(color_str)
        #
        #         rect = wx.Rect(j * self.colorWidth-1, i * self.colorHeight-1, self.colorWidth, self.colorHeight)
        #         dc.SetPen(wx.Pen((120, 120, 120), 1))
        #         dc.SetBrush(wx.Brush(color))
        #         dc.DrawRectangle(rect)
        #
        # bottom = self.colorHeight * 12
        # dc.SetPen(wx.Pen((120, 120, 120), 1))
        # dc.SetBrush(wx.Brush(ie_globals.pen.Colour))
        # dc.DrawRectangle(0,bottom, 40, 20)

