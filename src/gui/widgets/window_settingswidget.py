from PyQt6.QtCore import QSize, QFileInfo
from utils.utilities import BasicUtils
from utils.settings import Settings
from PyQt6.QtWidgets import (
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QFileDialog,
    QComboBox,
    QLineEdit,
    QGroupBox,
    QFormLayout
)

from handler.file_handler import FileHandler

class SettingsWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Change settings")
        self.setMinimumSize(QSize(600, 500))
        self.setMaximumSize(QSize(1000, 900))

        main_layout = QVBoxLayout()

        group_box = QGroupBox("export settings")
        form_layout = QFormLayout()

        file_box = QGroupBox("file selection settings")
        file_form_layout = QFormLayout()

        self.button = QPushButton("read info")
        self.button.clicked.connect(self.read_json_info)
        
        self.get_button = QPushButton("get choice")
        self.get_button.clicked.connect(self.get_json_info)

        self.combobox = QComboBox()
        self.combobox.addItems(Settings.retrieve_settings()["export_options"])

        self.change_button = QPushButton("change export")
        self.change_button.clicked.connect(self.change_export_setting)

        self.input = QLineEdit()
        self.input.setText(f"{Settings.retrieve_settings()['custom_file_selection']}")

        self.input_button = QPushButton("change custom file selection")
        self.input_button.clicked.connect(self.change_custom_file_selection_setting)

        self.selection_input = QLineEdit()
        self.selection_input.setText(f"{Settings.retrieve_settings()['custom_file_selection_name']}")

        self.select_input_button = QPushButton("change custom file selection name")
        self.select_input_button.clicked.connect(self.change_custom_file_selection_name_setting)

        form_layout.addRow(QLabel(f"default export: {Settings.retrieve_settings()['default_export']}"))
        form_layout.addRow(QLabel(f"chosen export: {Settings.retrieve_settings()['chosen_export']}"))
        form_layout.addRow(self.combobox, self.change_button)
        group_box.setLayout(form_layout)
        main_layout.addWidget(group_box)

        file_form_layout.addRow(QLabel(f"default file selection: {Settings.retrieve_settings()['default_file_selection']}"))
        file_form_layout.addRow(QLabel(f"file selection options: {Settings.retrieve_settings()['file_selection_options']}"))
        file_form_layout.addRow(QLabel("custom file selection:"))
        file_form_layout.addRow(self.input, self.input_button)
        file_form_layout.addRow(QLabel(f"file selection name: {Settings.retrieve_settings()['file_selection_name']}"))
        file_form_layout.addRow(QLabel("custom file selection name:"))
        file_form_layout.addRow(self.selection_input, self.select_input_button)
        file_box.setLayout(file_form_layout)
        main_layout.addWidget(file_box)
        
        self.setLayout(main_layout)

    def read_json_info(self):
        Settings.read_settings()

    def get_json_info(self):
        print(Settings.retrieve_settings()["default_export"])

    def change_export_setting(self):
        Settings.change_chosen_export(self.combobox.currentText())

    def change_custom_file_selection_setting(self):
        pass

    def change_custom_file_selection_name_setting(self):
        pass