import sys

from PyQt5.QtWidgets import QApplication
from core.information_center import InformationCenter
from views.main_window import MainWindow

class Main:
    def __init__(self):
        app = QApplication(sys.argv)
        
        info_center = InformationCenter()
        registeries = info_center.get_registered()
        print(registeries)

        window = MainWindow()
        window.show()

        sys.exit(app.exec_())


if __name__ == "__main__":
    app = Main()
