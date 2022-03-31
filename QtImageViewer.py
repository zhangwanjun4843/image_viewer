# https://github.com/marcel-goldschen-ohm/PyQtImageViewer

import os.path

from PySide6.QtCore import Qt, QRectF, Signal
from PySide6.QtGui import QImage, QPixmap, QPainter
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QFileDialog


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
        self.img_path = None

        self.aspectRatioMode = Qt.KeepAspectRatio

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.is_flipped = False

        self.is_rotating = False
        self.rotation = 0

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
    def set_image(self, image):
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
    def load_image_from_file(self, fileName=""):
        if len(fileName) == 0:
            fileName, dummy = QFileDialog.getOpenFileName(self, "Open image file.")
        if len(fileName) and os.path.isfile(fileName):
            self.img_path = fileName
            image = QImage(fileName)
            self.set_image(image)

        if self.is_flipped:
            self.flip_image()

        self.rotate(self.rotation * -1)

        self.zoomStack = []
        self.updateViewer()


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

    def flip_image(self):
        self.scale(-1, 1)
        self.is_flipped = not self.is_flipped

    def toggle_rotating(self):
        self.is_rotating = not self.is_rotating
        

    def reset_rotation(self):
        # dont touch this it works somehow idk why
        if self.is_flipped:
            self.rotate(self.rotation)
        else:
            self.rotate(self.rotation * -1)
        self.rotation = 0

    def render_image(self):
        if self.is_rotating or self.is_flipped:
            print("Exporting flippend and/or rotated images isnt't supported yet")
        else:
            source_rect = self.mapToScene(self.viewport().geometry()).boundingRect()
            image = QImage(source_rect.width(), source_rect.height(), QImage.Format.Format_ARGB32_Premultiplied)
            painter = QPainter(image)

            self.scene.render(painter, image.rect(), source_rect)
            
            painter.end()

            image.save("exported.png")



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


    def mouseDoubleClickEvent(self, event):
        scenePos = self.mapToScene(event.globalPosition().toPoint())
        
        if event.button() == Qt.RightButton:
            self.reset_rotation()

            # reset the zoom of the image
            if self.canZoom:
                self.zoomStack = []
                self.updateViewer()

            

            self.rightMouseButtonDoubleClicked.emit(scenePos.x(), scenePos.y())


        QGraphicsView.mouseDoubleClickEvent(self, event)

    def wheelEvent(self, event):
        # dont touch it it works idk why but it works
        if self.is_rotating:
            rotation_step = 5

            if event.angleDelta().y() > 0:
                if self.is_flipped:
                    self.rotate(-rotation_step)
                    self.rotation += rotation_step
                else:
                    self.rotate(rotation_step)
                    self.rotation += rotation_step

            else:
                if self.is_flipped:
                    self.rotate(rotation_step)
                    self.rotation += -rotation_step
                else:
                    self.rotate(-rotation_step)
                    self.rotation += -rotation_step


                    


        else:
            self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)

            scale_factor = 1.05
            if event.angleDelta().y() > 0:
                self.scale(scale_factor, scale_factor)
            else:
                self.scale(1.0 / scale_factor, 1.0 /  scale_factor)