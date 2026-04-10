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
    QFormLayout,
    QHBoxLayout
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

        apply_h_layout = QHBoxLayout()

        self.settings = {}

        self.button = QPushButton("read info")
        self.button.clicked.connect(self.read_json_info)
        
        self.get_button = QPushButton("get choice")
        self.get_button.clicked.connect(self.get_json_info)

        self.combobox = QComboBox()
        self.combobox.addItems(Settings.retrieve_settings()["export_options"])
        self.combobox.currentTextChanged.connect(self.change_export_setting)

        # self.change_button = QPushButton("change export")
        # self.change_button.clicked.connect(self.change_export_setting)

        self.input = QLineEdit()
        self.input.setText(f"{Settings.retrieve_settings()['custom_file_selection']}")
        self.input.textChanged.connect(self.change_custom_file_selection_setting)

        # self.input_button = QPushButton("change custom file selection")
        # self.input_button.clicked.connect(self.change_custom_file_selection_setting)

        self.selection_input = QLineEdit()
        self.selection_input.setText(f"{Settings.retrieve_settings()['custom_file_selection_name']}")
        self.selection_input.textChanged.connect(self.change_custom_file_selection_name_setting)

        # self.select_input_button = QPushButton("change custom file selection name")
        # self.select_input_button.clicked.connect(self.change_custom_file_selection_name_setting)

        self.apply_button = QPushButton("apply settings")
        self.apply_button.clicked.connect(self.apply_settings)

        self.default_button = QPushButton("to default")
        self.default_button.clicked.connect(self.default_settings)

        form_layout.addRow(QLabel(f"default export: {Settings.retrieve_settings()['default_export']}"))
        # form_layout.addRow(QLabel(f"chosen export: {Settings.retrieve_settings()['chosen_export']}"))
        form_layout.addRow(QLabel(f"chosen export: {Settings.retrieve_settings()['chosen_export']}"), self.combobox)
        group_box.setLayout(form_layout)
        main_layout.addWidget(group_box)

        file_form_layout.addRow(QLabel(f"default file selection: {Settings.retrieve_settings()['default_file_selection']}"))
        file_form_layout.addRow(QLabel(f"file selection options: {Settings.retrieve_settings()['file_selection_options']}"))
        file_form_layout.addRow(QLabel("custom file selection:"), self.input)
        # file_form_layout.addRow(self.input, self.input_button)
        file_form_layout.addRow(QLabel(f"file selection name: {Settings.retrieve_settings()['file_selection_name']}"))
        file_form_layout.addRow(QLabel("custom file selection name:"), self.selection_input)
        # file_form_layout.addRow(self.selection_input, self.select_input_button)
        file_box.setLayout(file_form_layout)
        main_layout.addWidget(file_box)

        apply_h_layout.addWidget(self.apply_button)
        apply_h_layout.addWidget(self.default_button)
        apply_h_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.addLayout(apply_h_layout)

        self.setLayout(main_layout)

    def read_json_info(self):
        Settings.read_settings()

    def get_json_info(self):
        print(Settings.retrieve_settings()["default_export"])

    def change_export_setting(self, val):
        self.settings.update({"chosen_export": val})

    def change_custom_file_selection_setting(self, val):
        self.settings.update({"custom_file_selection": val})

    def change_custom_file_selection_name_setting(self, val):
        self.settings.update({"custom_file_selection_name": val})

    def apply_settings(self):
        if not self.settings:
            return

        Settings.save_changes(self.settings)

    def default_settings(self):
        Settings.apply_default()