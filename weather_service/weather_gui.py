import traceback

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QLabel, QPushButton, QVBoxLayout
)
from PySide6.QtCore import Qt, QTimer, Signal, QObject, QThread, Slot
from PySide6.QtGui import QPixmap, QColor, QPainter, QFont
from datetime import datetime


class WeatherUpdateWorker(QObject):
    weather_updated = Signal(dict)
    error = Signal(str)
    finished = Signal()
    trigger_update = Signal()  # Add this line

    def __init__(self, weather_service, city, interval_sec):
        super().__init__()
        self.weather_service = weather_service
        self.city = city
        self.interval_sec = interval_sec
        self.running = True
        self._manual_update_requested = False
        self.trigger_update.connect(self.request_manual_update)

    @Slot()
    def request_manual_update(self):
        self._manual_update_requested = True

    def run(self):
        import time
        print("[WORKER] Worker thread started")
        while self.running:
            try:
                print("[WORKER] Fetching weather data...")
                data = self.weather_service.get_weather(self.city)
                print("[WORKER] Weather data received")
                self.weather_updated.emit(data)
            except Exception as e:
                print(f"[WORKER] Error fetching weather: {str(e)}")
                self.error.emit(str(e))

            wait_time = 0
            while wait_time < self.interval_sec and self.running:
                if self._manual_update_requested:
                    print("[WORKER] Manual update requested")
                    self._manual_update_requested = False
                    break
                time.sleep(0.1)
                wait_time += 0.1
        print("[WORKER] Worker thread stopped")
        self.finished.emit()

    def stop(self):
        self.running = False


class WeatherGUI(QMainWindow):
    def __init__(self, weather_service):
        super().__init__()
        self.weather_service = weather_service
        self.city = "Poltava"
        self.setWindowTitle("Weather App")
        self.setFixedSize(400, 500)

        title_font = QFont("Arial", 16, QFont.Bold)
        value_font = QFont("Arial", 14, QFont.Bold)
        label_font = QFont("Arial", 12)

        value_style = "color: #0066cc; font-weight: bold;"
        error_style = "color: #cc0000; font-weight: bold; font-size: 14px;"

        main_layout = QVBoxLayout()

        self.icon_label = QLabel()
        self.icon_label.setFixedSize(96, 96)
        self.icon_label.setAlignment(Qt.AlignCenter)

        self.city_label = QLabel("City: ...")
        self.city_label.setFont(label_font)

        self.temp_label = QLabel("Temperature: ...")
        self.temp_label.setFont(label_font)

        self.cond_label = QLabel("Weather: ...")
        self.cond_label.setFont(label_font)

        self.last_update_label = QLabel("Latest update: ...")

        self.error_label = QLabel()
        self.error_label.setStyleSheet(error_style)

        self.update_btn = QPushButton("Update the weather")
        self.update_btn.setFont(value_font)
        self.update_btn.setFixedHeight(40)
        self.update_btn.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
        self.update_btn.clicked.connect(self.manual_update)

        main_layout.addWidget(self.icon_label)
        main_layout.addWidget(self.city_label)
        main_layout.addWidget(self.temp_label)
        main_layout.addWidget(self.cond_label)
        main_layout.addWidget(self.last_update_label)
        main_layout.addWidget(self.error_label)
        main_layout.addWidget(self.update_btn)

        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        self.icons = self.load_icons()

        self.weather_data = None

        self.worker = WeatherUpdateWorker(self.weather_service, self.city, 300)
        self.thread = QThread()
        self.worker.moveToThread(self.thread)
        self.worker.weather_updated.connect(self.on_weather_update)
        self.worker.error.connect(self.on_error)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.thread.start()

        self.manual_update()

    def load_icons(self):
        pix = QPixmap(96, 96)
        pix.fill(Qt.transparent)

        painter = QPainter(pix)
        # Draw top half (blue)
        painter.setBrush(QColor(0, 87, 183))
        painter.setPen(Qt.NoPen)
        painter.drawRect(0, 0, 96, 48)

        painter.setBrush(QColor(255, 215, 0))
        painter.drawRect(0, 48, 96, 48)

        painter.end()

        icons = {
            "clear": pix,
            "clouds": pix,
            "rain": pix,
            "snow": pix,
            "default": pix
        }
        return icons

    def manual_update(self):
        self.update_btn.setEnabled(False)
        self.update_btn.setText("Update...")
        self.error_label.setText("")

        try:
            print("[GUI] Directly fetching weather data...")
            data = self.weather_service.get_weather(self.city)
            print(f"[GUI] Direct fetch result: {data}")
            self.on_weather_update(data)
        except Exception as e:
            print(f"[GUI] Direct fetch error: {str(e)}")
            traceback.print_exc()

        self.worker.trigger_update.emit()
        print("[GUI] Manual update requested")

        QTimer.singleShot(5000, self.reset_update_button)

    def on_weather_update(self, data):
        print(f"[GUI] Weather data received in GUI: {data}")
        self.weather_data = data
        self.error_label.setText("")

        self.update_btn.setEnabled(True)
        self.update_btn.setText("Update the weather")
        self.refresh_ui()

    def on_error(self, msg):
        print(f"[GUI] Error received: {msg}")
        self.error_label.setText(f"Error: {msg}")

        self.update_btn.setEnabled(True)
        self.update_btn.setText("Update the weather")

    def refresh_ui(self):
        if not self.weather_data:
            print("[GUI] No weather data available")
            self.city_label.setText("City: ...")
            self.temp_label.setText("Temperature: ...")
            self.cond_label.setText("Weather: ...")
            self.icon_label.setPixmap(self.icons.get("default", QPixmap()))
            self.last_update_label.setText("Latest update: ...")
            return

        print(f"[GUI] Refreshing UI with data: {self.weather_data}")

        location = self.weather_data.get("location", {}).get("city", "Unknown")
        temp = self.weather_data.get("temperature", {}).get("celsius", "N/A")
        condition = self.weather_data.get("description", "default")

        print(f"[GUI] Extracted: location={location}, temp={temp}, condition={condition}")

        self.city_label.setText(f"City: <b><span style='color: #0066cc;'>{location}</span></b>")
        self.temp_label.setText(f"Temperature: <b><span style='color: #0066cc;'>{temp}°C</span></b>")
        self.cond_label.setText(f"Weather: <b><span style='color: #0066cc;'>{condition}</span></b>")

        icon_key = "default"
        if condition:
            condition_lower = condition.lower()
            for key in self.icons.keys():
                if key in condition_lower:
                    icon_key = key
                    break

        print(f"[GUI] Using icon: {icon_key}")
        pix = self.icons.get(icon_key, self.icons.get('default', QPixmap()))
        self.icon_label.setPixmap(pix)

        self.last_update_label.setText(f"Latest update: <b>{datetime.now().strftime('%H:%M:%S')}</b>")

    def closeEvent(self, event):
        self.worker.stop()
        self.thread.quit()
        self.thread.wait()
        event.accept()

    def reset_update_button(self):
        if not self.update_btn.isEnabled() and self.update_btn.text() == "Update...":
            self.update_btn.setEnabled(True)
            self.update_btn.setText("Update the weather")
            self.error_label.setText("Update timed out. Try again.")
            print("[GUI] Update timed out")
