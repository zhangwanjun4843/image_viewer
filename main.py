import sys, os

from qt_core import *

from QtImageViewer import QtImageViewer

from qt_material import apply_stylesheet

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # loading ui files
        loader = QUiLoader()
        self.ui = loader.load("main_ui.ui", None)

        self.edit_window = loader.load("drawing_tools.ui", None)
        self.ui.verticalLayout.addWidget(self.edit_window)
        
        self.edit_window.hide()
        self.edit_shown = False


        # custom widgets
        self.ui.imageViewer = QtImageViewer()
        self.ui.imageViewer.setStyleSheet("border-width: 0px; border-style: solid")

        self.ui.verticalLayout_2.addWidget(self.ui.imageViewer)


        # connect the widgets to their respective functions
        self.ui.imageViewer.file_changed.connect(lambda new_name: self.image_changed(new_name))

        self.ui.left_btn.clicked.connect(lambda: self.ui.imageViewer.step("left"))
        self.ui.right_btn.clicked.connect(lambda: self.ui.imageViewer.step("right"))

        self.ui.open_btn.clicked.connect(lambda: self.show_image())
        self.ui.flip_btn.clicked.connect(lambda: self.flip_image())
        self.ui.rotate_btn.clicked.connect(lambda: self.rotate_image())
        self.ui.export_btn.clicked.connect(lambda: self.export_image())
        # self.ui.edit_mode_btn.clicked.connect(lambda: self.toggle_edit_mode())

        self.edit_window.line_btn.clicked.connect(lambda: self.ui.imageViewer.set_shape_type("line"))
        self.edit_window.rectangle_btn.clicked.connect(lambda: self.ui.imageViewer.set_shape_type("rectangle"))
        self.edit_window.ellipse_btn.clicked.connect(lambda: self.ui.imageViewer.set_shape_type("ellipse"))

        self.edit_window.line_width_slider.valueChanged.connect(lambda value: self.line_width_slider(value))

        # keyboard shortcuts
        # This: https://learndataanalysis.org/create-and-assign-keyboard-shortcuts-to-your-pyqt-application-pyqt5-tutorial/
        # article does a great job at showing how keyboard shortcuts work in qt.
        # self.open_shortcut = QShortcut(QKeySequence("Ctrl+O"), self)
        # self.open_shortcut.activated.connect(self.show_image())


        # window options
        self.setWindowTitle("Image Viewer")
        self.setCentralWidget(self.ui)

        self.count = 0

    def show_image(self):
        self.ui.imageViewer.file_from_file_dialog()

    def flip_image(self):
        self.ui.imageViewer.flip_image()

    def rotate_image(self):
        self.ui.imageViewer.toggle_rotating()

    def render_image(self):
        self.ui.imageViewer.render_image()

    def export_image(self):
        pixmap = self.ui.imageViewer.export_image()
        QApplication.clipboard().setPixmap(pixmap)

    def toggle_edit_mode(self):
        if self.edit_shown:
            if self.ui.imageViewer.scale_factor != 1:
                self.ui.imageViewer.resize_lock = True

            self.edit_window.hide()

            self.ui.horizontalLayout_2.setStretch(0, 0)
            self.ui.horizontalLayout_2.setStretch(1, 0)

            self.ui.imageViewer.set_shape_type(None)

        else:
            if self.ui.imageViewer.scale_factor != 1:
                self.ui.imageViewer.resize_lock = True

            self.ui.imageViewer.set_shape_type("line")

            self.ui.horizontalLayout_2.setStretch(0, 75)
            self.ui.horizontalLayout_2.setStretch(1, 25)

            self.edit_window.show()


        self.edit_shown = not self.edit_shown



    def line_width_slider(self, value):
        self.edit_window.label.setText(str(value))        

    def image_changed(self, new_name):
        self.setWindowTitle(f"Viewing \"{new_name}\"")
    
def run():
    app = QApplication(sys.argv)
    window = MainWindow()

    apply_stylesheet(app, theme='dark_teal.xml')

    window.showMaximized()
    app.exec()

if __name__ == '__main__':
    run()
