# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.4.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QMainWindow, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(669, 518)
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.actionOpen = QAction(MainWindow)
        self.actionOpen.setObjectName(u"actionOpen")
        self.actionSave = QAction(MainWindow)
        self.actionSave.setObjectName(u"actionSave")
        self.actionFlip = QAction(MainWindow)
        self.actionFlip.setObjectName(u"actionFlip")
        self.actionRotate = QAction(MainWindow)
        self.actionRotate.setObjectName(u"actionRotate")
        self.actionRotate.setCheckable(True)
        self.ui = QWidget(MainWindow)
        self.ui.setObjectName(u"ui")
        self.ui.setMinimumSize(QSize(400, 500))
        self.horizontalLayout_2 = QHBoxLayout(self.ui)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.flip_btn = QPushButton(self.ui)
        self.flip_btn.setObjectName(u"flip_btn")
        self.flip_btn.setCheckable(True)

        self.horizontalLayout_6.addWidget(self.flip_btn)

        self.rotate_btn = QPushButton(self.ui)
        self.rotate_btn.setObjectName(u"rotate_btn")
        self.rotate_btn.setCheckable(True)
        self.rotate_btn.setChecked(False)

        self.horizontalLayout_6.addWidget(self.rotate_btn)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_2)


        self.horizontalLayout_5.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.left_btn = QPushButton(self.ui)
        self.left_btn.setObjectName(u"left_btn")

        self.horizontalLayout_8.addWidget(self.left_btn)

        self.right_btn = QPushButton(self.ui)
        self.right_btn.setObjectName(u"right_btn")

        self.horizontalLayout_8.addWidget(self.right_btn)


        self.horizontalLayout_5.addLayout(self.horizontalLayout_8)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer)

        self.export_btn = QPushButton(self.ui)
        self.export_btn.setObjectName(u"export_btn")

        self.horizontalLayout_7.addWidget(self.export_btn)

        self.add_btn = QPushButton(self.ui)
        self.add_btn.setObjectName(u"add_btn")

        self.horizontalLayout_7.addWidget(self.add_btn)


        self.horizontalLayout_5.addLayout(self.horizontalLayout_7)


        self.verticalLayout_3.addLayout(self.horizontalLayout_5)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")

        self.verticalLayout_3.addLayout(self.verticalLayout_2)


        self.horizontalLayout_2.addLayout(self.verticalLayout_3)

        self.menu_layout = QVBoxLayout()
        self.menu_layout.setObjectName(u"menu_layout")

        self.horizontalLayout_2.addLayout(self.menu_layout)

        MainWindow.setCentralWidget(self.ui)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionOpen.setText(QCoreApplication.translate("MainWindow", u"Open", None))
        self.actionSave.setText(QCoreApplication.translate("MainWindow", u"Save as", None))
        self.actionFlip.setText(QCoreApplication.translate("MainWindow", u"Flip", None))
        self.actionRotate.setText(QCoreApplication.translate("MainWindow", u"Rotate", None))
        self.flip_btn.setText(QCoreApplication.translate("MainWindow", u"Flip", None))
#if QT_CONFIG(shortcut)
        self.flip_btn.setShortcut(QCoreApplication.translate("MainWindow", u"F", None))
#endif // QT_CONFIG(shortcut)
        self.rotate_btn.setText(QCoreApplication.translate("MainWindow", u"Rotate", None))
#if QT_CONFIG(shortcut)
        self.rotate_btn.setShortcut(QCoreApplication.translate("MainWindow", u"R", None))
#endif // QT_CONFIG(shortcut)
        self.left_btn.setText(QCoreApplication.translate("MainWindow", u"<", None))
#if QT_CONFIG(shortcut)
        self.left_btn.setShortcut(QCoreApplication.translate("MainWindow", u"Left", None))
#endif // QT_CONFIG(shortcut)
        self.right_btn.setText(QCoreApplication.translate("MainWindow", u">", None))
#if QT_CONFIG(shortcut)
        self.right_btn.setShortcut(QCoreApplication.translate("MainWindow", u"Right", None))
#endif // QT_CONFIG(shortcut)
        self.export_btn.setText(QCoreApplication.translate("MainWindow", u"Export", None))
#if QT_CONFIG(shortcut)
        self.export_btn.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+C", None))
#endif // QT_CONFIG(shortcut)
        self.add_btn.setText(QCoreApplication.translate("MainWindow", u"Add Image", None))
#if QT_CONFIG(shortcut)
        self.add_btn.setShortcut(QCoreApplication.translate("MainWindow", u"O", None))
#endif // QT_CONFIG(shortcut)
    # retranslateUi

