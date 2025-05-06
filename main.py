import logging
import sys

from PyQt5.QtWidgets import QApplication

from core.information_center import InformationCenter
from views.main_window import MainWindow

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(name)s %(message)s'
)

logger = logging.getLogger(__name__)


class Main:
    def __init__(self):
        app = QApplication(sys.argv)
        info_center = InformationCenter()
        services = info_center.get_services()
        info_center.start_monitoring()

        window = MainWindow()
        window.show()

        sys.exit(app.exec_())


if __name__ == "__main__":
    app = Main()
