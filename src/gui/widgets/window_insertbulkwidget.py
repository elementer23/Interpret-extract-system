from random import randint
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import (
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QFileDialog
)
from handler.file_handler import FileHandler

class InsertBulkFileWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Insert in bulk")
        self.setFixedSize(QSize(400, 300))
        self.file_handler = FileHandler()
        
        layout = QVBoxLayout()
        self.label = QLabel("Another Window % d" % randint(0, 100))
        self.button = QPushButton("select files")
        self.button.clicked.connect(self.open_file_dialog)
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def open_file_dialog(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        dialog.setNameFilter("General (*.png *.jpg *.jpeg *.webp *.pdf *.dwg)")

        if dialog.exec():
            self.file_handler.select_multi_file(dialog.selectedFiles())