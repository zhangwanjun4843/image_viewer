# https://github.com/marcel-goldschen-ohm/PyQtImageViewer
import os
from typing import overload

from qt_core import *

class QtImageViewer(QGraphicsView):
    file_changed = Signal(str)

    def __init__(self):
        QGraphicsView.__init__(self)

        self.scene = QGraphicsScene()
        self.setScene(self.scene)

        self.pixmaps = []

        self.aspectRatioMode = Qt.KeepAspectRatio
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.items_selectable = True

        self.is_flipped = False

        self.is_rotating = False
        self.rotation = 0
        self.rotation_step = 5

        self.scale_factor = 1
        self.resize_lock = False

        self.shapes = []

        self.is_drawing = False
        self.shape_start = None
        self.shape = None
        self.shape_type = None

        self.files = []
        self.img_path = None
        self.img_dir = None
        self.img_name = None

        self.SUPPORTED_FILE_TYPES = [".png", ".jpg"]


    def load_image(self, path):
        if os.path.isfile(path):
            #TODO: add checks if the image being loaded is already in the loaded directory
            self.img_path = path
            self.img_dir = os.path.dirname(path)
            self.img_name = os.path.basename(path)
            self.files = [f for f in os.listdir(self.img_dir) if os.path.splitext(f)[-1] in self.SUPPORTED_FILE_TYPES]

            pixmap = QPixmap(path)

            pixmap_item = self.add_image(pixmap)
            pixmap_item.setFlag(QGraphicsItem.ItemIsSelectable)
            pixmap_item.setFlag(QGraphicsItem.ItemIsMovable)

            self.pixmaps.append(pixmap_item)

    def add_image(self, pixmap):
        pixmap_item = self.scene.addPixmap(pixmap)
        self.reset_viewer(zoom = True)
        # self.setSceneRect(self.scene.itemsBoundingRect())

        return pixmap_item
        
    def add_debug_thing(self):
        paths = [r"C:\Users\pault\Pictures\one.png", r"C:\Users\pault\Pictures\f0cc337d3ff7275a4dc734f73690c5e7.webp"]

        for path in paths:
            pixmap = QPixmap(path)
            graphics_item = self.scene.addPixmap(pixmap)
            self.pixmaps.append(graphics_item)


    


    # def has_image(self):
    #     return self._pixmapHandle is not None

    # def clear_image(self):
    #     if self.has_image():
    #         self.scene.removeItem(self._pixmapHandle)
    #         self._pixmapHandle = None

    # # return the image currently being displayed as a pixmap
    # def pixmap(self):
    #     if self.has_image():
    #         return self._pixmapHandle.pixmap()
    #     return None

    # # return the image currently being displayed as QImage
    # def image(self):
    #     if self.has_image():
    #         return self._pixmapHandle.pixmap().toImage()
    #     return None

    # # set an image to be displayed on the image viewer
    # def set_image(self, image):
    #     # convert the iamge to pixmap
    #     if type(image) is QPixmap:
    #         pixmap = image 
    #     elif type(image) is QImage:
    #         pixmap = QPixmap.fromImage(image)

    #     # dunno what this does
    #     if self.has_image():
    #         self._pixmapHandle.setPixmap(pixmap)
    #     else:
    #         self._pixmapHandle = self.scene.addPixmap(pixmap)
        
    #     # adjust the view of the scene to the pixmap
    #     self.setSceneRect(QRectF(pixmap.rect()))
    #     self.fitInView(self.sceneRect(), self.aspectRatioMode)

    # # load an image from a filepath
    # def file_from_file_dialog(self):
    #     file_name, _ = QFileDialog.getOpenFileName(self, "Open image file:")

    #     self.load_file(file_name)


    # def load_file(self, file_path):
    #     if os.path.isfile(file_path):
    #         self.img_dir = os.path.dirname(file_path)
    #         self.img_name = os.path.basename(file_path)
    #         self.files = [f for f in os.listdir(self.img_dir) if os.path.splitext(f)[-1] in self.SUPPORTED_FILE_TYPES]

    #         self.img_path = file_path
    #         image = QImage(file_path)
    #         self.set_image(image)

    #         self.reset_viewer(rotation = True, zoom = True, flip = True, shapes = True)
            # self.file_changed.emit(self.img_name)




    def flip_image(self):
        self.scale(-1, 1)
        self.is_flipped = not self.is_flipped

    def toggle_rotating(self):
        self.is_rotating = not self.is_rotating
        
    def reset_viewer(self, rotation = False, zoom = False, flip = False, shapes = False):
        if shapes:
            for line in self.shapes:
                self.scene.removeItem(line)
            self.shapes = []
      
        if flip:
            if self.is_flipped:
                    self.flip_image()
            self.is_flipped = False

        if rotation:
            # dont touch this it works somehow idk why
            if self.is_flipped:
                self.rotate(self.rotation)
            else:
                self.rotate(self.rotation * -1)
            self.rotation = 0

        if zoom:
            self.setSceneRect(self.scene.itemsBoundingRect())
            self.fitInView(self.sceneRect(), self.aspectRatioMode)
            self.scale_factor = 1

    def adjust_zoom(self):
        self.fitInView(self.zoom_rect, self.aspectRatioMode)

    # returns the viewport as pixmap
    def export_image(self):
        pixmap = QPixmap(self.viewport().size())
        self.viewport().render(pixmap)

        return pixmap

    def step(self, direction):
        index = self.files.index(self.img_name)

        if direction == "left":
            if index == 0:
                return
            new_img_name = os.path.join(self.img_dir, self.files[index - 1])

        elif direction == "right":
            if index + 1 == len(self.files):
                return
            new_img_name = os.path.join(self.img_dir, self.files[index + 1])

        self.load_file(new_img_name)

    def toggle_selectable(self):
        match self.items_selectable:
            case False:
                for pixmap in self.pixmaps:
                    pixmap.setFlag(QGraphicsItem.ItemIsSelectable, True)
                    pixmap.setFlag(QGraphicsItem.ItemIsMovable, True)
                self.items_selectable = True
                print("Enabled Item selection and movation")

        
            case True:
                for pixmap in self.pixmaps:
                    pixmap.setFlag(QGraphicsItem.ItemIsSelectable, False)
                    pixmap.setFlag(QGraphicsItem.ItemIsMovable, False)
                self.items_selectable = False
                print("Disabled Item selection and movation")
        
    # Events
    def resizeEvent(self, event):
        if self.resize_lock:
            self.resize_lock = not self.resize_lock
            return

        self.reset_viewer(zoom = True)

    def mousePressEvent(self, event):
        scenePos = self.mapToScene(event.pos())

        if event.button() == Qt.LeftButton:
            self.setDragMode(QGraphicsView.ScrollHandDrag)
            self.is_dragging = True
            print("button pressed")

        QGraphicsView.mousePressEvent(self, event)


    def mouseReleaseEvent(self, event):
        QGraphicsView.mouseReleaseEvent(self, event)

        if event.button() == Qt.LeftButton:
            self.setDragMode(QGraphicsView.NoDrag)
            self.is_dragging = False
            print("button released")

        QGraphicsView.mouseReleaseEvent(self, event)



    def mouseDoubleClickEvent(self, event):        
        if event.button() == Qt.LeftButton:
            self.reset_viewer(shapes = True)

        elif event.button() == Qt.RightButton:
            self.reset_viewer(rotation = True, zoom = True)
            
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
            self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse) # AnchorUnderMouse # AnchorViewCenter

            scale_factor = 1.05
            if event.angleDelta().y() > 0:
                self.scale(scale_factor, scale_factor)
                self.scale_factor *= scale_factor
            else:
                self.scale(1.0 / scale_factor, 1.0 / scale_factor)
                self.scale_factor *= 1.0 / scale_factor

            self.zoom_rect = self.mapToScene(self.viewport().rect())


    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Control:
            self.toggle_selectable()

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Control:
            self.toggle_selectable()


    

    # def mouseMoveEvent(self, event):
    #     if self.is_dragging:
    #         self.mouseMoveEvent(QMouseEvent(
    #             type = event.type(),
    #             localPos = event.position(),
    #             globalPos = event.globalPos(),
    #             source = event.source(),
    #             scenePos = event.scenePosition(),
    #             button = Qt.MouseButton.LeftButton,
    #             buttons = event.buttons(),
    #             modifiers = event.modifiers(),
    #             device = event.device()
    #         ))