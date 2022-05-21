import sys, os

from qt_core import *
from QCCustomWidgets.QCImageViewer import QCImageViewer
from qt_material import apply_stylesheet

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # loading ui files
        loader = QUiLoader()
        self.ui = loader.load("ui_files/main.ui", None)

        self.open_menu = loader.load("ui_files/open_menu.ui", None)
        self.open_menu.hide()


        self.ui.menu_layout.addWidget(self.open_menu)


        self.toggled_menu = None


        # custom widgets
        self.ui.imageViewer = QCImageViewer()
        self.ui.imageViewer.setStyleSheet("border-width: 0px; border-style: solid")

        self.ui.verticalLayout_2.addWidget(self.ui.imageViewer)


        # connect the widgets to their respective functions
        self.ui.imageViewer.files_changed.connect(lambda imgs: self.files_changed(imgs))

        self.ui.left_btn.clicked.connect(lambda: self.ui.imageViewer.step("left"))
        self.ui.right_btn.clicked.connect(lambda: self.ui.imageViewer.step("right"))

        self.ui.add_btn.clicked.connect(lambda: self.show_open_menu())
        self.ui.flip_btn.clicked.connect(lambda: self.flip_image())
        self.ui.rotate_btn.clicked.connect(lambda: self.rotate_image())
        self.ui.export_btn.clicked.connect(lambda: self.export_image())

        self.ui.oppacity_slider.valueChanged.connect(lambda value: self.change_opacity(value))

        self.open_menu.add_image_btn.clicked.connect(lambda: self.add_additional_image())
        self.open_menu.single_image_btn.clicked.connect(lambda: self.show_single_image())




        # keyboard shortcuts
        # This: https://learndataanalysis.org/create-and-assign-keyboard-shortcuts-to-your-pyqt-application-pyqt5-tutorial/
        # article does a great job at showing how keyboard shortcuts work in qt.
        # self.open_shortcut = QShortcut(QKeySequence("Ctrl+O"), self)
        # self.open_shortcut.activated.connect(self.show_image())

        # window options
        self.setWindowTitle("Image Viewer")
        self.setCentralWidget(self.ui)

        self.count = 0

    def add_additional_image(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open image file:")
        self.ui.imageViewer.load_additional_image(path)
        self.ui.imageViewer.setFocus(Qt.OtherFocusReason)

    def show_single_image(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open image file:")
        self.ui.imageViewer.load_single_image(path)
        self.ui.imageViewer.setFocus(Qt.OtherFocusReason)


    def flip_image(self):
        self.ui.imageViewer.flip_image()

    def rotate_image(self):
        self.ui.imageViewer.toggle_rotating()

    def render_image(self):
        self.ui.imageViewer.render_image()

    def change_opacity(self, value):
        self.ui.imageViewer.change_opacity(value * 0.01)

    def export_image(self):
        pixmap = self.ui.imageViewer.export_image()
        QApplication.clipboard().setPixmap(pixmap)

    def files_changed(self, images):
        if len(images) == 1:
            self.setWindowTitle(f"Viewing {os.path.basename(images[0])}")
        else:
            self.setWindowTitle("Viewing multiple images :)")

    def show_open_menu(self):
        # remove all the other menues
        try:
            self.toggled_menu.hide()
        except AttributeError as e:
            print("You shall not pass!")
            pass # fly, you fools

        if self.toggled_menu != self.open_menu:
            self.open_menu.show()
            self.toggled_menu = self.open_menu
        else:
            self.toggled_menu = None
        

def run():
    app = QApplication(sys.argv)
    window = MainWindow()

    apply_stylesheet(app, theme='dark_teal.xml')

    window.showMaximized()
    app.exec()

if __name__ == '__main__':
    run()
