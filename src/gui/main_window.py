from PyQt6.QtCore import QSize, Qt

from PyQt6.QtWidgets import (QMainWindow, QVBoxLayout)
from gui.widgets.menu_menubarwidget import CustomMenu

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("interpret & extract")

        self.setMinimumSize(QSize(400, 300))
        self.setMaximumSize(QSize(1000, 900))

        self.setMenuBar(CustomMenu(self))
    
        