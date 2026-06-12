from PyQt6.QtCore import QSize, Qt
from middleware.label_studio_controller import LabelStudioController
from PyQt6.QtWidgets import (
    QLabel,
    QPushButton,
    QStyle,
    QVBoxLayout,
    QWidget,
    QFileDialog,
    QLineEdit,
    QGroupBox,
    QFormLayout,
    QMessageBox
)

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

        self.email_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.button = QPushButton("login")
        self.button.setEnabled(True)
        self.button.clicked.connect(self.login)

        form_layout.addRow(QLabel("email:"), self.email_input)
        form_layout.addRow(QLabel("password:"), self.password_input)
        form_layout.addRow(self.button)
        group_box.setLayout(form_layout)
        main_layout.addWidget(group_box)

        self.setLayout(main_layout)

    def login(self):
        if self.email_input.text() and self.password_input.text():
            b, v = self.label_studio_controller.label_studio_free_port(8080)
            if not b:
                if self.__show_port_warning(8080, v):
                    return

            self.label_studio_controller.label_studio_login(self.email_input.text(), self.password_input.text())


    def __show_port_warning(self, port, process_name):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setWindowTitle("Port in use!")
        msg.setText(f"Can't start label studio on port: {port}")
        msg.setInformativeText(
            f"The requested port is momentarily used by process: '{process_name}'.\n\n"
            "Close the process manually or change the port settings."
        )
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        if msg.exec():
            return True

    def closeEvent(self, event):
        self.label_studio_controller.close()
        event.accept()

   
