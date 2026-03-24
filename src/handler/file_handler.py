from PyQt6.QtWidgets import QFileDialog

class FileHandler():
    def __init__(self):
        super().__init__()

    def select_file_from_explorer(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)