from PyQt6.QtCore import QSize, Qt
from handler.file_handler import FileHandler
from PyQt6.QtWidgets import (
    QLabel,
    QPushButton,
    QStyle,
    QVBoxLayout,
    QWidget,
    QFileDialog,
    QLineEdit,
    QGroupBox,
    QFormLayout
)

class ImageToPDFWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Change image to pdf")
        self.setMinimumSize(QSize(300, 200))
        self.setMaximumSize(QSize(500, 400))

        self.file_path = ""

        main_layout = QVBoxLayout()

        group_box = QGroupBox("image to pdf")
        form_layout = QFormLayout()

        self.label = QLabel("File chosen:")
        icon = self.style().standardIcon(QStyle.StandardPixmap.SP_DirIcon)

        self.button = QPushButton("choose file")
        self.button.setIcon(icon)
        self.button.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.button.clicked.connect(self.open_dir)

        self.name_file_to = QLineEdit()

        self.convert_button = QPushButton("convert to pdf")
        self.convert_button.setDisabled(True)
        self.convert_button.clicked.connect(self.run_convert)

        form_layout.addRow(self.label, self.button)
        form_layout.addRow(QLabel("name file:"), self.name_file_to)
        form_layout.addRow(self.convert_button)
        group_box.setLayout(form_layout)
        main_layout.addWidget(group_box)

        self.setLayout(main_layout)

    def open_dir(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.FileMode.ExistingFile)

        if dialog.exec():
            self.label.setText(f"File chosen: {dialog.selectedFiles()[0]}")
            self.file_path = dialog.selectedFiles()[0]
            self.convert_button.setDisabled(False)


    def run_convert(self):
        FileHandler().image_to_pdf(self.file_path, self.name_file_to.text())
        self.convert_button.setDisabled(True)

