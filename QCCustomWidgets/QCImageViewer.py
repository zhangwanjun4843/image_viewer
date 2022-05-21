# https://github.com/marcel-goldschen-ohm/PyQtImageViewer
import os

from qt_core import *

class QCImageViewer(QGraphicsView):
    files_changed = Signal(list)

    def __init__(self):
        QGraphicsView.__init__(self)

        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.setSceneRect(-5000, -5000, 10000, 10000)

        self.pixmaps = []

        self.aspectRatioMode = Qt.KeepAspectRatio
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.single_image_mode = False

        self.items_selectable = False

        self.is_flipped = False

        self.is_rotating = False
        self.rotation = 0
        self.rotation_step = 5

        self.scale_factor = 1
        self.resize_lock = False

        self.images = [] # the image files being displayed in the scene
        self.files = [] # the loadable image files in the currant directory

        self.SUPPORTED_FILE_TYPES = [".png", ".jpg", ".jfif", ".webp"]


    def load_single_image(self, path):
        if os.path.isfile(path):
            for pixmap in self.pixmaps:
                self.scene.removeItem(pixmap)

            self.pixmaps = []
            self.images = []

            pixmap = QPixmap(path)
            pixmap_item = self.add_image(pixmap)

            self.pixmaps.append(pixmap_item)
            self.images.append(path)

            self.single_image_mode = True


    def load_additional_image(self, path):
        if os.path.isfile(path):
            self.images.append(path)
            self.files_changed.emit(self.images)

            pixmap = QPixmap(path)
            pixmap_item = self.add_image(pixmap)

            self.pixmaps.append(pixmap_item)


    def add_image(self, pixmap):
        item = self.scene.addPixmap(pixmap)
        
        self.toggle_selectable(False)
        self.reset_viewer(zoom = True)
        
        return item


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
            # self.setSceneRect(self.scene.itemsBoundingRect())
            self.fitInView(self.scene.itemsBoundingRect(), self.aspectRatioMode)
            self.scale_factor = 1

    # returns the viewport as pixmap
    def export_image(self):
        pixmap = QPixmap(self.viewport().size())
        self.viewport().render(pixmap)

        return pixmap

    def step(self, direction):
        print(self.files)
        index = self.files.index(self.img_name)

        if direction == "left":
            if index == 0:
                return
            new_img_name = os.path.join(self.img_dir, self.files[index - 1])

        elif direction == "right":
            if index + 1 == len(self.files):
                return
            new_img_name = os.path.join(self.img_dir, self.files[index + 1])

        
        self.load_image(new_img_name)


    def toggle_selectable(self, value):
        for pixmap in self.pixmaps:
            pixmap.setFlag(QGraphicsItem.ItemIsSelectable, value)
            pixmap.setFlag(QGraphicsItem.ItemIsMovable, value)
        self.items_selectable = value

    def change_opacity(self, value):
        if len(self.scene.selectedItems()) == 1:
            self.scene.selectedItems()[0].setOpacity(value)


    # Events
    def resizeEvent(self, event):
        if self.resize_lock:
            self.resize_lock = not self.resize_lock
            return

        self.reset_viewer(zoom = True)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.setDragMode(QGraphicsView.ScrollHandDrag)
            self.is_dragging = True

        QGraphicsView.mousePressEvent(self, event)

        if self.items_selectable:
            for item in self.pixmaps:
                item.setZValue(0)
            self.scene.selectedItems()[0].setZValue(1)


    def mouseReleaseEvent(self, event):
        QGraphicsView.mouseReleaseEvent(self, event)

        if event.button() == Qt.LeftButton:
            self.setDragMode(QGraphicsView.NoDrag)
            self.is_dragging = False

        QGraphicsView.mouseReleaseEvent(self, event)



    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.RightButton:
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
        if event.key() == Qt.Key_Alt and not self.single_image_mode:
            self.toggle_selectable(True)

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Alt and not self.single_image_mode:
            self.toggle_selectable(False)

