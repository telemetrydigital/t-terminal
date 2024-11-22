from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QDateTimeEdit, QMessageBox
from PyQt5.QtCore import QDateTime
from backend.time_settings import set_time, set_ntp_server

class TimePage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Nadpis
        title = QLabel("Time Settings")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)

        # Čas a dátum
        datetime_label = QLabel("Set Date and Time:")
        self.datetime_edit = QDateTimeEdit(QDateTime.currentDateTime())
        self.datetime_edit.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        layout.addWidget(datetime_label)
        layout.addWidget(self.datetime_edit)

        # NTP server
        ntp_label = QLabel("Set NTP Server:")
        self.ntp_input = QLineEdit()
        self.ntp_input.setPlaceholderText("Enter NTP server address (e.g., pool.ntp.org)")
        layout.addWidget(ntp_label)
        layout.addWidget(self.ntp_input)

        # Uložiť tlačidlo
        save_button = QPushButton("Save Settings")
        save_button.clicked.connect(self.save_settings)
        layout.addWidget(save_button)

        # Nastaviť hlavný layout
        self.setLayout(layout)

    def save_settings(self):
        try:
            # Získaj čas a dátum z editora
            datetime_value = self.datetime_edit.dateTime().toString("yyyy-MM-dd HH:mm:ss")
            date, time = datetime_value.split(" ")

            # Nastav čas
            set_time(date, time)

            # Získaj NTP server a nastav ho (ak je zadaný)
            ntp_server = self.ntp_input.text()
            if ntp_server:
                set_ntp_server(ntp_server)

            # Zobraz potvrdenie
            QMessageBox.information(self, "Success", "Time and NTP settings saved successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save settings: {str(e)}")

