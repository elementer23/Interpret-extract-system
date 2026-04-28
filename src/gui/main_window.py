from PyQt6.QtCore import QSize, Qt, QFileInfo, QMutex, QMutexLocker
from utils.utilities import BasicUtils
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
from handler.file_handler import FileHandler, FileOsHandler
from vision.image_handler import ImageHandler
from utils.settings import Settings, PackageSettings
from core.decompress import Decompress
from core.exporter import Exporter
from gui.widgets.menu_menubarwidget import CustomMenu
import os
from gui.widgets.window_showplotwidget import PlotWindow
from gui.events.thread_handler import ThreadHandler

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.lock = QMutex()
        self.active_files = set()
        self.windows = []
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

        self.decomp_button = QPushButton("add file(s)")
        self.decomp_button.setStatusTip("add files whether from compressed folders or loose instances.")
        self.decomp_button.setHidden(True)
        self.decomp_button.clicked.connect(lambda checked: self.run_func(self.decomp, self.main_decomp, checked))

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
        self.export_selected_button.clicked.connect( lambda checked, sfl=self.selected_files_list: self.run_func(self.export_selected_files, None, sfl))

        self.open_selected_button = QPushButton("open selected")
        self.open_selected_button.setStatusTip("open the selected files as images with bounding boxes drawn in them.")
        self.open_selected_button.setEnabled(False)
        self.open_selected_button.clicked.connect( lambda checked, sfl=self.selected_files_list: self.run_func(self.open_selected_files, self.show_plot_window, sfl))

        self.main_checkbox = QCheckBox()
        self.main_checkbox.stateChanged.connect( lambda checked: self.handle_checkbox_state(checked))

        grid_layout.addWidget(QLabel("File(s):"), 1, 0)
        grid_layout.addWidget(self.label, 1, 1)
        grid_layout.addWidget(self.button, 1, 2)
        grid_layout.addWidget(self.decomp_button, 1, 3)
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

        self.threadhandler = ThreadHandler()

    def run_func(self, fn, fn_out, *args, **kwargs):
        kwargs.get("thread_id", 0)
        self.threadhandler.run_event(fn, fn_out, args, kwargs)

    def open_file_dialog(self):
        filter = Settings.retrieve_settings()
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        dialog.setNameFilter(f"{filter['file_selection_name']} {filter['default_file_selection']}")

        if dialog.exec():
            self.label.setText(self.file_name_list(dialog.selectedFiles()))
            self.file_path = dialog.selectedFiles()
            self.decomp_button.setHidden(False)

    def decomp(self, checked, progress_callback, thread_id):
        self.threadhandler.track_progress(progress_callback=progress_callback, thread_id=thread_id)

        return checked

    def main_decomp(self, data):
        path = FileOsHandler().formulate_files_dir()
        target_path = os.path.join(path[0], path[1])
        Decompress(directory=target_path, file_s=self.file_path[:])

        self.dir_content()
        self.decomp_button.setHidden(True)
        self.label.setText("Select...")

    def dir_content(self):
        all_files = FileOsHandler().get_temp_files_dir()
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

            open_image_button.clicked.connect(lambda checked, d=file["dir"]: self.run_func(self.open_file, self.show_plot_window, d))
            export_file_button.clicked.connect(lambda checked, d=file["dir"], f=file["file"]: self.run_func(self.export_file, None, d, f))
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


    def open_file(self, dir, progress_callback, thread_id):

        dir_list = []
        data = dir[0][0] if isinstance(dir, tuple) else dir
        dir_list.append(data)

        with QMutexLocker(self.lock):
                self.active_files.add(data)

        try:
            builder = Handler.pipeline_builder(self, False, Handler.STANDARD_TEXT_BUILD)
            context = builder.run(builder.handler, dir_list[:])

            custom = Handler.pipeline_builder(self, True, None, FileHandler(), ImageHandler())
            image_context = custom.run(custom.handler, dir_list[:])
            plot_data = []
            if context is not None and image_context is not None:
                plot_data = ImageHandler().draw_bounding_box(image_context=image_context, pipeline_context=context)

            self.threadhandler.track_progress(progress_callback=progress_callback, thread_id=thread_id)

            return plot_data
        
        finally:
            with QMutexLocker(self.lock):
                if data in self.active_files:
                    self.active_files.remove(data)
        

    def show_plot_window(self, data):
        try:
            if data:
                plot_window = ""
                for f in data[:]:
                    plot_window = PlotWindow(f)
                    self.windows.append(plot_window)
                    plot_window.show()

                plot_window.destroyed.connect(lambda: self.windows.remove(plot_window))
        except ValueError: pass

    def open_selected_files(self, dic_list, progress_callback, thread_id):
        dir_list = []
        data = dic_list[0][0] if isinstance(dic_list, tuple) else dic_list
 
        for n in data:
            dir_list.append(n["dir"])
            with QMutexLocker(self.lock):
                self.active_files.add(n["dir"])

        try:
             
            builder = Handler.pipeline_builder(self, False, Handler.STANDARD_TEXT_BUILD)
            context = builder.run(builder.handler, dir_list[:])

            custom = Handler.pipeline_builder(self, True, None, FileHandler(), ImageHandler())
            image_context = custom.run(custom.handler, dir_list[:])
            plot_data = []
            if context is not None and image_context is not None:
                plot_data = ImageHandler().draw_bounding_box(image_context=image_context, pipeline_context=context)

            self.threadhandler.track_progress(progress_callback=progress_callback, thread_id=thread_id)

            return plot_data

        finally:
            with QMutexLocker(self.lock):
                for f in data:
                    if f['dir'] in self.active_files:
                        self.active_files.remove(f['dir'])
       

    def export_file(self, file_data, progress_callback, thread_id):
        data, _ = file_data
        dir, file = data

        file = file.split(".")[0]
        dir_list, file_list = [], []
        dir_list.append(dir)
        file_list.append(file)

        with QMutexLocker(self.lock):
            self.active_files.add(dir)

        try:
            builder = Handler.pipeline_builder(self, False, Handler.STANDARD_TEXT_BUILD)
            context = builder.run(builder.handler, dir_list[:])
            if context is not None:
                Exporter().execute_export(context.text_boxes, file_list, PackageSettings.manage_package())

            self.threadhandler.track_progress(progress_callback=progress_callback, thread_id=thread_id)

            return f"{file} has been successfully exported."
        
        finally:
            with QMutexLocker(self.lock):
                if dir in self.active_files:
                    self.active_files.remove(dir)
        

    def export_selected_files(self, dic_list, progress_callback, thread_id):

        data = dic_list[0][0] if isinstance(dic_list, tuple) else dic_list
        dir_list, file_list = [], []
        for n in data:
            dir_list.append(n["dir"])
            file_list.append(n["file"].split(".")[0])

            with QMutexLocker(self.lock):
                self.active_files.add(n["dir"])

        try:

            builder = Handler.pipeline_builder(self, False, Handler.STANDARD_TEXT_BUILD)
            context = builder.run(builder.handler, dir_list[:])
            if context is not None:
                Exporter().execute_export(context.text_boxes, file_list, PackageSettings.manage_package())

            self.threadhandler.track_progress(progress_callback=progress_callback, thread_id=thread_id)

            return f"{file_list} has or have been successfully exported."

        finally:
            with QMutexLocker(self.lock):
                for f in data:
                    if f["dir"] in self.active_files:
                        self.active_files.remove(f["dir"])
        

    def delete_file(self, dir, file):
        path = FileOsHandler().formulate_files_dir()
        target_path = os.path.join(path[0], path[1])

        with QMutexLocker(self.lock):
            if dir in self.active_files:
                print(f"Can not delete the file, cause {file} is still active in another thread.")
                return

        FileOsHandler().delete_file(dir)
        self.loaded_files.remove(file)
        if {"dir": dir, "file": file} in self.selected_files_list:
            self.selected_files_list.remove({"dir": dir, "file": file})

        correct_item = self.retrieve_widget_layout_in_scroll_view(label_name=file)

        while correct_item.count():
            child = correct_item.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        self.content_layout.removeItem(correct_item)

        if not self.selected_files_list:
            self.delete_selected_button.setEnabled(False)
            self.export_selected_button.setEnabled(False)
            self.open_selected_button.setEnabled(False)

        if BasicUtils.is_directory_empty(dir_path=target_path):
            FileOsHandler().remove_dir(dir_path=target_path)
            self.main_checkbox.setEnabled(False)
            self.main_checkbox.setCheckState(Qt.CheckState.Unchecked)

    def retrieve_widget_layout_in_scroll_view(self, label_name: str):
        for i in reversed(range(self.content_layout.count() - 1)):
            item = self.content_layout.itemAt(i).layout()

            for y in range(item.count()):
                if isinstance(item.itemAt(y).widget(), QLabel):
                    if item.itemAt(y).widget().text() == label_name:
                        return item

    def check_box_checked(self, dir, file, checked):
        if Qt.CheckState(checked) == Qt.CheckState.Checked:
            self.selected_files_list.append({"dir": dir, "file": file})
        else:
            self.selected_files_list.remove({"dir": dir, "file": file})

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
        path = FileOsHandler().formulate_files_dir()
        target_path = os.path.join(path[0], path[1])

        dir_list, file_list = [],[]

        for n in dic_list:
            dir_list.append(n["dir"])
            file_list.append(n["file"])
            with QMutexLocker(self.lock):
                if n["dir"] in self.active_files:
                    print(f"The file or files are still active and can't be deleted, files in question {file_list}")
                    return

        dlg = QMessageBox(self)
        dlg.setWindowTitle("Warning")
        dlg.setText("Are you sure, you want to remove the selected files?")
        dlg.setStandardButtons(
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        dlg.setIcon(QMessageBox.Icon.Warning)
        button = dlg.exec()

        if button == QMessageBox.StandardButton.Yes:
            
            FileOsHandler().delete_files(dir_list)
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
            self.export_selected_button.setEnabled(False)
            self.open_selected_button.setEnabled(False)
            
            if BasicUtils.is_directory_empty(dir_path=target_path):
                FileOsHandler().remove_dir(dir_path=target_path)
                self.main_checkbox.setEnabled(False)
                self.main_checkbox.setCheckState(Qt.CheckState.Unchecked)
            
        else:
            print("not deleted")

    
    def file_name_list(self, file_list):
        list = []

        for path in file_list:
            list.append(QFileInfo(path).fileName())

        return str(list)