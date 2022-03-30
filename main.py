import sys

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

        self.ui.open_btn.clicked.connect(lambda: self.show_image())
        self.ui.flip_btn.clicked.connect(lambda: self.flip_image())
        self.ui.rotate_btn.clicked.connect(lambda: self.rotate_image())
        self.ui.export_btn.clicked.connect(lambda: self.render_image())


        self.ui.verticalLayout_2.addWidget(self.ui.imageViewer)
        self.setCentralWidget(self.ui)

    def show_image(self):
        self.ui.imageViewer.load_image_from_file()

    def flip_image(self):
        self.ui.imageViewer.flip_image()

    def rotate_image(self):
        self.ui.imageViewer.toggle_rotating()

    def render_image(self):
        self.ui.imageViewer.render_image()

def run():
    app = QApplication(sys.argv)
    window = MainWindow()


    apply_stylesheet(app, theme='dark_teal.xml')


    window.showMaximized()
    app.exec()

if __name__ == '__main__':
    run()