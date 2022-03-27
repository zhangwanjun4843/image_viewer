import sys, os, pprint

from PySide6.QtWidgets import QMainWindow, QApplication
from PySide6.QtUiTools import QUiLoader

from QtImageViewer import QtImageViewer

from qt_material import apply_stylesheet

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        loader = QUiLoader()
        self.ui = loader.load("main_ui.ui", None)

        self.ui.imageViewer = QtImageViewer()
        self.ui.imageViewer.setStyleSheet("border-width: 0px; border-style: solid")

        self.ui.pushButton.clicked.connect(lambda: self.show_image())
        self.ui.pushButton_2.clicked.connect(lambda: self.flip_image())

        self.ui.verticalLayout_2.addWidget(self.ui.imageViewer)
        self.setCentralWidget(self.ui)

    def show_image(self):
        self.ui.imageViewer.loadImageFromFile()

    def flip_image(self):
        self.ui.imageViewer.scale(-1, 1)

if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = MainWindow()


    apply_stylesheet(app, theme='dark_teal.xml')


    window.showMaximized()
    app.exec()
