import secrets
from typing import TYPE_CHECKING

from PySide6.QtCore import QFile, QIODevice
from PySide6.QtWebEngineCore import (
    QWebEngineProfile,
    QWebEngineScript,
    QWebEngineSettings,
)

from runekit.browser.api import RuneKitSchemeHandler
from runekit.browser.scheme import RuneKitScheme

if TYPE_CHECKING:
    from runekit.app import App


class WebProfile(QWebEngineProfile):
    rpc_secret: str
    app: "App"

    def __init__(self, app=None, parent=None):
        super().__init__("app", parent=parent)
        self.app = app
        self.rpc_secret = secrets.token_urlsafe(64)
        self._insert_scheme_handlers()
        self._insert_alt1_api()
        self.settings().setAttribute(
            QWebEngineSettings.WebAttribute.PlaybackRequiresUserGesture, False
        )
        self.settings().setAttribute(QWebEngineSettings.WebAttribute.PdfViewerEnabled, False)
        self.settings().setAttribute(QWebEngineSettings.WebAttribute.ScreenCaptureEnabled, False)
        self.settings().setAttribute(QWebEngineSettings.WebAttribute.AutoLoadIconsForPage, False)

    def _insert_scheme_handlers(self):
        self.installUrlSchemeHandler(
            RuneKitScheme.scheme,
            RuneKitSchemeHandler(
                rpc_secret=self.rpc_secret.encode("ascii"),
                api=self.app.get_api(),
                parent=self,
            ),
        )

    def _insert_alt1_api(self):
        qwc_file = QFile(":/qtwebchannel/qwebchannel.js", parent=self)
        if not qwc_file.open(QIODevice.OpenModeFlag.ReadOnly):
            raise IOError
        src = bytes(qwc_file.readAll()).decode("utf8")
        qwc_file.close()

        src += "\n;;\n"

        alt1_file = QFile(":/runekit/browser/alt1.js", parent=self)
        if not alt1_file.open(QIODevice.OpenModeFlag.ReadOnly):
            raise IOError
        src += bytes(alt1_file.readAll()).decode("utf8")
        alt1_file.close()

        script = QWebEngineScript()
        script.setName("alt1.js")
        script.setWorldId(QWebEngineScript.ScriptWorldId.MainWorld)
        script.setInjectionPoint(QWebEngineScript.InjectionPoint.DocumentCreation)
        script.setSourceCode(src.replace("%%RPC_TOKEN%%", self.rpc_secret))
        script.setRunsOnSubFrames(True)

        self.scripts().insert(script)
