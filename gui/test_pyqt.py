import sys
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("App")
        self.setGeometry(100, 100, 400, 200)  # x, y, width, height
        
        # Создаем надпись
        label = QLabel("Hello, PyQT!", self)
        label.move(150, 80)  # Позиционируем надпись
        label.setStyleSheet("font-size: 20px;")  # Стиль текста

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())