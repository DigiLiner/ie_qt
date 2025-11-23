from abc import ABC, abstractmethod
from PySide6.QtGui import QMouseEvent, QPaintEvent
from PySide6.QtWidgets import QWidget

class Tool(ABC):
    def __init__(self, editor: QWidget):
        self.editor = editor

    @abstractmethod
    def mousePressEvent(self, event: QMouseEvent):
        pass

    @abstractmethod
    def mouseMoveEvent(self, event: QMouseEvent):
        pass

    @abstractmethod
    def mouseReleaseEvent(self, event: QMouseEvent):
        pass

    @abstractmethod
    def paintEvent(self, event: QPaintEvent):
        pass
