import sys
import traceback

from weather_service import WeatherService
from weather_gui import WeatherGUI
from PySide6.QtWidgets import QApplication


def main():
    print("[MAIN] Launch the application...")
    try:
        print("[MAIN] Initializing weather service...")
        weather_service = WeatherService()
        print("[MAIN] Weather service has been successfully initialized")

        print("[MAIN] Creating QApplication...")
        app = QApplication(sys.argv)

        print("[MAIN] Creating GUI...")
        gui = WeatherGUI(weather_service)
        gui.show()
        print("[MAIN] GUI has been successfully created")

        print("[MAIN] Launch GUI main loop...")
        app.exec()
        print("[MAIN] GUI main loop has been completed")

    except Exception as e:
        print(f"[ERROR] Critical error in main: {str(e)}")
        print(f"[ERROR] Tracing: {traceback.format_exc()}")
    finally:
        print("[MAIN] Starting clean up procedure...")
        if 'gui' in locals():
            print("[MAIN] Closing GUI...")
            gui.close()
        if 'weather_service' in locals():
            print("[MAIN] Closing weather service...")
            weather_service.close()
        print("[MAIN] Clean up procedure has been completed successfully")


if __name__ == "__main__":
    main()
