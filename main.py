#!/usr/bin/env python
import sys

from PySide6 import QtWidgets

from interface.mainwindow import MainWindow

if __name__ == "__main__":
    app = QtWidgets.QApplication()
    mainWindow = MainWindow()
    mainWindow.buildUI()
    mainWindow.show()
    sys.exit(app.exec())
