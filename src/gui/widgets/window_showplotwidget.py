import cv2 as cv
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea, QScroller
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import Qt


class PlotWindow(QWidget):
    """Plotwindow class, inherits from QWidget
    Displays the drawn canvas of matpotlib but in a PyQt6 window widget instead.

    :type data: Any -> MatLike
    :param data: boundary box data or image data to be displayed on the canvas
    """
    def __init__(self, data):
        super().__init__()
        self.setWindowTitle("Afbeelding Viewer")
        self.resize(800, 600)

        height, width, channel = data.shape
        bytes_per_line = channel * width

        q_img = QImage(data.data, width, height, bytes_per_line, QImage.Format.Format_BGR888)
        self.pixmap = QPixmap.fromImage(q_img)

        self.image_label = QLabel()
        self.image_label.setPixmap(self.pixmap)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setScaledContents(True)
        self.image_label.resize(self.pixmap.size())

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.image_label)
        self.scroll_area.setWidgetResizable(False)
        QScroller.grabGesture(self.scroll_area.viewport(), QScroller.ScrollerGestureType.LeftMouseButtonGesture)

        layout = QVBoxLayout()
        layout.addWidget(self.scroll_area)
        self.setLayout(layout)

        self.zoom_factor = 1.0

    def wheelEvent(self, event):
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            if event.angleDelta().y() > 0:
                self.zoom(1.15)  
            else:
                self.zoom(0.85)  
            event.accept()
        else:
            super().wheelEvent(event)

    def zoom(self, factor):
        if float(self.zoom_factor * factor) < 0.2 or float(self.zoom_factor * factor) > 5.0:
            return

        self.zoom_factor *= factor

        scroller = QScroller.scroller(self.scroll_area.viewport())
        scroller.stop()

        h_bar = self.scroll_area.horizontalScrollBar()
        v_bar = self.scroll_area.verticalScrollBar()
        old_h = h_bar.value()
        old_v = v_bar.value()

        new_size = self.pixmap.size() * self.zoom_factor
        self.image_label.resize(new_size)

        h_bar.setValue(int(factor * old_h + ((factor - 1) * h_bar.pageStep() / 2)))
        v_bar.setValue(int(factor * old_v + ((factor - 1) * v_bar.pageStep() / 2)))

    def closeEvent(self, event):
        """Hard clean-up after closing the window"""
        self.image_label.clear()
        self.setParent(None)
        event.accept()
        