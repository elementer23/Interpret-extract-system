from PyQt6.QtCore import QSize, Qt
from handler.file_handler import FileHandler
from handler.main_handler import Handler
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
    QProgressBar,
    QHBoxLayout
)
from gui.events.thread_handler import ThreadHandler
import gc

class GenerateExtractedDataPDF(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("generate a pdf with the extracted data")
        self.setMinimumSize(QSize(300, 200))
        self.setMaximumSize(QSize(500, 400))

        self.file_path = []
        self.count_active_threads = 0

        main_layout = QVBoxLayout()
        progress_layout = QHBoxLayout()

        group_box = QGroupBox("pdf to draw on")
        form_layout = QFormLayout()

        self.label = QLabel("File chosen:")
        icon = self.style().standardIcon(QStyle.StandardPixmap.SP_DirIcon)

        self.button = QPushButton("choose file")
        self.button.setIcon(icon)
        self.button.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.button.clicked.connect(self.open_dir)

        self.name_file_to = QLineEdit()

        self.convert_button = QPushButton("draw data")
        self.convert_button.setDisabled(True)
        self.convert_button.clicked.connect(lambda checked: self.run_func(self.run_convert, self.convert_output, checked))

        self.progressbar = QProgressBar()
        self.progressbar.setVisible(False)
        self.progressbar.setTextVisible(False)

        form_layout.addRow(self.label, self.button)
        form_layout.addRow(QLabel("name file:"), self.name_file_to)
        form_layout.addRow(self.convert_button)
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

    def open_dir(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.FileMode.ExistingFile)

        if dialog.exec():
            self.label.setText(f"File chosen: {dialog.selectedFiles()[0]}")
            self.file_path = dialog.selectedFiles()
            self.convert_button.setDisabled(False)


    def run_convert(self, checked, progress_callback=None, thread_id=0, **kwargs):
        self.convert_button.setDisabled(True)

        def update_progressbar(percentage):
            if progress_callback:
                progress_callback.emit(percentage)

        builder = Handler.pipeline_builder(self, False, Handler.STANDARD_BUILD)
        context = builder.run(builder.handler, self.file_path[:], progress_callback=update_progressbar)

        if context is not None:
            FileHandler().draw_contextdata_on_pdf(context, self.file_path[0], self.name_file_to.text())
            context = None
            gc.collect()


    def convert_output(self, data):
        self.label.setText(f"File chosen:")

