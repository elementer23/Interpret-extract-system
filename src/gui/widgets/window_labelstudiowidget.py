from PyQt6.QtCore import QSize, Qt
from middleware.label_studio_controller import LabelStudioController
from PyQt6.QtWidgets import (
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QLineEdit,
    QGroupBox,
    QFormLayout
)
from utils.config import Config

class LabelStudioWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("label studio")
        self.setMinimumSize(QSize(500, 400))
        self.setMaximumSize(QSize(700, 600))

        self.file_path = ""
        main_layout = QVBoxLayout()
        self.label_studio_controller = LabelStudioController()

        group_box = QGroupBox("label studio")
        form_layout = QFormLayout()

        self.label = QLabel("File chosen:")

        self.button = QPushButton("login")
        self.button.setDefault(True)
        self.button.clicked.connect(self.login)

        self.email_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        form_layout.addRow(QLabel("email:"), self.email_input)
        form_layout.addRow(QLabel("password:"), self.password_input)
        form_layout.addRow(self.button)
        group_box.setLayout(form_layout)
        main_layout.addWidget(group_box)

        self.setLayout(main_layout)

    def login(self):
        if self.email_input.text() and self.password_input.text():
            if self.label_studio_controller.label_studio_free_port(int(Config.get("port"))):
                self.label_studio_controller.label_studio_login(self.email_input.text(), self.password_input.text())

    def closeEvent(self, event):
        self.label_studio_controller.close()
        event.accept()

   
