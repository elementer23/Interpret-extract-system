from PyQt6.QtCore import QSize, Qt, QFileInfo
from PyQt6.QtWidgets import (
    QLabel,
    QPushButton,
    QStyle,
    QVBoxLayout,
    QWidget,
    QFileDialog,
    QHBoxLayout,
    QLineEdit,
    QGroupBox,
    QFormLayout,
    QProgressBar
)
from utils.io import IO
from gui.events.thread_handler import ThreadHandler
from handler.file_handler import FileOsHandler
from error.error_hub import ErrorHub

class ConvertDatasetWindow(QWidget):
    """
    Isn't finished yet.
    """
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Coco dataset to Yolo dataset conversion")
        self.setMinimumSize(QSize(400, 450))
        self.setMaximumSize(QSize(600, 550))

        main_layout = QVBoxLayout()

        progress_layout = QHBoxLayout()

        self.files = ""
        self.directory = ""
        self.count_active_threads = 0

        group_box = QGroupBox("Coco to Yolo conversion")
        form_layout = QFormLayout()

        icon = self.style().standardIcon(QStyle.StandardPixmap.SP_DirIcon)

        self.json_result_button = QPushButton("choose coco embedded json file")
        self.json_result_button.setIcon(icon)
        self.json_result_button.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.json_result_button.clicked.connect(self.open_json_coco_file)

        self.cleaned_json_input = QLineEdit()
        self.cleaned_json_input.setText("cleaned_json")
        self.cleaned_json_input.setEnabled(False)

        self.images_to_slice_button = QPushButton("Choose image directory to slice")
        self.images_to_slice_button.setIcon(icon)
        self.images_to_slice_button.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.images_to_slice_button.setEnabled(False)
        self.images_to_slice_button.clicked.connect(self.open_images_to_slice_dir)

        # self.sliced_images_dir_name_input = QLineEdit()
        # self.sliced_images_dir_name_input.setText("tiled_dataset")
        # self.sliced_images_dir_name_input.setEnabled(False)

        self.width_in_pix_input = QLineEdit()
        self.width_in_pix_input.setText("1500")
        self.width_in_pix_input.setEnabled(False)

        self.slice_width_input = QLineEdit()
        self.slice_width_input.setText("640")
        self.slice_width_input.setEnabled(False)

        self.slice_height_input = QLineEdit()
        self.slice_height_input.setText("640")
        self.slice_height_input.setEnabled(False)

        self.activate_function_button = QPushButton("convert")
        self.activate_function_button.setEnabled(False)
        self.activate_function_button.clicked.connect(lambda checked: self.run_func(self.run_convert, None, checked))

        self.progressbar = QProgressBar()
        self.progressbar.setVisible(False)
        self.progressbar.setTextVisible(False)

        form_layout.addRow(QLabel("Choose the corresponding result.json"), self.json_result_button)
        form_layout.addRow(QLabel("Name the file to enter the clean json in"), self.cleaned_json_input)
        form_layout.addRow(QLabel("Choose the corresponding directory with the images to be sliced"), self.images_to_slice_button)
        # form_layout.addRow(QLabel("Name the directory where the sliced images should be saved"), self.sliced_images_dir_name_input)
        form_layout.addRow(QLabel("The minimum width of the images that should be excluded"), self.width_in_pix_input)
        form_layout.addRow(QLabel("The width that each slice should be"), self.slice_width_input)
        form_layout.addRow(QLabel("The height that each slice should be"), self.slice_height_input)
        form_layout.addRow(self.activate_function_button)

        group_box.setLayout(form_layout)
        progress_layout.addWidget(self.progressbar)
        main_layout.addWidget(group_box)
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

    def open_json_coco_file(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        dialog.setNameFilter(f"Json (*.json)")

        if dialog.exec():
            self.json_result_button.setText(f"Selected: {self.file_name_list(dialog.selectedFiles())}")
            self.cleaned_json_input.setEnabled(True)
            self.images_to_slice_button.setEnabled(True)
            self.files = dialog.selectedFiles()


    def open_images_to_slice_dir(self):
        dialog = QFileDialog.getExistingDirectory(
            parent=self,
            caption="Select directory",
            options=QFileDialog.Option.ShowDirsOnly
        )

        if dialog:
            print(dialog)
            self.images_to_slice_button.setText(f"{dialog}")
            self.directory = dialog
            self.width_in_pix_input.setEnabled(True)
            self.slice_width_input.setEnabled(True)
            self.slice_height_input.setEnabled(True)
            self.activate_function_button.setEnabled(True)


    def test_run(self):
        clean_json = self.cleaned_json_input.text()
        width_in_pix = self.width_in_pix_input.text()
        slice_width = self.slice_width_input.text()
        slice_height = self.slice_height_input.text()

        print(self.files)
        print(self.directory)
        print(clean_json)
        print(int(width_in_pix))
        print(int(slice_width))
        print(int(slice_height))

    def run_convert(self, checked, progress_callback=None, thread_id=0, **kwargs):

        try:
            def update_progressbar(percentage):
                if progress_callback:
                    progress_callback.emit(percentage)

            clean_json = self.cleaned_json_input.text()
            width_in_pix = self.width_in_pix_input.text()
            slice_width = self.slice_width_input.text()
            slice_height = self.slice_height_input.text()
            io_convert = IO(progress_callback=update_progressbar)
            
            io_convert.slice_sahi(self.files[0], clean_json, self.directory, None, int(width_in_pix), int(slice_width), int(slice_height))

            return "converted dataset"
        except Exception as e:
            print(e)
            ErrorHub.error_msg(f"dataset conversion went wrong, see: {e}", "warning")
    
    def convert_output(self, data):
        self.json_result_button.setText("choose coco embedded json file")
        self.cleaned_json_input.setEnabled(False)
        self.cleaned_json_input.setText("cleaned_json")
        self.images_to_slice_button.setEnabled(False)
        self.images_to_slice_button.setText("Choose image directory to slice")
        self.width_in_pix_input.setText("1500")
        self.width_in_pix_input.setEnabled(False)
        self.slice_width_input.setText("640")
        self.slice_width_input.setEnabled(False)
        self.slice_height_input.setText("640")
        self.slice_height_input.setEnabled(False)
        self.activate_function_button.setEnabled(False)

    def file_name_list(self, file_list):
        list = []

        for path in file_list:
            list.append(QFileInfo(path).fileName())

        return str(list[0])


        