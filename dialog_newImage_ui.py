# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialog_newImage.ui'
##
## Created by: Qt User Interface Compiler version 6.10.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QComboBox, QDialog,
    QDialogButtonBox, QGroupBox, QLabel, QPlainTextEdit,
    QRadioButton, QSizePolicy, QWidget)
import svgicons_rc

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(264, 320)
        Dialog.setMinimumSize(QSize(260, 320))
        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(10, 270, 221, 41))
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)
        self.comboBoxSizeList = QComboBox(Dialog)
        self.comboBoxSizeList.setObjectName(u"comboBoxSizeList")
        self.comboBoxSizeList.setGeometry(QRect(50, 40, 161, 24))
        self.groupBox = QGroupBox(Dialog)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setEnabled(False)
        self.groupBox.setGeometry(QRect(20, 120, 221, 131))
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 40, 61, 16))
        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(10, 80, 61, 16))
        self.plainTextEditWidth = QPlainTextEdit(self.groupBox)
        self.plainTextEditWidth.setObjectName(u"plainTextEditWidth")
        self.plainTextEditWidth.setGeometry(QRect(80, 30, 104, 31))
        self.plainTextEditHeight = QPlainTextEdit(self.groupBox)
        self.plainTextEditHeight.setObjectName(u"plainTextEditHeight")
        self.plainTextEditHeight.setGeometry(QRect(80, 70, 104, 31))
        self.radioButtonStdSize = QRadioButton(Dialog)
        self.radioButtonStdSize.setObjectName(u"radioButtonStdSize")
        self.radioButtonStdSize.setGeometry(QRect(10, 10, 251, 20))
        self.radioButtonStdSize.setChecked(True)
        self.radioButtonCustomSize = QRadioButton(Dialog)
        self.radioButtonCustomSize.setObjectName(u"radioButtonCustomSize")
        self.radioButtonCustomSize.setGeometry(QRect(10, 90, 201, 20))

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        self.radioButtonStdSize.toggled.connect(self.comboBoxSizeList.setEnabled)
        self.radioButtonCustomSize.toggled.connect(self.groupBox.setEnabled)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"New Image", None))
        self.groupBox.setTitle(QCoreApplication.translate("Dialog", u"Enter Custom Image Size", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Width", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Height", None))
        self.radioButtonStdSize.setText(QCoreApplication.translate("Dialog", u"Standard Size", None))
        self.radioButtonCustomSize.setText(QCoreApplication.translate("Dialog", u"Custom Size", None))
    # retranslateUi

