import sys
from PyQt5.QtWidgets import QLabel, QApplication, QMainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LogRaven SIEM Dashboard")
        self.setGeometry(500, 500, 800, 600)

        self.label = QLabel("Welcome to LogRaven", self)
        self.label.move(300,0)
        self.label.adjustSize()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())