from PyQt6.QtCore import QSize, Qt
from utils.settings import Settings
from PyQt6.QtWidgets import (
    QLabel,
    QPushButton,
    QStyle,
    QVBoxLayout,
    QWidget,
    QFileDialog,
    QMessageBox,
    QComboBox,
    QLineEdit,
    QGroupBox,
    QFormLayout,
    QHBoxLayout
)

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
        self.combobox.addItems(Settings.retrieve_settings("export_options"))
        self.combobox.currentTextChanged.connect(self.change_export_setting)

        icon = self.style().standardIcon(QStyle.StandardPixmap.SP_DirIcon)

        self.select_dir_button = QPushButton(f"{Settings.retrieve_settings('directory_path')}")
        self.select_dir_button.setIcon(icon)
        self.select_dir_button.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.select_dir_button.clicked.connect( lambda checked, origin_path=Settings.retrieve_settings('directory_path'): self.open_dir(origin_path=origin_path))

        self.directory_name_input = QLineEdit()
        self.directory_name_input.setText(f"{Settings.retrieve_settings('temp_dir_name')}")
        self.directory_name_input.textChanged.connect(self.change_temp_dir_name_setting)

        self.package_box = QComboBox()
        self.package_box.addItems(Settings.retrieve_settings('package_type_s'))
        self.package_box.currentTextChanged.connect(self.change_package_type_setting)

        self.input = QLineEdit()
        self.input.setText(f"{Settings.retrieve_settings('custom_file_selection')}")
        self.input.textChanged.connect(self.change_custom_file_selection_setting)

        self.selection_input = QLineEdit()
        self.selection_input.setText(f"{Settings.retrieve_settings('custom_file_selection_name')}")
        self.selection_input.textChanged.connect(self.change_custom_file_selection_name_setting)

        self.apply_button = QPushButton("apply settings")
        self.apply_button.clicked.connect(self.apply_settings)

        self.default_button = QPushButton("to default")
        self.default_button.clicked.connect(self.default_settings)

        form_layout.addRow(QLabel(f"default export: {Settings.retrieve_settings('default_export')}"))
        form_layout.addRow(QLabel(f"chosen export: {Settings.retrieve_settings('chosen_export')}"), self.combobox)
        form_layout.addRow(QLabel("directory path:"), self.select_dir_button)
        form_layout.addRow(QLabel("directory name:"), self.directory_name_input)
        form_layout.addRow(QLabel("package type:"), self.package_box)
        group_box.setLayout(form_layout)
        main_layout.addWidget(group_box)

        file_form_layout.addRow(QLabel(f"default file selection: {Settings.retrieve_settings('default_file_selection')}"))
        file_form_layout.addRow(QLabel(f"file selection options: {Settings.retrieve_settings('file_selection_options')}"))
        file_form_layout.addRow(QLabel("custom file selection:"), self.input)
        file_form_layout.addRow(QLabel(f"file selection name: {Settings.retrieve_settings('file_selection_name')}"))
        file_form_layout.addRow(QLabel("custom file selection name:"), self.selection_input)
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
        print(Settings.retrieve_settings("default_export"))

    def open_dir(self, origin_path: str):
        dialog = QFileDialog.getExistingDirectory(
            parent=self,
            caption="Select directory",
            directory=origin_path,
            options=QFileDialog.Option.ShowDirsOnly
        )

        if dialog:
            self.settings.update({"directory_path": dialog})

    def change_export_setting(self, val):
        self.settings.update({"chosen_export": val})

    def change_temp_dir_name_setting(self, val):
        self.settings.update({"temp_dir_name": val})

    def change_package_type_setting(self, val):
        self.settings.update({"chosen_package": val})

    def change_custom_file_selection_setting(self, val):
        self.settings.update({"custom_file_selection": val})

    def change_custom_file_selection_name_setting(self, val):
        self.settings.update({"custom_file_selection_name": val})

    def apply_settings(self):
        if not self.settings:
            return
        
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Changes")
        dlg.setText("Are you sure you want to change your settings?")
        dlg.setStandardButtons(
            QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel
        )
        dlg.setIcon(QMessageBox.Icon.Question)
        button = dlg.exec()

        if button == QMessageBox.StandardButton.Ok:
            Settings.save_changes(self.settings)
            self.settings.clear()
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
            Settings.apply_default()
        else:
            print("default cancelled")