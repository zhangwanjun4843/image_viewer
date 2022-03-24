import sys, os

from PySide6.QtWidgets import QApplication, QLabel, QMainWindow
from PySide6.QtUiTools import QUiLoader
from PySide6 import QtGui
from PySide6.QtCore import Qt

from qt_material import apply_stylesheet



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        loader = QUiLoader()
        self.ui = loader.load("tabs.ui", None)
        
        self.ui.pushButton.clicked.connect(lambda: self.show_screenshot())

        self.setCentralWidget(self.ui)

    def show_screenshot(self):
        img_path = self.ui.lineEdit.text()
        if not os.path.isfile(img_path):
            self.ui.label.setText(f"{img_path}\nis not a valid image path")
            return

        pixmap = QtGui.QPixmap(img_path)
        scaled_pixmap = pixmap.scaled(self.ui.label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.ui.label.setPixmap(scaled_pixmap)

    def resizeEvent(self, event):
        self.show_screenshot()

        return super().resizeEvent(event)


app = QApplication(sys.argv)
window = MainWindow()

apply_stylesheet(app, theme='dark_teal.xml')

window.showMaximized()
app.exec()
