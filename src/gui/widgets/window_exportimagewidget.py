from PyQt6.QtCore import QSize, Qt, QFileInfo
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
    QHBoxLayout,
    QCheckBox
)
from utils.settings import PackageSettings, PackageType, Settings
from handler.file_handler import FileHandler
from vision.image_handler import ImageHandler

class ExportImageWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Export file to image for dataset creation")
        self.setMinimumSize(QSize(400, 450))
        self.setMaximumSize(QSize(600, 550))

        self.files = []

        main_layout = QVBoxLayout()

        group_box = QGroupBox("image settings")
        form_layout = QFormLayout()

        extra_box = QGroupBox("extra options")
        extra_form_layout = QFormLayout()

        directory_box = QGroupBox("directory settings")
        directory_form_layout = QFormLayout()

        file_box = QGroupBox("file(s) to convert")
        file_form_layout = QFormLayout()

        self.combobox_color_type = QComboBox()
        self.combobox_color_type.addItems(["gray", "color", "inverted"])

        self.combobox_image_type = QComboBox()
        self.combobox_image_type.addItems([".png", ".webp", ".jpeg", ".jpg"])

        self.extra_options = QCheckBox("extra")
        self.extra_options.stateChanged.connect( lambda checked: self.reveal_extra(checked=checked))

        self.export_type_label = QLabel("choose export type:")
        self.export_type_label.setHidden(True)

        self.combobox_export_type = QComboBox()
        self.combobox_export_type.setHidden(True)
        self.combobox_export_type.addItems(["default", ".zip", ".7zip", ".tar"])

        self.encryption_input_label = QLabel("optional password:")
        self.encryption_input_label.setHidden(True)

        self.encryption_input = QLineEdit()
        self.encryption_input.setHidden(True)

        self.effect_type_label = QLabel("choose effect type:")
        self.effect_type_label.setHidden(True)

        self.combobox_effect_type = QComboBox()
        self.combobox_effect_type.setHidden(True)
        self.combobox_effect_type.addItems(["default", "grid", "causianblur", "medianblur"])

        icon = self.style().standardIcon(QStyle.StandardPixmap.SP_DirIcon)

        self.save_location_button = QPushButton("default")
        self.save_location_button.setIcon(icon)
        self.save_location_button.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

        self.save_as = QLineEdit("images")

        self.label = QLabel("Selected:")

        self.select_file_s = QPushButton()
        self.select_file_s.setIcon(icon)
        self.select_file_s.clicked.connect(self.open_dir)

        self.convert_button = QPushButton("convert")
        self.convert_button.setEnabled(False)
        self.convert_button.clicked.connect(self.convert)

        form_layout.addRow(QLabel("choose color type:"), self.combobox_color_type)
        form_layout.addRow(QLabel("Image type to convert to:"), self.combobox_image_type)

        extra_form_layout.addRow(self.extra_options)
        extra_form_layout.addRow(self.export_type_label, self.combobox_export_type)
        extra_form_layout.addRow(self.encryption_input_label, self.encryption_input)
        extra_form_layout.addRow(self.effect_type_label, self.combobox_effect_type)

        directory_form_layout.addRow(QLabel("save to this directory:"), self.save_location_button)
        directory_form_layout.addRow(QLabel("name of archive:"), self.save_as)

        file_form_layout.addRow(self.label, self.select_file_s)
        file_form_layout.addRow(self.convert_button)

        group_box.setLayout(form_layout)
        directory_box.setLayout(directory_form_layout)
        extra_box.setLayout(extra_form_layout)
        file_box.setLayout(file_form_layout)

        main_layout.addWidget(group_box)
        main_layout.addWidget(extra_box)
        main_layout.addWidget(directory_box)
        main_layout.addWidget(file_box)

        self.setLayout(main_layout)

    def reveal_extra(self, checked):
        is_hidden = False if Qt.CheckState(checked) == Qt.CheckState.Checked else True

        self.export_type_label.setHidden(is_hidden)
        self.combobox_export_type.setHidden(is_hidden)
        self.encryption_input_label.setHidden(is_hidden)
        self.encryption_input.setHidden(is_hidden)
        self.effect_type_label.setHidden(is_hidden)
        self.combobox_effect_type.setHidden(is_hidden)


    def open_dir(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        dialog.setNameFilter("Default (*.png *.jpg *.jpeg *.webp *.pdf *.dwg *.zip)")

        if dialog.exec():
            self.label.setText(f"Selected: {self.file_name_list(dialog.selectedFiles())}")
            self.convert_button.setEnabled(True)    
            self.files = dialog.selectedFiles()

    def convert(self):
        self.label.setText(f"Selected:")
        self.convert_button.setEnabled(False)
        FileHandler().conversion(self.files)

    
    def file_name_list(self, file_list):
        list = []

        for path in file_list:
            list.append(QFileInfo(path).fileName())

        return str(list)
