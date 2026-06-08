from PyQt6.QtCore import QSize, Qt, QFileInfo
from PyQt6.QtWidgets import (
    QLabel,
    QPushButton,
    QStyle,
    QVBoxLayout,
    QWidget,
    QFileDialog,
    QComboBox,
    QLineEdit,
    QGroupBox,
    QFormLayout,
    QCheckBox,
    QProgressBar,
    QHBoxLayout
)
from handler.file_handler import FileHandler, FileOsHandler
from vision.image_handler import ImageExportHandler
from utils.settings import Settings
from utils.utilities import BasicUtils, FileType
from core.decompress import Decompress
import os
from gui.events.thread_handler import ThreadHandler

class ExportImageWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Export file to image for dataset creation")
        self.setMinimumSize(QSize(500, 550))
        self.setMaximumSize(QSize(700, 650))

        self.files = []
        self.count_active_threads = 0

        main_layout = QVBoxLayout()

        progress_layout = QHBoxLayout()

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
        self.combobox_export_type.addItems(["default", "zip", "7zip", "tar"])

        self.encryption_input_label = QLabel("optional password:")
        self.encryption_input_label.setHidden(True)

        self.encryption_input = QLineEdit()
        self.encryption_input.setHidden(True)

        self.effect_type_label = QLabel("choose effect type:")
        self.effect_type_label.setHidden(True)

        self.combobox_effect_type = QComboBox()
        self.combobox_effect_type.setHidden(True)
        self.combobox_effect_type.addItems(["default", "grid", "gaussianblur", "medianblur"])

        self.combobox_effect_type.currentTextChanged.connect(self.grid_options)

        self.tile_size_label = QLabel("Tile Size:")
        self.tile_size_label.setHidden(True)
        self.tile_size_input = QLineEdit("640")
        self.tile_size_input.setHidden(True)

        self.tile_overlap_label = QLabel("Tile Overlap:")
        self.tile_overlap_label.setHidden(True)
        self.tile_overlap_input = QLineEdit("100")
        self.tile_overlap_input.setHidden(True)

        icon = self.style().standardIcon(QStyle.StandardPixmap.SP_DirIcon)

        self.save_location_button = QPushButton("default")
        self.save_location_button.setIcon(icon)
        self.save_location_button.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.save_location_button.clicked.connect(self.decide_save_location)

        self.save_as = QLineEdit("images")

        self.label = QLabel("Selected:")

        self.select_file_s = QPushButton()
        self.select_file_s.setIcon(icon)
        self.select_file_s.clicked.connect(self.open_dir)

        self.convert_button = QPushButton("convert")
        self.convert_button.setEnabled(False)
        self.convert_button.clicked.connect(lambda checked: self.run_func(self.convert, self.convert_output, checked))

        form_layout.addRow(QLabel("choose color type:"), self.combobox_color_type)
        form_layout.addRow(QLabel("Image type to convert to:"), self.combobox_image_type)

        extra_form_layout.addRow(self.extra_options)
        extra_form_layout.addRow(self.export_type_label, self.combobox_export_type)
        extra_form_layout.addRow(self.encryption_input_label, self.encryption_input)
        extra_form_layout.addRow(self.effect_type_label, self.combobox_effect_type)
        extra_form_layout.addRow(self.tile_size_label, self.tile_size_input)
        extra_form_layout.addRow(self.tile_overlap_label, self.tile_overlap_input)

        directory_form_layout.addRow(QLabel("save to this directory:"), self.save_location_button)
        directory_form_layout.addRow(QLabel("name of archive:"), self.save_as)

        file_form_layout.addRow(self.label, self.select_file_s)
        file_form_layout.addRow(self.convert_button)

        self.progressbar = QProgressBar()
        self.progressbar.setVisible(False)
        self.progressbar.setTextVisible(False)

        group_box.setLayout(form_layout)
        directory_box.setLayout(directory_form_layout)
        extra_box.setLayout(extra_form_layout)
        file_box.setLayout(file_form_layout)
        progress_layout.addWidget(self.progressbar)

        main_layout.addWidget(group_box)
        main_layout.addWidget(extra_box)
        main_layout.addWidget(directory_box)
        main_layout.addWidget(file_box)
        main_layout.addLayout(progress_layout)

        self.setLayout(main_layout)

        self.threadhandler = ThreadHandler()
        self.threadhandler.func_finished.connect(self.progressbar.setValue)
        self.threadhandler.event_finished.connect(self.event_has_ended)

    def run_func(self, fn, fn_out, *args, **kwargs):

        self.count_active_threads += 1
        self.progressbar.setVisible(True)
        self.progressbar.setTextVisible(True)

        self.threadhandler.run_event(fn, fn_out, *args, **kwargs)

    def event_has_ended(self, thread_id):
        self.count_active_threads -= 1
        if self.count_active_threads <= 0:
            self.count_active_threads = 0
            self.progressbar.setVisible(False)
            self.progressbar.setTextVisible(False)
            self.progressbar.setValue(0)

    def reveal_extra(self, checked):
        is_hidden = False if Qt.CheckState(checked) == Qt.CheckState.Checked else True

        self.export_type_label.setHidden(is_hidden)
        self.combobox_export_type.setHidden(is_hidden)
        self.encryption_input_label.setHidden(is_hidden)
        self.encryption_input.setHidden(is_hidden)
        self.effect_type_label.setHidden(is_hidden)
        self.combobox_effect_type.setHidden(is_hidden)

        if is_hidden:
            self.combobox_export_type.setCurrentIndex(0)
            self.encryption_input.setText("")
            self.combobox_effect_type.setCurrentIndex(0)
            self.tile_size_input.setText("640")
            self.tile_overlap_input.setText("100")

    def grid_options(self, val):
        is_hidden = False if val == "grid" else True

        self.tile_size_label.setHidden(is_hidden)
        self.tile_size_input.setHidden(is_hidden)
        self.tile_overlap_label.setHidden(is_hidden)
        self.tile_overlap_input.setHidden(is_hidden)

        if is_hidden:
            self.tile_size_input.setText("640")
            self.tile_overlap_input.setText("100")


    def open_dir(self):
        filter = Settings.retrieve_settings()
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        dialog.setNameFilter(f"{filter['file_selection_name']} {filter['default_file_selection']}")

        if dialog.exec():
            self.label.setText(f"Selected: {self.file_name_list(dialog.selectedFiles())}")
            self.convert_button.setEnabled(True)    
            self.files = dialog.selectedFiles()


    def decide_save_location(self):

        directory = Settings.retrieve_settings('directory_path') if self.save_location_button.text() == "default" else self.save_location_button.text()

        dialog = QFileDialog.getExistingDirectory(
            parent=self,
            caption="Select directory",
            directory=directory,
            options=QFileDialog.Option.ShowDirsOnly
        )

        if dialog:
            self.save_location_button.setText(dialog)

    def convert(self, checked, progress_callback=None, thread_id=0, **kwargs):

        directory = Settings.retrieve_settings('directory_path') if self.save_location_button.text() == "default" else self.save_location_button.text()

        convert_ops = {}
        convert_ops.update({"color_type": self.combobox_color_type.currentText()})
        convert_ops.update({"image_type": self.combobox_image_type.currentText()})
        convert_ops.update({"save_location": directory})
        convert_ops.update({"file_name": "image"})
        convert_ops.update({"archive_name": self.save_as.text()})

        encryption = self.encryption_input.text() if len(self.encryption_input.text()) > 0 else None
        
        convert_ops.update({"export_type": self.combobox_export_type.currentText()})
        convert_ops.update({"encryption": encryption})
        convert_ops.update({"effect_type": self.combobox_effect_type.currentText()})
        convert_ops.update({"tile_size": int(self.tile_size_input.text())})
        convert_ops.update({"tile_overlap": int(self.tile_overlap_input.text())})

        FileOsHandler().create_dir(convert_ops['save_location'], convert_ops['archive_name'])
        FileOsHandler().create_dir(convert_ops['save_location'], "temp_export")
        target_path = os.path.join(convert_ops['save_location'], "temp_export")

        def update_progressbar(percentage):
            if progress_callback:
                progress_callback.emit(percentage)

        Decompress(directory=target_path, file_s=self.files, progress_callback=update_progressbar)

        files = FileOsHandler().get_files_from_dir(target_path=target_path)
        compatible_files = BasicUtils.maintain_compatible_extensions(files, FileType.PDF, FileType.IMAGE)

        c_file = FileHandler().conversion(compatible_files)

        if progress_callback: progress_callback.emit(60)

        ImageExportHandler().conversion(c_file, convert_ops)

        if progress_callback: progress_callback.emit(90)

        FileOsHandler().remove_dir(target_path)

        if progress_callback: progress_callback.emit(100)
        
        return checked

    def convert_output(self, data):
        self.label.setText(f"Selected:")
        self.convert_button.setEnabled(False)

    def file_name_list(self, file_list):
        list = []

        for path in file_list:
            list.append(QFileInfo(path).fileName())

        return str(list)
