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

class InsertSingleFileWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Insert singular")
        self.setFixedSize(QSize(400, 300))
        self.file_handler = FileHandler()

        layout = QVBoxLayout()
        self.label = QLabel("Another Window % d" % randint(0, 100))
        self.button = QPushButton("select file")
        self.button.clicked.connect(self.open_file_dialog)
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def open_file_dialog(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        dialog.setNameFilter("General (*.png *.jpg *.jpeg *.webp *.pdf *.dwg)")

        # "N:\049_Plas\2126030 Afstudeeropdracht automatisering info uit docs\12. Tek-Software\Examples\AOC\001.pdf"

        if dialog.exec():
            self.file_handler.select_file(dialog.selectedFiles())