from random import randint
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import (
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

class InsertBulkFileWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Insert in bulk")
        self.setFixedSize(QSize(400, 300))
        
        layout = QVBoxLayout()
        self.label = QLabel("Another Window % d" % randint(0, 100))
        layout.addWidget(self.label)
        self.setLayout(layout)