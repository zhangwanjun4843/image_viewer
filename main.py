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

        # custom widgets
        self.ui.imageViewer = QCImageViewer()
        self.ui.imageViewer.setStyleSheet("border-width: 0px; border-style: solid")

        self.ui.verticalLayout_2.addWidget(self.ui.imageViewer)


        self.ui.left_btn.hide()
        self.ui.right_btn.hide()

        # connect the widgets to their respective functions
        self.ui.imageViewer.files_changed.connect(lambda imgs: self.files_changed(imgs))
        self.ui.imageViewer.state_changed.connect(lambda state: self.state_changed(state))

        self.ui.left_btn.clicked.connect(lambda: self.ui.imageViewer.step("left"))
        self.ui.right_btn.clicked.connect(lambda: self.ui.imageViewer.step("right"))

        self.open_image_menu = QMenu()
        self.show_single_image_action = self.open_image_menu.addAction("Open single image", self.show_single_image)
        self.add_additional_image_action = self.open_image_menu.addAction("Add additional image", self.add_additional_image)
        self.add_additional_image_action.setDisabled(True)
        self.ui.add_btn.setMenu(self.open_image_menu)

        self.ui.flip_btn.clicked.connect(lambda: self.flip_image())
        self.ui.rotate_btn.clicked.connect(lambda: self.rotate_image())
        self.ui.export_btn.clicked.connect(lambda: self.export_image())

        # self.ui.oppacity_slider.valueChanged.connect(lambda value: self.change_opacity(value))

        # self.open_menu.add_image_btn.clicked.connect(lambda: self.add_additional_image())
        # self.open_menu.single_image_btn.clicked.connect(lambda: self.show_single_image())

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

        self.ui.right_btn.setChecked(False)
        self.ui.left_btn.setChecked(False)
        self.ui.imageViewer.setFocus(Qt.OtherFocusReason)

    def flip_image(self):
        self.ui.imageViewer.flip_image()

    def rotate_image(self):
        self.ui.imageViewer.toggle_rotating()

    def export_image(self):
        pixmap = self.ui.imageViewer.export_image()
        QApplication.clipboard().setPixmap(pixmap)

    def files_changed(self, images):
        if len(images) == 1:
            self.setWindowTitle(f"Viewing {os.path.basename(images[0])}")
        else:
            self.setWindowTitle("Viewing multiple images :)")

    def state_changed(self, state):
        print(state)
        if state == "single":
            self.ui.left_btn.show()
            self.ui.right_btn.show()
            self.add_additional_image_action.setDisabled(False)
        elif state == "multiple":
            self.ui.left_btn.hide()
            self.ui.right_btn.hide()
            self.add_additional_image_action.setDisabled(False)


        self.ui.add_btn.setChecked(False)


def run():
    app = QApplication(sys.argv)
    window = MainWindow()

    apply_stylesheet(app, theme='dark_teal.xml')

    window.showMaximized()
    app.exec()

if __name__ == '__main__':
    run()
