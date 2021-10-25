import sys
from PyQt5.QtWidgets import QApplication
from ui.main_window import Window

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())