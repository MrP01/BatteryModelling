#!/usr/bin/env python
"""Welcome to the main simulation file, running me starts up the battery simulator! :)
The interface code is contained within interface/mainwindow.py.
Get to know the code by starting from there (or simulator/simulation.py).
"""
import argparse
import sys

from PySide6 import QtWidgets

from interface.mainwindow import MainWindow

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--locality", default="example")
    args = parser.parse_args()
    app = QtWidgets.QApplication()
    mainWindow = MainWindow(args.locality)
    mainWindow.buildUI()
    mainWindow.show()
    sys.exit(app.exec())
