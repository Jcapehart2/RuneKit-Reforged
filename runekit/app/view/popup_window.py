import logging

from PySide6.QtCore import Qt, QSize

from .browser_window import BrowserWindow


class PopupWindow(BrowserWindow):
    logger: logging.Logger

    def __init__(self, **kwargs):
        super().__init__(flags=Qt.WindowType.Dialog | Qt.WindowType.WindowStaysOnTopHint, **kwargs)
        self.logger = logging.getLogger(
            __name__
            + "."
            + self.__class__.__name__
            + "."
            + self.app.manifest["appName"]
        )
        self.setWindowTitle(self.app.manifest["appName"])

    def sizeHint(self) -> QSize:
        return QSize(300, 500)
