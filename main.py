import os
import sys
from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow

def check_display():
    """
    Overí, či je nastavená premenná DISPLAY a či je X server dostupný.
    """
    if "DISPLAY" not in os.environ:
        print("[ERROR] DISPLAY variable not set. Please ensure Xorg is running.")
        sys.exit(1)

if __name__ == "__main__":
    # Overenie prostredia
    check_display()

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
