import sys

from qt_core import *
from QCCustomWidgets.QCImageViewer import QCImageViewer
from qt_material import apply_stylesheet

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # loading ui files
        loader = QUiLoader()
        self.ui = loader.load("ui_files/main.ui", None)

        # custom widgets
        self.ui.imageViewer = QCImageViewer()
        self.ui.imageViewer.setStyleSheet("border-width: 0px; border-style: solid")

        self.ui.verticalLayout_2.addWidget(self.ui.imageViewer)


        # connect the widgets to their respective functions
        self.ui.imageViewer.files_changed.connect(lambda imgs: self.files_changed(imgs))

        self.ui.left_btn.clicked.connect(lambda: self.ui.imageViewer.step("left"))
        self.ui.right_btn.clicked.connect(lambda: self.ui.imageViewer.step("right"))

        self.ui.add_btn.clicked.connect(lambda: self.add_image())
        self.ui.flip_btn.clicked.connect(lambda: self.flip_image())
        self.ui.rotate_btn.clicked.connect(lambda: self.rotate_image())
        self.ui.export_btn.clicked.connect(lambda: self.export_image())

        # keyboard shortcuts
        # This: https://learndataanalysis.org/create-and-assign-keyboard-shortcuts-to-your-pyqt-application-pyqt5-tutorial/
        # article does a great job at showing how keyboard shortcuts work in qt.
        # self.open_shortcut = QShortcut(QKeySequence("Ctrl+O"), self)
        # self.open_shortcut.activated.connect(self.show_image())

        # window options
        self.setWindowTitle("Image Viewer")
        self.setCentralWidget(self.ui)

        self.count = 0

    def add_image(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open image file:")
        self.ui.imageViewer.load_image(path)
        self.ui.imageViewer.setFocus(Qt.OtherFocusReason)

    def flip_image(self):
        self.ui.imageViewer.flip_image()

    def rotate_image(self):
        self.ui.imageViewer.toggle_rotating()

    def render_image(self):
        self.ui.imageViewer.render_image()

    def export_image(self):
        pixmap = self.ui.imageViewer.export_image()
        QApplication.clipboard().setPixmap(pixmap)

    def files_changed(self, images):
        print(images)

    
def run():
    app = QApplication(sys.argv)
    window = MainWindow()

    apply_stylesheet(app, theme='dark_teal.xml')

    window.showMaximized()
    app.exec()

if __name__ == '__main__':
    run()
