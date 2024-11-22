from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton

class BrowserSettings(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.label = QLabel("Zadajte URL pre kiosk režim:", self)
        layout.addWidget(self.label)

        self.url_input = QLineEdit(self)
        self.url_input.setPlaceholderText("https://example.com")
        layout.addWidget(self.url_input)

        self.save_button = QPushButton("Uložiť URL", self)
        self.save_button.clicked.connect(self.save_url)
        layout.addWidget(self.save_button)

        self.setLayout(layout)
        self.load_current_url()

    def load_current_url(self):
        try:
            with open("/opt/tterminal/kiosk_url.txt", "r") as file:
                self.url_input.setText(file.read().strip())
        except FileNotFoundError:
            self.url_input.setText("")

    def save_url(self):
        url = self.url_input.text().strip()
        if url:
            try:
                with open("/opt/tterminal/kiosk_url.txt", "w") as file:
                    file.write(url)
                print("URL uložená:", url)
            except Exception as e:
                print(f"Chyba pri ukladaní URL: {e}")

# Pridajte do hlavného okna aplikácie
self.addTab(BrowserSettings(), "Browser")
