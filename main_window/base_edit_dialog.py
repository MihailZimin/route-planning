"""
Base edit window class.

This module provides:
- base class EditDialogWindow for editing geometry object.

"""


from PyQt6 import uic
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QDialog, QWidget

from draw.abstract_drawer import ABCDrawer


class EditDialogWindow(QDialog):
    """
    Edit window class for editing geo objects.
    """

    def __init__(self, geo_object : ABCDrawer, path: str, parent: QWidget = None) -> None:
        """
        Create edit window object.

        Args:

            geo_object: geometry object which will be edited.
            path: path to the ui file with dialog window for current object.
            parent: parent window.
        """
        super().__init__(parent)
        self._geo_object = geo_object
        self.InitializeWin(path)
        self.loadParams()

    def InitializeWin(self, path: str) -> None:
        """
        Initialize edit window.

        Args:

            path: path to the ui file with dialog window.
        """
        uic.loadUi(path, self)
        self.setMinimumSize(QSize(400, 210))
        self.buttonBox.accepted.disconnect()
        self.buttonBox.accepted.connect(self.validateAccept)
        self.buttonBox.rejected.connect(self.reject)

    def validateAccept() -> None:
        """
        Slot for accept button with validation of object parameters.
        """

    def loadParams(self) -> None:
        """
        Load current parameters of geo object.
        """
