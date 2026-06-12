from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QAction, QIcon, QKeySequence
from PyQt6.QtWidgets import (QMenuBar, QStatusBar)
from gui.widgets.window_settingswidget import SettingsWindow
from gui.widgets.window_exportimagewidget import ExportImageWindow
from gui.widgets.window_convertdatasetwidget import ConvertDatasetWindow
from gui.widgets.window_imageto_pdfwidget import ImageToPDFWindow
from gui.widgets.window_generate_extracteddatawidget import GenerateExtractedDataPDF
from gui.widgets.window_labelstudiowidget import LabelStudioWindow
import atexit

class CustomMenu(QMenuBar):
    def __init__(self, parent=None):
        super().__init__(parent)

        open_label_studio = QAction("&label studio", self)
        open_label_studio.setStatusTip("label studio dataset labeling")
        open_label_studio.setShortcut(QKeySequence("Ctrl+l"))
        open_label_studio.triggered.connect(self.open_label_studio_window)

        open_settings = QAction("&open settings", self)
        open_settings.setStatusTip("open the settings")
        open_settings.setShortcut(QKeySequence("Ctrl+o"))
        open_settings.triggered.connect(self.open_setting_window)

        open_export_image = QAction("&file(s) to image(s)", self)
        open_export_image.setStatusTip("export file(s) to image(s)")
        open_export_image.setShortcut(QKeySequence("Ctrl+Shift+i"))
        open_export_image.triggered.connect(self.open_export_image_window)

        open_coco_converter = QAction("&coco to yolo", self)
        open_coco_converter.setStatusTip("convert a coco dataset to yolo dataset")
        open_coco_converter.setShortcut(QKeySequence("Ctrl+Shift+c"))
        open_coco_converter.triggered.connect(self.open_coco_converter_window)

        open_image_to_pdf = QAction("&image to pdf", self)
        open_image_to_pdf.setStatusTip("convert image to pdf")
        open_image_to_pdf.setShortcut(QKeySequence("Ctrl+p"))
        open_image_to_pdf.triggered.connect(self.open_image_to_pdf_window)

        open_generate_data_pdf = QAction("&generate data on pdf", self)
        open_generate_data_pdf.setStatusTip("generate extracted data on pdf")
        open_generate_data_pdf.setShortcut(QKeySequence("Ctrl+g"))
        open_generate_data_pdf.triggered.connect(self.open_generate_data_pdf_window)

        parent.setStatusBar(QStatusBar(self))

        options_menu = self.addMenu("&Options")
        options_insertmenu = options_menu.addMenu("options")
        options_convertmenu = options_menu.addMenu("convert")
        options_insertmenu.addActions([open_export_image, open_settings])
        options_convertmenu.addActions([open_image_to_pdf, open_generate_data_pdf])

        training_menu = self.addMenu("&Training")
        training_menu.addActions([open_label_studio, open_coco_converter])

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

    def open_coco_converter_window(self):
        self.coco_converter_window = ConvertDatasetWindow()
        self.coco_converter_window.show()

    def open_image_to_pdf_window(self):
        self.image_to_pdf_window = ImageToPDFWindow()
        self.image_to_pdf_window.show()

    def open_generate_data_pdf_window(self):
        self.generate_data_pdf_window = GenerateExtractedDataPDF()
        self.generate_data_pdf_window.show()

    def open_label_studio_window(self):
        self.label_studio_window = LabelStudioWindow()
        self.label_studio_window.show()

        atexit.register(self.label_studio_window.label_studio_controller.close)