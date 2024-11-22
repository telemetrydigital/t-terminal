from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QStackedWidget, QPushButton, QHBoxLayout
from ui.pages import TimePage, NetworkPage, DisplayPage, BrowserPage, VPNPage, SystemPage, AboutPage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TTerminal")
        self.setGeometry(100, 100, 800, 480)

        # Hlavné rozloženie
        layout = QHBoxLayout()
        self.menu_widget = self.create_menu()
        self.content_widget = QStackedWidget()

        layout.addWidget(self.menu_widget)
        layout.addWidget(self.content_widget)

        main_widget = QWidget()
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

        # Pridanie stránok
        self.time_page = TimePage()
        self.network_page = NetworkPage()
        self.display_page = DisplayPage()
        self.browser_page = BrowserPage()
        self.vpn_page = VPNPage()
        self.system_page = SystemPage()
        self.about_page = AboutPage()

        self.content_widget.addWidget(self.time_page)
        self.content_widget.addWidget(self.network_page)
        self.content_widget.addWidget(self.display_page)
        self.content_widget.addWidget(self.browser_page)
        self.content_widget.addWidget(self.vpn_page)
        self.content_widget.addWidget(self.system_page)
        self.content_widget.addWidget(self.about_page)

    def create_menu(self):
        menu_layout = QVBoxLayout()
        menu_buttons = {
            "Time": lambda: self.show_page(self.time_page),
            "Network": lambda: self.show_page(self.network_page),
            "Display": lambda: self.show_page(self.display_page),
            "Browser": lambda: self.show_page(self.browser_page),
            "VPN": lambda: self.show_page(self.vpn_page),
            "System": lambda: self.show_page(self.system_page),
            "About": lambda: self.show_page(self.about_page),
        }
        for name, callback in menu_buttons.items():
            button = QPushButton(name)
            button.clicked.connect(callback)
            menu_layout.addWidget(button)
        
        menu_widget = QWidget()
        menu_widget.setLayout(menu_layout)
        return menu_widget

    def show_page(self, page):
        self.content_widget.setCurrentWidget(page)
