from PyQt6.QtCore import QSize, QFileInfo
import zipfile
from utils.utilities import BasicUtils
from PyQt6.QtWidgets import (
    QLabel,
    QPushButton,
    QVBoxLayout,
    QScrollArea,
    QHBoxLayout,
    QGridLayout,
    QWidget,
    QFileDialog,
    QListView
)

from handler.file_handler import FileHandler

class InsertZipFileWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Insert through zip")
        self.setFixedSize(QSize(400, 300))
        self.file_path = ""
        self.context = ""

        main_layout = QVBoxLayout()

        grid_layout = QGridLayout()
        self.label = QLabel("select...")

        self.button = QPushButton("select files")
        self.button.clicked.connect(self.open_file_dialog)

        self.check_button = QPushButton("check content")
        self.check_button.setHidden(True)
        self.check_button.clicked.connect(self.check_content)

        self.unzip_button = QPushButton("unzip content")
        self.unzip_button.setHidden(True)
        self.unzip_button.clicked.connect(self.unzip_zip)

        self.dir_button = QPushButton("check dir")
        self.dir_button.setHidden(True)
        self.dir_button.clicked.connect(self.dir_content)

        grid_layout.addWidget(QLabel("File:"), 1, 0)
        grid_layout.addWidget(self.label, 1, 1)
        grid_layout.addWidget(self.button, 1, 2)
        grid_layout.addWidget(self.check_button, 1, 3)
        grid_layout.addWidget(self.unzip_button, 1, 4)
        grid_layout.addWidget(self.dir_button, 2, 3)
        main_layout.addLayout(grid_layout)

        scroll_view = QScrollArea()
        scroll_view.setWidgetResizable(True)

        content_widget = QWidget()
        self.content_layout = QVBoxLayout(content_widget)

        scroll_view.setWidget(content_widget)
        main_layout.addWidget(scroll_view)
        
        self.setLayout(main_layout)

        self.dir_content()

    def open_file_dialog(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        dialog.setNameFilter("General (*.png *.jpg *.jpeg *.webp *.pdf *.dwg *.zip)")

        if dialog.exec():
            self.label.setText(self.file_name_list(dialog.selectedFiles()))
            self.file_path = dialog.selectedFiles()
            self.check_button.setHidden(False)
            self.unzip_button.setHidden(False)
            self.dir_button.setHidden(False)

    def check_content(self):
        if BasicUtils.is_zip_present(self.file_path[:]):
            # print(QFileInfo(self.file_path[0]).fileName())
            zf = zipfile.ZipFile(f"{self.file_path[0]}", "r")
            print(zf.namelist())
            zf.close()

    def unzip_zip(self):
        if BasicUtils.is_zip_present(self.file_path[:]):
            zf = zipfile.ZipFile(f"{self.file_path[0]}", "r")
            try:
                zf.extractall(path="C:/Users/697/Documents/temp_files", pwd=None)
            except:
                print('Error')
                pass
            zf.close()

    def dir_content(self):
        files = FileHandler().get_temp_files_dir()

        for i in reversed(range(self.content_layout.count())):
            widget = self.content_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        if not files:
            self.content_layout.addWidget(QLabel("Geen content"))
            return

        for file in files:
            row = QHBoxLayout()
            label = QLabel(f"{file}")
            
            open_image_button = QPushButton("Open image")
            export_file_button = QPushButton("export to excel")

            open_image_button.clicked.connect(lambda checked, f=file: self.open_file(f))

            export_file_button.clicked.connect(lambda checked, f=file: self.export_file(f))

            row.addWidget(label)
            row.addWidget(open_image_button)
            row.addWidget(export_file_button)

            self.content_layout.addLayout(row)

        self.content_layout.addStretch()

    def open_file(self, file):
        print(file)

    def export_file(self, file):
        print(file)

    def file_name_list(self, file_list):
        list = []

        for path in file_list:
            list.append(QFileInfo(path).fileName())

        return str(list)