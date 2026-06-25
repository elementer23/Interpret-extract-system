from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea, 
    QScroller, QComboBox, QPushButton
)
from PyQt6.QtGui import QImage, QPixmap, QWheelEvent
from PyQt6.QtCore import Qt, QSize

class PlotWindow(QWidget):
    """
    I ain't gonna lie, this window mostly consists out of AI generation.
    Just loading in the images through a label and swapping through them with a stackwidget
    was easy enough. But once several functionalities were needed to make the viewing of images
    easier, a lot of changes were necessary as well. Something i couldn't figure out in the timespan 
    of a couple of hours. Either way.

    This window is used to load in the images that originate from the easyocr and tesseract dataset.
    It gives the user the ability to zoom in, zoom out. Switch between images. All with a very low cost of 
    ram. Do keep in mind, the more data is generated, the more ram is filled up. Closing this window,
    will automatically restore all the used ram however.

    This window should work with data other than the easyocr and tesseract data. It simply depends if the data you give
    consists out of a opencv numpy array.
    """
    def __init__(self, data):
        super().__init__()
        self.setWindowTitle("View image")
        self.resize(1024, 768)

        self.raw_data = data 
        self.zoom_factor = 1.0

        image_naming = [f"Image: {i + 1}" for i in range(len(data))]
        self.dropdown = QComboBox()
        self.dropdown.addItems(image_naming)
        self.dropdown.currentIndexChanged.connect(self.change_image)

        self.btn_zoom_in = QPushButton("Zoom In (+)")
        self.btn_zoom_out = QPushButton("Zoom Out (-)")
        self.btn_fit = QPushButton("Fit Window")

        self.btn_zoom_in.clicked.connect(lambda: self.adjust_zoom(1.2))
        self.btn_zoom_out.clicked.connect(lambda: self.adjust_zoom(0.8))
        self.btn_fit.clicked.connect(self.fit_to_window)

        controls_layout = QHBoxLayout()
        controls_layout.addWidget(self.dropdown)
        controls_layout.addWidget(self.btn_zoom_in)
        controls_layout.addWidget(self.btn_zoom_out)
        controls_layout.addWidget(self.btn_fit)
        controls_layout.addStretch()

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setScaledContents(False)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.image_label)
        self.scroll_area.setWidgetResizable(True)
        QScroller.grabGesture(self.scroll_area.viewport(), QScroller.ScrollerGestureType.LeftMouseButtonGesture)

        layout = QVBoxLayout()
        layout.addLayout(controls_layout)
        layout.addWidget(self.scroll_area)
        self.setLayout(layout)

        self.fit_to_window()

    def change_image(self, index):
        """
        This funtion simply switches between the images.
        """
        self.update_current_image_view()

    def fit_to_window(self):
        """
        This function fits the image to the window, 
        depending on the current width and height of the window.
        """
        idx = self.dropdown.currentIndex()
        height, width, _ = self.raw_data[idx].shape
        
        area_size = self.scroll_area.viewport().size()
        width_ratio = area_size.width() / width
        height_ratio = area_size.height() / height
        
        self.zoom_factor = min(width_ratio, height_ratio, 1.0)
        self.update_current_image_view()

    def update_current_image_view(self):
        """
        This function loads in a new image, depending on which one is selected.
        Makes use of lazy loading, so ram consumption shouldn't be a problem here.
        """
        idx = self.dropdown.currentIndex()
        cv_img = self.raw_data[idx]

        height, width, channel = cv_img.shape
        bytes_per_line = channel * width
        q_img = QImage(cv_img.data, width, height, bytes_per_line, QImage.Format.Format_BGR888)
        
        orig_pixmap = QPixmap.fromImage(q_img)

        new_width = int(width * self.zoom_factor)
        new_height = int(height * self.zoom_factor)

        scaled_pixmap = orig_pixmap.scaled(
            QSize(new_width, new_height),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )

        self.image_label.setPixmap(scaled_pixmap)
        self.image_label.setFixedSize(scaled_pixmap.size())

    def adjust_zoom(self, factor):
        self.zoom_factor = max(0.1, min(4.0, self.zoom_factor * factor))
        self.update_current_image_view()

    def wheelEvent(self, event: QWheelEvent):
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            if event.angleDelta().y() > 0:
                self.adjust_zoom(1.1)
            else:
                self.adjust_zoom(0.9)
            event.accept()
        else:
            super().wheelEvent(event)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.fit_to_window()

    def closeEvent(self, event):
        self.setParent(None)
        event.accept()