from PyQt6.QtCore import QSize, QFileInfo
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

class InsertBulkFileWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Insert in bulk")
        self.setFixedSize(QSize(400, 300))
        self.file_path = ""
        self.context = ""

        layout = QGridLayout()
        self.label = QLabel("select...")

        self.button = QPushButton("select files")
        self.button.clicked.connect(self.open_file_dialog)

        self.add_button = QPushButton("add files")
        self.add_button.setHidden(True)
        self.add_button.clicked.connect(self.add_files)

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
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        dialog.setNameFilter("General (*.png *.jpg *.jpeg *.webp *.pdf *.dwg *.zip)")

        if dialog.exec():
            self.label.setText(self.file_name_list(dialog.selectedFiles()))
            self.file_path = dialog.selectedFiles()
            self.add_button.setHidden(False)

    def add_files(self):
        if not self.add_button.isHidden():
            self.add_button.setHidden(True)
            print(self.file_path)

            builder = Handler.pipeline_builder(self, False, Handler.STANDARD_TEXT_BUILD)

            # for file_path in self.file_path:
            self.context = builder.run(builder.handler, self.file_path[:])

            self.label.setText("Select...")
            self.bound_box_button.setHidden(False)
            self.export_button.setHidden(False)
            
    def file_name_list(self, file_list):
        list = []

        for path in file_list:
            list.append(QFileInfo(path).fileName())

        return str(list)
    
    def draw_box(self):
        if not self.bound_box_button.isHidden():
            self.bound_box_button.setHidden(True)

            custom = Handler.pipeline_builder(self, True, None, FileHandler(), ImageHandler())
            # print(self.file_path)
            in_context = custom.run(custom.handler, self.file_path[:])
            ImageHandler().draw_bounding_box(in_context, self.context)
            # ImageHandler().draw_bounding_box(needed_image, DomainHandler().detection_box_list)

    def activate_export(self):
        if not self.export_button.isHidden():
            self.export_button.setHidden(True)

            Exporter().export_to_excel(self.context.text_boxes)
