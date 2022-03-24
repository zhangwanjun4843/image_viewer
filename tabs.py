
import sys, os

from PySide6.QtWidgets import QApplication
from PySide6.QtUiTools import QUiLoader
from PySide6 import QtGui
from PySide6.QtCore import Qt

from qt_material import apply_stylesheet

def show_screenshot(window):
    img_path = window.lineEdit.text()
    if not os.path.isfile(img_path):
        window.label.setText(f"{img_path}\nis not a valid image path")
        return

    pixmap = QtGui.QPixmap(img_path)
    scaled_pixmap = pixmap.scaled(window.label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
    window.label.setPixmap(scaled_pixmap)

def resize(window, event):
    print("resized")

app = QApplication(sys.argv)

loader = QUiLoader()
window = loader.load("tabs.ui", None)

window.pushButton.clicked.connect(lambda: show_screenshot(window))

apply_stylesheet(app, theme='dark_teal.xml')

window.show()
app.exec()
