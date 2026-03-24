from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QLabel, QVBoxLayout


class CustomDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("HELLO!")
        self.setFixedSize(QSize(400, 300))

        QBtn = (
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout = QVBoxLayout()
        message = QLabel("Something happened, is that OK?")
        layout.addWidget(message)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)