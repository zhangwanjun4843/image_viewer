# https://github.com/marcel-goldschen-ohm/PyQtImageViewer

from math import degrees
import os.path, sys
from turtle import width

from PySide6.QtCore import Qt, QRectF, Signal, QMargins, QPointF, QSizeF, QLineF
from PySide6.QtGui import QImage, QPixmap, QPainterPath, QPen, QBrush, QTransform
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QFileDialog, QApplication, QMainWindow, QVBoxLayout, QGraphicsTransform
from PySide6.QtUiTools import QUiLoader

from qt_material import apply_stylesheet

class QtImageViewer(QGraphicsView):
    leftMouseButtonPressed = Signal(float, float)
    rightMouseButtonPressed = Signal(float, float)
    leftMouseButtonReleased = Signal(float, float)
    rightMouseButtonReleased = Signal(float, float)
    leftMouseButtonDoubleClicked = Signal(float, float)
    rightMouseButtonDoubleClicked = Signal(float, float)

    def __init__(self):
        QGraphicsView.__init__(self)

        self.scene = QGraphicsScene()
        self.setScene(self.scene)

        self._pixmapHandle = None

        self.aspectRatioMode = Qt.KeepAspectRatio

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.h11 = 1.0
        self.h12 = 0
        self.h21 = 1.0
        self.h22 = 0

        self.zoomStack = []

        self.canZoom = True
        self.canPan = True

    # return weather or not there is an image currently being displayed
    def hasImage(self):
        return self._pixmapHandle is not None

    # remove the curerent image from the image viewer
    def clearImage(self):
        if self.hasImage():
            self.scene.removeItem(self._pixmapHandle)
            self._pixmapHandle = None

    # return the iamge currently being displayed as a pixmap
    def pixmap(self):
        if self.hasImage():
            return self._pixmapHandle.pixmap()
        return None

    # return the image currently being displayed as QImage
    def image(self):
        if self.hasImage():
            return self._pixmapHandle.pixmap().toImage()
        return None

    # set an image to be displayed on the image viewer
    def setImage(self, image):
        # convert the iamge to pixmap
        if type(image) is QPixmap:
            pixmap = image 
        elif type(image) is QImage:
            pixmap = QPixmap.fromImage(image)
        else:
            raise RuntimeError("ImageViewer.setImage: Argument must be a QImage or QPixmap.")

        # dunno what this does
        if self.hasImage():
            self._pixmapHandle.setPixmap(pixmap)
        else:
            self._pixmapHandle = self.scene.addPixmap(pixmap)
        
        # adjust the view of the scene to the pixmap
        self.setSceneRect(QRectF(pixmap.rect()))
        self.updateViewer()

    # load an image from a filepath
    def loadImageFromFile(self, fileName=""):
        if len(fileName) == 0:
            fileName, dummy = QFileDialog.getOpenFileName(self, "Open image file.")
        if len(fileName) and os.path.isfile(fileName):
            image = QImage(fileName)
            self.setImage(image)

    # update the zoom of the image viewer
    def updateViewer(self):
        # return if the image viewer isnt currently displaying an image
        if not self.hasImage():
            return

        # adjust the zoom of the image viewer to the latest rect on the zoom stack
        if len(self.zoomStack) and self.sceneRect().contains(self.zoomStack[-1]):
            self.fitInView(self.zoomStack[-1], self.aspectRatioMode)
        else:
            # reset the zoom if the zoom stack is empty
            self.zoomStack = []
            self.fitInView(self.sceneRect(), self.aspectRatioMode)

    # Events

    def resizeEvent(self, event):
        self.updateViewer()


    def mousePressEvent(self, event):
        scenePos = self.mapToScene(event.globalPosition().toPoint())

        # pan if the left button has been pressed
        if event.button() == Qt.LeftButton:
            if self.canPan:
                self.setDragMode(QGraphicsView.ScrollHandDrag)
            self.leftMouseButtonPressed.emit(scenePos.x(), scenePos.y())


        # zoom if the right mouse button has been pressed
        elif event.button() == Qt.RightButton:
            if self.canZoom:
                self.setDragMode(QGraphicsView.RubberBandDrag)
            self.rightMouseButtonPressed.emit(scenePos.x(), scenePos.y())


        # send the mouse press event
        QGraphicsView.mousePressEvent(self, event)


    def mouseReleaseEvent(self, event):
        QGraphicsView.mouseReleaseEvent(self, event)

        scenePos = self.mapToScene(event.globalPosition().toPoint())

        # stop dragging if the left mouse button has been released
        if event.button() == Qt.LeftButton:
            self.setDragMode(QGraphicsView.NoDrag)

            # send the left mouse button released event
            self.leftMouseButtonReleased.emit(scenePos.x(), scenePos.y())

        # zoom if the right mouse button has been released
        elif event.button() == Qt.RightButton:
            if self.canZoom:
                # get the current view area
                viewBBox = self.zoomStack[-1] if len(self.zoomStack) else self.sceneRect()
                
                # get the selected area realative to the current view area
                selectionBBox = self.scene.selectionArea().boundingRect().intersected(viewBBox)

                # clear the selction area
                self.scene.setSelectionArea(QPainterPath())

                # if the selection area is valid and the selection area isnt the view area
                if selectionBBox.isValid() and (selectionBBox != viewBBox):
                    # append the selection area to the zoom stack and update the viewer
                    self.zoomStack.append(selectionBBox)
                    self.updateViewer()

            # reset the drag mode and send the right mouse button release event
            self.setDragMode(QGraphicsView.NoDrag)
            self.rightMouseButtonReleased.emit(scenePos.x(), scenePos.y())


    def mouseDoubleClickEvent(self, event):
        scenePos = self.mapToScene(event.globalPosition().toPoint())

        if event.button() == Qt.LeftButton:
            # send the left mouse button double clicked event
            self.leftMouseButtonDoubleClicked.emit(scenePos.x(), scenePos.y())
        
        elif event.button() == Qt.RightButton:
            # reset the zoom of the image
            if self.canZoom:
                self.zoomStack = []
                self.updateViewer()

            self.rightMouseButtonDoubleClicked.emit(scenePos.x(), scenePos.y())


        QGraphicsView.mouseDoubleClickEvent(self, event)

    def wheelEvent(self, event):
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)

        scale_factor = 1.05
        if event.angleDelta().y() > 0:
            self.scale(scale_factor, scale_factor)
        else:
            self.scale(1.0 / scale_factor, 1.0 /  scale_factor)