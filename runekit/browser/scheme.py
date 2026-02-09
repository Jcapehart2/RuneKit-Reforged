from PySide6.QtWebEngineCore import (
    QWebEngineUrlScheme,
)


class RuneKitScheme(QWebEngineUrlScheme):
    scheme = b"rk"

    def __init__(self):
        super().__init__(self.scheme)
        self.setSyntax(QWebEngineUrlScheme.Syntax.Path)
        self.setDefaultPort(QWebEngineUrlScheme.PortUnspecified)
        self.setFlags(
            QWebEngineUrlScheme.Flag.SecureScheme
            | QWebEngineUrlScheme.Flag.ContentSecurityPolicyIgnored
            | QWebEngineUrlScheme.Flag.CorsEnabled
        )


class Alt1Scheme(QWebEngineUrlScheme):
    scheme = b"alt1"

    def __init__(self):
        super().__init__(self.scheme)
        self.setSyntax(QWebEngineUrlScheme.Syntax.Path)
        self.setDefaultPort(QWebEngineUrlScheme.PortUnspecified)


def register():
    QWebEngineUrlScheme.registerScheme(Alt1Scheme())
    QWebEngineUrlScheme.registerScheme(RuneKitScheme())
