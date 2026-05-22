from PyQt6.QtCore import QSize, QFileInfo
import cv2 as cv
from PyQt6.QtWidgets import (
    QLabel,
    QPushButton,
    QGridLayout,
    QWidget,
    QFileDialog
)
from handler.main_handler import Handler
from handler.file_handler import FileHandler
from vision.image_handler import ImageHandler
from vision.text_handler import TextHandler
import matplotlib.pyplot as plt
from core.exporter import Exporter

class InsertSingleFileWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Insert singular")
        self.setFixedSize(QSize(400, 300))
        self.file_path = ""
        self.context = ""

        layout = QGridLayout()
        self.label = QLabel("select...")

        self.button = QPushButton("select file")
        self.button.clicked.connect(self.open_file_dialog)

        self.add_button = QPushButton("add file")
        self.add_button.setHidden(True)
        self.add_button.clicked.connect(self.add_file)

        self.bound_box_button = QPushButton("draw box")
        self.bound_box_button.setHidden(True)
        self.bound_box_button.clicked.connect(self.draw_box)
        
        self.export_button = QPushButton("export data")
        self.export_button.setHidden(True)
        self.export_button.clicked.connect(self.activate_export)

        layout.addWidget(QLabel("File:"), 1, 0)
        layout.addWidget(self.label, 1, 1)
        layout.addWidget(self.button, 1, 2)
        layout.addWidget(self.add_button, 1, 3)
        layout.addWidget(self.bound_box_button, 1, 3)
        layout.addWidget(self.export_button, 2, 3)
        self.setLayout(layout)

    def open_file_dialog(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        dialog.setNameFilter("General (*.png *.jpg *.jpeg *.webp *.pdf *.dwg)")

        if dialog.exec():
            self.label.setText(QFileInfo(dialog.selectedFiles()[0]).fileName())
            self.file_path = dialog.selectedFiles()
            self.add_button.setHidden(False)

    def add_file(self):
        if not self.add_button.isHidden():
            self.add_button.setHidden(True)

            # custom = Handler.pipeline_builder(self, True, None, FileHandler(), ImageHandler())
            builder = Handler.pipeline_builder(self, False, Handler.STANDARD_TEXT_BUILD)
            # builder = Handler.pipeline_builder(self, False, Handler.STANDARD_DETECTION_BUILD)
            self.context = builder.run(builder.handler, self.file_path[:])
            # test = custom.run(custom.handler, self.file_path)
            # cv.imshow("image", self.context.image)
            # cv.waitKey(0)
            # cv.destroyAllWindows()
            # plt.figure(figsize=(10, 10))
            # plt.imshow(self.context.image)
            # plt.axis('off')
            # plt.show()

            self.label.setText("select...")
            self.bound_box_button.setHidden(False)
            self.export_button.setHidden(False)

    def draw_box(self):
        if not self.bound_box_button.isHidden():
            self.bound_box_button.setHidden(True)

            custom = Handler.pipeline_builder(self, True, None, FileHandler(), ImageHandler())
            in_context = custom.run(custom.handler, self.file_path[:])
            ImageHandler().draw_bounding_box(in_context, self.context)
            # ImageHandler().draw_bounding_box(needed_image, DomainHandler().detection_box_list)

    def activate_export(self):
        if not self.export_button.isHidden():
            self.export_button.setHidden(True)

            # Exporter().export_to_excel(self.context.text_boxes)
            
