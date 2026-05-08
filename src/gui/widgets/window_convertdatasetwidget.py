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
    QCheckBox
)
from utils.io import IO
from gui.events.thread_handler import ThreadHandler
from handler.file_handler import FileOsHandler

class ConvertDatasetWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Coco dataset to Yolo dataset conversion")
        self.setMinimumSize(QSize(400, 450))
        self.setMaximumSize(QSize(600, 550))

        main_layout = QVBoxLayout()

        group_box = QGroupBox("Coco to Yolo conversion")
        form_layout = QFormLayout()

        icon = self.style().standardIcon(QStyle.StandardPixmap.SP_DirIcon)

        self.json_result_button = QPushButton("choose coco embedded json file")
        self.json_result_button.setIcon(icon)
        self.json_result_button.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

        self.cleaned_json_input = QLineEdit()
        self.cleaned_json_input.setText("cleaned_json")
        self.cleaned_json_input.setEnabled(False)

        self.images_to_slice_button = QPushButton("Choose image directory to slice")
        self.images_to_slice_button.setIcon(icon)
        self.images_to_slice_button.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.images_to_slice_button.setEnabled(False)

        self.sliced_images_dir_name_input = QLineEdit()
        self.sliced_images_dir_name_input.setText("tiled_dataset")
        self.sliced_images_dir_name_input.setEnabled(False)

        self.width_in_pix_input = QLineEdit()
        self.width_in_pix_input.setText("1500")
        self.width_in_pix_input.setEnabled(False)

        self.slice_width_input = QLineEdit()
        self.slice_width_input.setText("640")
        self.slice_width_input.setEnabled(False)

        self.slice_height_input = QLineEdit()
        self.slice_height_input.setText("640")
        self.slice_height_input.setEnabled(False)

        form_layout.addRow(QLabel("Choose the corresponding result.json"), self.json_result_button)
        form_layout.addRow(QLabel("Name the file to enter the clean json in"), self.cleaned_json_input)
        form_layout.addRow(QLabel("Choose the corresponding directory with the images to be sliced"), self.images_to_slice_button)
        form_layout.addRow(QLabel("Name the directory where the sliced images should be saved"), self.sliced_images_dir_name_input)
        form_layout.addRow(QLabel("The minimum width of the images that should be excluded"), self.width_in_pix_input)
        form_layout.addRow(QLabel("The width that each slice should be"), self.slice_width_input)
        form_layout.addRow(QLabel("The height that each slice should be"), self.slice_height_input)

        group_box.setLayout(form_layout)
        main_layout.addWidget(group_box)

        self.setLayout(main_layout)


        