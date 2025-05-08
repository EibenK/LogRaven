import logging
import sys
from PyQt5.QtGui import QGuiApplication
from PyQt5 .QtCore import Qt
from PyQt5.QtWidgets import (
    QLabel, QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QPushButton, QTabWidget, QCheckBox, QFrame,
    QSpacerItem, QSizePolicy
)

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LogRaven — SIEM Dashboard")

        main_widget = QWidget()
        main_layout = QHBoxLayout()

        self.dashboard_page = DashboardPage()
        self.settings_page = SettingsPage()
        
        tabs = QTabWidget()
        tabs.addTab(self.dashboard_page, "DashBoard")
        tabs.addTab(self.settings_page, "Settings")

        tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #ccc;
                border-top-right-radius: 12px;
                border-bottom-left-radius: 12px;
                border-bottom-right-radius: 12px;
                background-color: #fdfdfd;
                padding: 0px;
                margin-top: -1px;  /* Overlap tab bar to eliminate line gap */
            }

            QTabBar::tab {
                background: #e0e0e0;
                border: 1px solid #aaa;
                border-bottom: none;
                border-top-right-radius: 10px;
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
                min-width: 120px;
                padding: 8px 16px;
                margin-right: 2px;
            }

            QTabBar::tab:selected {
                background: #ffffff;
                font-weight: bold;
            }

            QTabBar::tab:!selected {
                margin-top: 2px;  /* Makes non-selected tabs appear slightly lower */
            }
        """)

        container = QWidget()
        container_layout = QVBoxLayout()
        container_layout.setContentsMargins(20, 20, 20, 20)
        container_layout.addWidget(tabs, stretch=1)
        container.setLayout(container_layout)

        self.setCentralWidget(container)

        screen_geometry = QGuiApplication.primaryScreen().availableGeometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()

        # dynamically resize the application to fit 75% of the screen
        target_width = int(screen_width * 0.75) 
        target_height = int(screen_height * 0.75)
        self.resize(target_width, target_height)
        
class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()
        main_layout = QVBoxLayout()
        verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        diagnostics_title_row = QHBoxLayout()
        diagnostics_title_row.addWidget(InfoBox("Diagnostics"))

        diagnostics_row = QHBoxLayout()
        diagnostics_row.addWidget(InfoBox("0"))
        diagnostics_row.addWidget(InfoBox("0"))
        diagnostics_row.addWidget(InfoBox("0"))
        diagnostics_row.addWidget(InfoBox("0"))
        diagnostics_row.addWidget(InfoBox("0"))
        diagnostics_row.addWidget(InfoBox("0"))
        
        sys_info_title_row = QHBoxLayout()
        sys_info_title_row.addWidget(InfoBox("System Status"))
        sys_info_title_row.addWidget(InfoBox("Events"))
        sys_info_title_row.addWidget(InfoBox("Agent Count"))

        sys_info_row = QHBoxLayout()
        sys_info_row.addWidget(InfoBox("0"))
        sys_info_row.addWidget(InfoBox("0"))
        sys_info_row.addWidget(InfoBox("0"))
        

        main_layout.addLayout(diagnostics_title_row)
        main_layout.addLayout(diagnostics_row)
        main_layout.addItem(verticalSpacer)
        main_layout.addLayout(sys_info_title_row)
        main_layout.addLayout(sys_info_row)
        main_layout.addItem(verticalSpacer)
        self.setLayout(main_layout)

class InfoBox(QFrame):
    # I want to add customizable parameters here 
    def __init__(self, title="Title", bg_color="#f0f0f0"):
        super().__init__()
        self.setFrameStyle(QFrame.StyledPanel)
        self.setMaximumHeight(80)
        self.setStyleSheet(f"""
            QFrame {{
                border-radius: 8px;
                background-color: {bg_color};
                padding: 10px;
            }}
        """)
        layout = QVBoxLayout()
        content_info = QLabel(f"<b>{title}</b>")
        content_info.setAlignment(Qt.AlignCenter)
        layout.addWidget(content_info)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(2)
        self.setLayout(layout)


class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()    
        page_layout = QVBoxLayout()
        
        # notification setting within the Settings Page
        notifications_layout = QHBoxLayout()
        notifications_layout.addWidget(QLabel("Enable Notifications"))
        notifications_checkbox = QCheckBox()
        notifications_checkbox.setCheckable(True)
        notifications_layout.addWidget(notifications_checkbox)
        page_layout.addLayout(notifications_layout)

        # add more settings here with similar structure from before

        self.setLayout(page_layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())