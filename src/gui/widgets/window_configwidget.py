from PyQt6.QtCore import QSize, Qt
from utils.config import Config
from models.models import Models
from PyQt6.QtWidgets import (
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QMessageBox,
    QComboBox,
    QLineEdit,
    QGroupBox,
    QFormLayout,
    QHBoxLayout
)

class ConfigWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Change configuration")
        self.setMinimumSize(QSize(500, 400))
        self.setMaximumSize(QSize(700, 600))

        self.changes = {}

        main_layout = QVBoxLayout()

        group_box = QGroupBox("Config settings")
        form_layout = QFormLayout()

        apply_h_layout = QHBoxLayout()

        self.port_input = QLineEdit(Config.get("port"))

        self.label_studio_api_key_input = QLineEdit(Config.get("api_key"))
        self.label_studio_api_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        
        self.forcing_cpu = QComboBox()
        self.forcing_cpu.addItems(["False", "True"])
        forcing_cpu_index = self.forcing_cpu.findText(Config.get("force_cpu"), Qt.MatchFlag.MatchFixedString)
        self.forcing_cpu.setCurrentIndex(forcing_cpu_index)

        self.model = QComboBox()
        self.model.addItem("default")
        self.model.addItems(Models().get_models())
        model_index = self.model.findText(Config().get("model"), Qt.MatchFlag.MatchFixedString)
        if model_index >= 0:
            self.model.setCurrentIndex(model_index)

        self.save_button = QPushButton("apply changes")
        self.save_button.clicked.connect(self.apply_settings)
        
        self.default_button = QPushButton("apply default")
        self.default_button.clicked.connect(self.default_settings)

        form_layout.addRow(QLabel("port label studio: "), self.port_input)
        form_layout.addRow(QLabel("label studio api key: "), self.label_studio_api_key_input)
        form_layout.addRow(QLabel("force cpu: "), self.forcing_cpu)
        form_layout.addRow(QLabel("ai model: "), self.model)
        group_box.setLayout(form_layout)
        main_layout.addWidget(group_box)

        apply_h_layout.addWidget(self.save_button)
        apply_h_layout.addWidget(self.default_button)
        apply_h_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.addLayout(apply_h_layout)

        self.setLayout(main_layout)

    def apply_settings(self):

        self.changes.update({"port": self.port_input.text(), "force_cpu": self.forcing_cpu.currentText(),
                             "api_key": self.label_studio_api_key_input.text(), "model": self.model.currentText()})

        dlg = QMessageBox(self)
        dlg.setWindowTitle("Changes")
        dlg.setText("Are you sure you want to change your config settings?")
        dlg.setStandardButtons(
            QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel
        )
        dlg.setIcon(QMessageBox.Icon.Question)
        button = dlg.exec()

        if button == QMessageBox.StandardButton.Ok:
            Config.save(self.changes)
        else:
            print("changes cancelled")

    def default_settings(self):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Default")
        dlg.setText("Are you sure you want to revert to default settings?")
        dlg.setStandardButtons(
            QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel
        )
        dlg.setIcon(QMessageBox.Icon.Question)
        button = dlg.exec()

        if button == QMessageBox.StandardButton.Ok:
            default = Config.default()
            print(default)
        else:
            print("default cancelled")