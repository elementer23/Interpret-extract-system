from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent))
from src.config import DEVICE
from PyQt6.QtWidgets import QApplication
from gui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()

if __name__ == "__main__":
    main()