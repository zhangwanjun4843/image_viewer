# https://github.com/marcel-goldschen-ohm/PyQtImageViewer
import os

from PySide6.QtCore import Qt, QRectF, Signal, QPointF
from PySide6.QtGui import QImage, QPixmap, QKeyEvent
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QFileDialog


class QtImageViewer(QGraphicsView):
    keyPressed = Signal(QKeyEvent)

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
        self.rotation_step = 5

        self.shapes = []

        self.is_drawing = False
        self.shape_start = None
        self.shape = None
        self.shape_type = None

        self.files = []


    def has_image(self):
        return self._pixmapHandle is not None

    def clear_image(self):
        if self.has_image():
            self.scene.removeItem(self._pixmapHandle)
            self._pixmapHandle = None

    # return the image currently being displayed as a pixmap
    def pixmap(self):
        if self.has_image():
            return self._pixmapHandle.pixmap()
        return None

    # return the image currently being displayed as QImage
    def image(self):
        if self.has_image():
            return self._pixmapHandle.pixmap().toImage()
        return None

    # set an image to be displayed on the image viewer
    def set_image(self, image):
        # convert the iamge to pixmap
        if type(image) is QPixmap:
            pixmap = image 
        elif type(image) is QImage:
            pixmap = QPixmap.fromImage(image)

        # dunno what this does
        if self.has_image():
            self._pixmapHandle.setPixmap(pixmap)
        else:
            self._pixmapHandle = self.scene.addPixmap(pixmap)
        
        # adjust the view of the scene to the pixmap
        self.setSceneRect(QRectF(pixmap.rect()))
        self.fitInView(self.sceneRect(), self.aspectRatioMode)

    # load an image from a filepath
    def load_image_from_file(self, file_name=""):
        if len(file_name) == 0:
            file_name, dummy = QFileDialog.getOpenFileName(self, "Open image file:")

        if len(file_name) and os.path.isfile(file_name):
            dir_name = os.path.dirname(file_name)
            self.files = [f for f in os.listdir(dir_name) if f.split(".")[-1] in ["png", "jpg"]]

            self.img_path = file_name
            image = QImage(file_name)
            self.set_image(image)

        self.reset_viewer(zoom = True, flip = True, rotation = True)

    def flip_image(self):
        self.scale(-1, 1)
        self.is_flipped = not self.is_flipped

    def toggle_rotating(self):
        self.is_rotating = not self.is_rotating
        
    def reset_viewer(self, rotation, zoom, flip):
        if flip:
            if self.is_flipped:
                    self.flip_image()

        if rotation:
            # dont touch this it works somehow idk why
            if self.is_flipped:
                self.rotate(self.rotation)
            else:
                self.rotate(self.rotation * -1)
            self.rotation = 0

        if zoom:
            self.fitInView(self.sceneRect(), self.aspectRatioMode)

    # returns the viewport as pixmap
    def export_image(self):
        pixmap = QPixmap(self.viewport().size())
        self.viewport().render(pixmap)

        return pixmap

    def set_shape_type(self, shape):
        self.shape_type = shape


    # THE FOLLOWING CODE IS TERRIBLE. REWRITE UNDER ALL CIRCUMSTANCES (except temporary laziness, I need a loophole shut up)
    # ----------------------------------------------
    def step_left(self):
        file_name = os.path.basename(self.img_path)
        index = self.files.index(file_name)

        print(index, len(self.files))
        if index + 1 < 0:
            return

        try:
            new_file = self.files[index - 1]
        except IndexError:
            return

        new_file = os.path.join(os.path.dirname(self.img_path), new_file)

        self.img_path = new_file
        image = QImage(new_file)
        self.set_image(image)



    def step_right(self):
        file_name = os.path.basename(self.img_path)
        index = self.files.index(file_name)

        print(index, len(self.files))
        if index + 1 > len(self.files):
            return

        try:
            new_file = self.files[index + 1]
        except IndexError:
            new_file = self.files[0]

        new_file = os.path.join(os.path.dirname(self.img_path), new_file)

        self.img_path = new_file
        image = QImage(new_file)
        self.set_image(image)
    # ----------------------------------------------



    # Events
    def resizeEvent(self, event):
        self.fitInView(self.sceneRect(), self.aspectRatioMode)

    def mousePressEvent(self, event):
        scenePos = self.mapToScene(event.pos())

        if event.button() == Qt.LeftButton:
            self.setDragMode(QGraphicsView.ScrollHandDrag)

        elif event.button() == Qt.RightButton:
            self.is_drawing = True
            self.shape_start = (scenePos.x(), scenePos.y())

        QGraphicsView.mousePressEvent(self, event)


    def mouseReleaseEvent(self, event):
        QGraphicsView.mouseReleaseEvent(self, event)

        if event.button() == Qt.LeftButton:
            self.setDragMode(QGraphicsView.NoDrag)

        elif event.button() == Qt.RightButton:
            self.shapes.append(self.shape)
            self.is_drawing = False

            self.shape_start = None
            self.shape = None


    def mouseDoubleClickEvent(self, event):        
        if event.button() == Qt.LeftButton:
            for line in self.shapes:
                self.scene.removeItem(line)

            self.shapes = []

        elif event.button() == Qt.RightButton:
            self.reset_viewer(rotation = True, flip = False, zoom = True)
            
        QGraphicsView.mouseDoubleClickEvent(self, event)


    def wheelEvent(self, event):
        # dont touch it it works idk why but it works
        if self.is_rotating:
            if event.angleDelta().y() > 0:
                if self.is_flipped:
                    self.rotate(-self.rotation_step)
                    self.rotation += self.rotation_step
                else:
                    self.rotate(self.rotation_step)
                    self.rotation += self.rotation_step

            else:
                if self.is_flipped:
                    self.rotate(self.rotation_step)
                    self.rotation -= self.rotation_step
                else:
                    self.rotate(-self.rotation_step)
                    self.rotation -= self.rotation_step

        else:
            self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)

            scale_factor = 1.05
            if event.angleDelta().y() > 0:
                self.scale(scale_factor, scale_factor)
            else:
                self.scale(1.0 / scale_factor, 1.0 / scale_factor)

    def mouseMoveEvent(self, event):
        scenePos = self.mapToScene(event.pos())

        if self.is_drawing:
            if self.shape != None:
                self.scene.removeItem(self.shape)


            if self.shape_type == "line":
                self.shape = self.scene.addLine(
                    self.shape_start[0],
                    self.shape_start[1],
                    scenePos.x(),
                    scenePos.y()
                )
            elif self.shape_type == "rectangle":
                self.shape = self.scene.addRect(
                    self.shape_start[0],
                    self.shape_start[1],
                    (scenePos.x() - self.shape_start[0]),
                    (scenePos.y() - self.shape_start[1])
                )
            elif self.shape_type == "ellipse":
                self.shape = self.scene.addEllipse(
                    self.shape_start[0],
                    self.shape_start[1],
                    (scenePos.x() - self.shape_start[0]),
                    (scenePos.y() - self.shape_start[1])
                )

        QGraphicsView.mouseMoveEvent(self, event)

    def keyPressEvent(self, event):
        print("test")
        self.keyPressed.emit(event)