from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QLabel, QVBoxLayout
from PyQt6.QtGui import QPixmap, QWheelEvent, QMouseEvent
from PyQt6.QtCore import Qt, QRectF


class ImageView(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.setScene(QGraphicsScene(self))
        self.pixmap_item = QGraphicsPixmapItem()
        self.scene().addItem(self.pixmap_item)

        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        
        self.scale_factor = 1.15 # 每次的缩放比例
        self._zoom = 0 # 当前缩放等级

        self.controller = None
        self._keep_zoom = False

    def set_controller(self, controller):
        self.controller = controller
    
    def display_image(self, pixmap: QPixmap):

        view_height = self.viewport().height()
        scaled_pixmap = pixmap.scaledToHeight(
            view_height,
            Qt.TransformationMode.SmoothTransformation
        )
        self.pixmap_item.setPixmap(scaled_pixmap)
        self.setSceneRect(self.pixmap_item.boundingRect())

        self.horizontalScrollBar().setValue(self.horizontalScrollBar().minimum())

        self.pixmap_item.setPixmap(pixmap)
        self.setSceneRect(QRectF(pixmap.rect()))
        if not self._keep_zoom:
            self._zoom = 0
            self.resetTransform()
            self.fitInView(self.pixmap_item, Qt.AspectRatioMode.KeepAspectRatio)
            self._keep_zoom = True
        

    
    def wheelEvent(self, event: QWheelEvent):
        if event.angleDelta().y() > 0:
            factor = self.scale_factor
            self._zoom += 1
        else:
            factor = 1 / self.scale_factor
            self._zoom -= 1

        # 限制缩放范围
        if self._zoom < -10:
            self._zoom = -10
            return
        elif self._zoom > 20:
            self._zoom = 20
            return

        self.scale(factor, factor)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        super().mouseReleaseEvent(event)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.controller:
            self.controller.update_image()