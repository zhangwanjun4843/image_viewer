import sys, os

from PySide6.QtWidgets import QMainWindow, QApplication, QVBoxLayout
from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QPixmap

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
        
        self.ui.verticalLayout_2.addWidget(self.ui.imageViewer)
        self.setCentralWidget(self.ui)

    def show_image(self):
        img_path = self.ui.lineEdit.text()
        if not os.path.isfile(img_path):
            print(f"{img_path} is not a valid path")

        self.ui.imageViewer.loadImageFromFile(img_path)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = MainWindow()


    apply_stylesheet(app, theme='dark_teal.xml')


    window.showMaximized()
    app.exec()
