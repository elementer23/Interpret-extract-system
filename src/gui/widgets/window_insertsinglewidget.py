from random import randint
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import (
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from handler.file_handler import FileHandler

class InsertSingleFileWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Insert singular")
        self.setFixedSize(QSize(400, 300))
        file_handler = FileHandler()

        layout = QVBoxLayout()
        self.label = QLabel("Another Window % d" % randint(0, 100))
        self.button = QPushButton("select file")
        # self.button.clicked.connect(file_handler.select_file_from_explorer())
        layout.addWidget(self.label)
        self.setLayout(layout)