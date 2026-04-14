from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QAction, QIcon, QKeySequence
from PyQt6.QtWidgets import (QMenuBar, QStatusBar)
from gui.widgets.dialog_insertsinglewidget import CustomDialog
from gui.widgets.window_insertsinglewidget import InsertSingleFileWindow
from gui.widgets.window_insertbulkwidget import InsertBulkFileWindow
from gui.widgets.window_insertzipwidget import InsertZipFileWindow
from gui.widgets.window_settingswidget import SettingsWindow
from gui.widgets.window_exportimagewidget import ExportImageWindow

class CustomMenu(QMenuBar):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.insert_single_file_window = InsertSingleFileWindow()
        self.insert_bulk_file_window = InsertBulkFileWindow()
        self.insert_zip_file_window = InsertZipFileWindow()

        insert_action = QAction("&new file", self)
        insert_action.setStatusTip("insert file")
        insert_action.setShortcut(QKeySequence("Ctrl+i"))
        insert_action.triggered.connect( lambda checked: self.open_insert_window(self.insert_single_file_window))

        insert_bulk = QAction("&multiple files", self)
        insert_bulk.setStatusTip("insert bulk of files")
        insert_bulk.setShortcut(QKeySequence("Ctrl+Shift+b"))
        insert_bulk.triggered.connect( lambda checked: self.open_insert_window(self.insert_bulk_file_window))

        insert_zip = QAction("&add zip", self)
        insert_zip.setStatusTip("insert files in zip")
        insert_zip.setShortcut(QKeySequence("Ctrl+Shift+z"))
        insert_zip.triggered.connect( lambda checked: self.open_insert_window(self.insert_zip_file_window))

        open_settings = QAction("&open settings", self)
        open_settings.setStatusTip("open the settings")
        open_settings.setShortcut(QKeySequence("Ctrl+o"))
        open_settings.triggered.connect(self.open_setting_window)

        open_export_image = QAction("&file(s) to image(s)", self)
        open_export_image.setStatusTip("export file(s) to image(s)")
        open_export_image.setShortcut(QKeySequence("Ctrl+Shift+i"))
        open_export_image.triggered.connect(self.open_export_image_window)

        parent.setStatusBar(QStatusBar(self))

        file_menu = self.addMenu("&File")
        file_insertmenu = file_menu.addMenu("insert")
        file_insertmenu.addActions([insert_action, insert_bulk, insert_zip])

        options_menu = self.addMenu("&Options")
        options_insertmenu = options_menu.addMenu("options")
        options_insertmenu.addActions([open_export_image, open_settings])

    def open_insert_window(self, window):
        if window.isVisible():
            window.hide()
        else:
            window.show()

    def open_setting_window(self):
        self.settings_window = SettingsWindow()
        self.settings_window.show()

    def open_export_image_window(self):
        self.export_image_window = ExportImageWindow()
        self.export_image_window.show()