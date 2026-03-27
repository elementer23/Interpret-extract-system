from PyQt6.QtCore import QSize, QFileInfo
from PyQt6.QtWidgets import (
    QLabel,
    QPushButton,
    QGridLayout,
    QWidget,
    QFileDialog
)
from handler.file_handler import FileHandler
from vision.image_handler import ImageHandler
from vision.text_handler import TextHandler
from handler.pipeline import Pipeline

class InsertSingleFileWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Insert singular")
        self.setFixedSize(QSize(400, 300))
        self.file_path = ""

        layout = QGridLayout()
        self.label = QLabel("select...")

        self.button = QPushButton("select file")
        self.button.clicked.connect(self.open_file_dialog)

        self.add_button = QPushButton("add file")
        self.add_button.setHidden(True)
        self.add_button.clicked.connect(self.add_file)

        layout.addWidget(QLabel("File:"), 1, 0)
        layout.addWidget(self.label, 1, 1)
        layout.addWidget(self.button, 1, 2)
        layout.addWidget(self.add_button, 1, 3)
        self.setLayout(layout)

    def open_file_dialog(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        dialog.setNameFilter("General (*.png *.jpg *.jpeg *.webp *.pdf *.dwg)")

        if dialog.exec():
            self.label.setText(QFileInfo(dialog.selectedFiles()[0]).fileName())
            self.file_path = dialog.selectedFiles()[0]
            self.add_button.setHidden(False)

    def add_file(self):
        if not self.add_button.isHidden():
            self.add_button.setHidden(True)

            build_pipeline = Pipeline(
                FileHandler(),
                ImageHandler(),
                TextHandler()
            )

            print(build_pipeline.run(build_pipeline.handler, self.file_path))

            self.label.setText("select...")