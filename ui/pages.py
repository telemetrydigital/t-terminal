from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

class TimePage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Time Settings"))
        self.setLayout(layout)

class NetworkPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Network Settings"))
        self.setLayout(layout)

class DisplayPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Display Settings"))
        self.setLayout(layout)

class BrowserPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Browser Settings"))
        self.setLayout(layout)

class VPNPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("VPN Settings"))
        self.setLayout(layout)

class SystemPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("System Settings"))
        self.setLayout(layout)

class AboutPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("About TTerminal"))
        self.setLayout(layout)
