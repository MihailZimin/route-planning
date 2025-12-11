"""
Entry point.

This is the entrance to the app.
"""


import faulthandler
import sys

faulthandler.enable()

from PyQt6.QtWidgets import QApplication

from main_window.mainwindow import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    app.exec()
