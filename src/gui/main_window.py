from PyQt6.QtCore import QSize, Qt, QFileInfo
from utils.utilities import BasicUtils
import zipfile
from PyQt6.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QHBoxLayout,
    QGridLayout,
    QWidget,
    QFileDialog,
    QCheckBox,
    QMessageBox
    )
from handler.main_handler import Handler
from handler.file_handler import FileHandler
from vision.image_handler import ImageHandler
from vision.text_handler import TextHandler
import matplotlib.pyplot as plt
from utils.settings import Settings, PackageSettings
from core.exporter import Exporter
from gui.widgets.menu_menubarwidget import CustomMenu

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("interpret & extract")

        self.setMinimumSize(QSize(600, 500))
        self.setMaximumSize(QSize(1000, 900))

        self.setMenuBar(CustomMenu(self))

        self.file_path = []
        self.selected_files_list = []

        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        main_layout = QVBoxLayout()

        grid_layout = QGridLayout()

        self.label = QLabel("select...")

        self.button = QPushButton("select file(s)")
        self.button.setStatusTip("select the files to be added.")
        self.button.clicked.connect(self.open_file_dialog)

        self.add_button = QPushButton("add file(s)")
        self.add_button.setStatusTip("add the selected files.")
        self.add_button.setHidden(True)
        self.add_button.clicked.connect(self.add_files)

        self.unzip_button = QPushButton("unzip content")
        self.unzip_button.setStatusTip("unzip the files inside of the chosen zip folder.")
        self.unzip_button.setHidden(True)
        self.unzip_button.clicked.connect(self.unzip_zip)

        self.update_list_button = QPushButton("update content")
        self.update_list_button.setStatusTip("update the content of the list to check for changes.")
        self.update_list_button.clicked.connect(self.dir_content)

        self.delete_selected_button = QPushButton("delete selected")
        self.delete_selected_button.setStatusTip("delete the files that are selected.")
        self.delete_selected_button.setEnabled(False)
        self.delete_selected_button.clicked.connect( lambda checked, sfl=self.selected_files_list: self.delete_selected_files(sfl))

        self.export_selected_button = QPushButton("export selected")
        self.export_selected_button.setStatusTip("export the selected files in accordance with the chosen settings.")
        self.export_selected_button.setEnabled(False)
        self.export_selected_button.clicked.connect( lambda checked, sfl=self.selected_files_list: self.export_selected_files(sfl))

        self.open_selected_button = QPushButton("open selected")
        self.open_selected_button.setStatusTip("open the selected files as images with bounding boxes drawn in them.")
        self.open_selected_button.setEnabled(False)
        self.open_selected_button.clicked.connect( lambda checked, sfl=self.selected_files_list: self.open_selected_files(sfl))

        self.main_checkbox = QCheckBox()
        self.main_checkbox.stateChanged.connect( lambda checked: self.handle_checkbox_state(checked))

        grid_layout.addWidget(QLabel("File(s):"), 1, 0)
        grid_layout.addWidget(self.label, 1, 1)
        grid_layout.addWidget(self.button, 1, 2)
        grid_layout.addWidget(self.add_button, 1, 3)
        grid_layout.addWidget(self.unzip_button, 1, 3)
        grid_layout.addWidget(self.main_checkbox, 2, 0)
        grid_layout.addWidget(self.update_list_button, 2, 1)
        grid_layout.addWidget(self.open_selected_button, 2, 2)
        grid_layout.addWidget(self.export_selected_button, 2, 3)
        grid_layout.addWidget(self.delete_selected_button, 2, 4)
        main_layout.addLayout(grid_layout)

        scroll_view = QScrollArea()
        scroll_view.setWidgetResizable(True)

        content_widget = QWidget()
        self.content_layout = QVBoxLayout(content_widget)
        self.content_layout.addStretch()
        self.loaded_files = set()

        scroll_view.setWidget(content_widget)
        main_layout.addWidget(scroll_view)
        
        main_widget.setLayout(main_layout)

        self.dir_content()

    def open_file_dialog(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        dialog.setNameFilter("Default (*.png *.jpg *.jpeg *.webp *.pdf *.dwg *.zip)")

        if dialog.exec():
            self.label.setText(self.file_name_list(dialog.selectedFiles()))
            self.file_path = dialog.selectedFiles()
            if BasicUtils.is_zip_present(self.file_path[:]):
                self.unzip_button.setHidden(False)
                self.add_button.setHidden(True)
            else:
                self.unzip_button.setHidden(True)
                self.add_button.setHidden(False)

    def add_files(self):
        if not self.add_button.isHidden():
            self.add_button.setHidden(True)

            FileHandler().copy_files(self.file_path[:])
            self.label.setText("Select...")
            self.dir_content()

    def unzip_zip(self):
        if BasicUtils.is_zip_present(self.file_path[:]):
            zf = zipfile.ZipFile(f"{self.file_path[0]}", "r")
            try:
                zf.extractall(path="C:/Users/697/Documents/temp_files", pwd=None)
            except:
                print('Error')
                pass
            zf.close()
            self.dir_content()
            self.unzip_button.setHidden(True)
            self.label.setText("Select...")

    def dir_content(self):
        all_files = FileHandler().get_temp_files_dir()
        new_files = [f for f in all_files if f["file"] not in self.loaded_files]

        if not all_files and self.content_layout.count() <= 1:
            self.content_layout.insertWidget(0, QLabel("Geen content"))
            self.main_checkbox.setEnabled(False)
            return

        if not new_files:
            return

        if self.content_layout.count() > 0:
            first_item = self.content_layout.itemAt(0).widget()
            if isinstance(first_item, QLabel) and first_item.text() == "Geen content":
                first_item.deleteLater()

        for file in new_files:
            row = QHBoxLayout()
            checkbox = QCheckBox()
            checkbox.stateChanged.connect(lambda checked, d=file["dir"], n=file["file"]: self.check_box_checked(d, n, checked))
            label = QLabel(f"{file["file"]}")
            
            open_image_button = QPushButton("Open image")
            open_image_button.setStatusTip("open the chosen file as an image with bounding boxes.")
            export_file_button = QPushButton("export")
            export_file_button.setStatusTip("export the chosen file according to the selected settings.")
            remove_file_button = QPushButton("delete file")
            remove_file_button.setStatusTip("remove the chosen file.")

            open_image_button.clicked.connect(lambda checked, d=file["dir"]: self.open_file(d))
            export_file_button.clicked.connect(lambda checked, d=file["dir"]: self.export_file(d))
            remove_file_button.clicked.connect(lambda checked, d=file["dir"], f=file["file"]: self.delete_file(d, f))

            row.addWidget(checkbox)
            row.addWidget(label)
            row.addWidget(open_image_button)
            row.addWidget(export_file_button)
            row.addWidget(remove_file_button)

            self.content_layout.insertLayout(0, row)
            
            self.loaded_files.add(file["file"])

        self.main_checkbox.setEnabled(True)
        if not self.selected_files_list:
            self.main_checkbox.setCheckState(Qt.CheckState.Unchecked)


    def open_file(self, dir):
        dir_list = []
        dir_list.append(dir)

        builder = Handler.pipeline_builder(self, False, Handler.STANDARD_TEXT_BUILD)
        context = builder.run(builder.handler, dir_list[:])

        custom = Handler.pipeline_builder(self, True, None, FileHandler(), ImageHandler())
        image_context = custom.run(custom.handler, dir_list[:])
        ImageHandler().draw_bounding_box(image_context=image_context, pipeline_context=context)

    def open_selected_files(self, dic_list: list):
        dir_list = []
        for n in dic_list:
            dir_list.append(n["dir"])

        builder = Handler.pipeline_builder(self, False, Handler.STANDARD_TEXT_BUILD)
        context = builder.run(builder.handler, dir_list[:])

        custom = Handler.pipeline_builder(self, True, None, FileHandler(), ImageHandler())
        image_context = custom.run(custom.handler, dir_list[:])
        ImageHandler().draw_bounding_box(image_context=image_context, pipeline_context=context)

    def export_file(self, dir):
        dir_list = []
        dir_list.append(dir)

        builder = Handler.pipeline_builder(self, False, Handler.STANDARD_TEXT_BUILD)
        context = builder.run(builder.handler, dir_list[:])
        Exporter().execute_export(context.text_boxes, PackageSettings.manage_package())

    def export_selected_files(self, dic_list: list):
        dir_list = []
        for n in dic_list:
            dir_list.append(n["dir"])

        builder = Handler.pipeline_builder(self, False, Handler.STANDARD_TEXT_BUILD)
        context = builder.run(builder.handler, dir_list[:])
        Exporter().execute_export(context.text_boxes, PackageSettings.manage_package())

    def delete_file(self, dir, file):
        FileHandler().delete_file(dir)
        self.loaded_files.remove(file)
        correct_item = self.retrieve_widget_layout_in_scroll_view(label_name=file)

        while correct_item.count():
            child = correct_item.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        self.content_layout.removeItem(correct_item)

    def retrieve_widget_layout_in_scroll_view(self, label_name: str):
        for i in reversed(range(self.content_layout.count() - 1)):
            item = self.content_layout.itemAt(i).layout()

            for y in range(item.count()):
                if isinstance(item.itemAt(y).widget(), QLabel):
                    if item.itemAt(y).widget().text() == label_name:
                        return item

    def check_box_checked(self, dir, file, checked):
        if Qt.CheckState(checked) == Qt.CheckState.Checked:
            self.selected_files_list.append({"checked": True, "dir": dir, "file": file})
        else:
            self.selected_files_list.remove({"checked": True, "dir": dir, "file": file})

        check_handler = len(self.selected_files_list) > 0

        self.delete_selected_button.setEnabled(check_handler)
        self.export_selected_button.setEnabled(check_handler)
        self.open_selected_button.setEnabled(check_handler)
        if not check_handler:
            self.main_checkbox.setCheckState(Qt.CheckState.Unchecked)

    def handle_checkbox_state(self, checked):
        get_checkstate = Qt.CheckState.Checked if Qt.CheckState(checked) == Qt.CheckState.Checked else Qt.CheckState.Unchecked

        for i in reversed(range(self.content_layout.count() - 1)):
            item = self.content_layout.itemAt(i).layout()
            for y in range(item.count()):
                if isinstance(item.itemAt(y).widget(), QCheckBox):
                    item.itemAt(y).widget().setCheckState(get_checkstate)

    def delete_selected_files(self, dic_list: list):

        dir_list, file_list = [],[]

        for n in dic_list:
            dir_list.append(n["dir"])
            file_list.append(n["file"])

        dlg = QMessageBox(self)
        dlg.setWindowTitle("Warning")
        dlg.setText("Are you sure, you want to remove the selected files?")
        dlg.setStandardButtons(
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        dlg.setIcon(QMessageBox.Icon.Warning)
        button = dlg.exec()

        if button == QMessageBox.StandardButton.Yes:
            
            FileHandler().delete_files(dir_list)
            for n in file_list:
                self.loaded_files.remove(n)
                correct_widget = self.retrieve_widget_layout_in_scroll_view(label_name=n)

                while correct_widget.count():
                    child = correct_widget.takeAt(0)
                    if child.widget():
                        child.widget().deleteLater()

                self.content_layout.removeItem(correct_widget)

            self.selected_files_list.clear()
            self.delete_selected_button.setEnabled(False)
            
        else:
            print("not deleted")

    
    def file_name_list(self, file_list):
        list = []

        for path in file_list:
            list.append(QFileInfo(path).fileName())

        return str(list)