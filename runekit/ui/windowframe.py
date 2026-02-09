from PySide6.QtCore import Signal, QPoint, Qt
from PySide6.QtGui import QPixmap, QResizeEvent
from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QSizePolicy,
    QPushButton,
)

SKIN = ":/runekit/ui/skins/default/"


class WindowFrame(QWidget):
    on_minimize = Signal()
    on_settings = Signal()
    on_exit = Signal()

    content: QWidget
    shade = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._layout()

    def _layout(self):
        self._inner = _FrameInner(parent=self)
        self._buttons = _WindowButtons(parent=self)
        self._buttons.on_minimize.connect(self.on_minimize)
        self._buttons.on_minimize.connect(self.handle_shade)
        self._buttons.on_settings.connect(self.on_settings)
        self._buttons.on_exit.connect(self.on_exit)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        layout.addWidget(self._inner)
        self._buttons.show()

    def resizeEvent(self, evt: QResizeEvent):
        buttons_size = self._buttons.sizeHint()
        self._buttons.setGeometry(
            evt.size().width() - buttons_size.width(),
            0,
            buttons_size.width(),
            buttons_size.height(),
        )

    def set_content(self, content: QWidget):
        self._inner.set_content(content)
        self.content = content

    def handle_shade(self):
        self.set_shade(not self.shade)

    def set_shade(self, shade: bool):
        if shade == self.shade:
            return

        self.shade = shade

        if self.shade:
            self.previous_window_geom = self.window().size()
            self.previous_window_min_size = self.window().minimumSize()
            top_right = self.window().geometry().topRight()
            self._inner.hide()
            self.window().setMinimumSize(self._buttons.sizeHint())

            size = self._buttons.sizeHint()
            self.window().resize(size)

            new_top_left = QPoint(top_right)
            new_top_left.setX(top_right.x() - size.width())
            self.window().move(new_top_left)
        else:
            pos = self.window().geometry().topRight()
            self._inner.show()
            if hasattr(self, "previous_window_geom"):
                self.window().setMinimumSize(self.previous_window_min_size)
                geom = self.previous_window_geom
            else:
                geom = self.window().sizeHint()

            pos.setX(pos.x() - geom.width())
            self.window().resize(geom)
            self.window().move(pos)


class _FrameInner(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._layout()
        # TODO: Set background

    def _layout(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        top_row = QHBoxLayout()
        layout.addLayout(top_row)
        top_row.setContentsMargins(0, 0, 0, 0)
        top_row.setSpacing(0)
        top_row.addWidget(self.build_image("borderTL", Qt.Edge.TopEdge | Qt.Edge.LeftEdge))
        top_row.addWidget(self.build_image("borderT", Qt.Edge.TopEdge, h_fix=False))
        top_row.addWidget(self.build_image("borderTR", Qt.Edge.TopEdge | Qt.Edge.RightEdge))

        mid_row = QHBoxLayout()
        layout.addLayout(mid_row)
        mid_row.setContentsMargins(0, 0, 0, 0)
        mid_row.setSpacing(0)
        mid_row.addWidget(self.build_image("borderL", Qt.Edge.LeftEdge, v_fix=False))
        self.content = QWidget(self)
        mid_row.addWidget(self.content, 1)
        mid_row.addWidget(self.build_image("borderR", Qt.Edge.RightEdge, v_fix=False))

        bot_row = QHBoxLayout()
        layout.addLayout(bot_row)
        bot_row.setContentsMargins(0, 0, 0, 0)
        bot_row.setSpacing(0)
        bot_row.addWidget(
            self.build_image(
                "borderBL",
                Qt.Edge.BottomEdge | Qt.Edge.LeftEdge,
            )
        )
        bot_row.addWidget(self.build_image("borderB", Qt.Edge.BottomEdge, h_fix=False))
        bot_row.addWidget(self.build_image("borderBR", Qt.Edge.BottomEdge | Qt.Edge.RightEdge))

    def build_image(self, name: str, edge=None, h_fix=True, v_fix=True):
        pixmap = QPixmap(SKIN + name)
        label = _ResizeHandle(edge, parent=self)
        label.setSizePolicy(
            QSizePolicy.Policy.Fixed if h_fix else QSizePolicy.Policy.Preferred,
            QSizePolicy.Policy.Fixed if v_fix else QSizePolicy.Policy.Preferred,
        )
        label.setScaledContents(True)
        label.setPixmap(pixmap)
        return label

    def set_content(self, content: QWidget):
        self.layout().replaceWidget(self.content, content)
        self.content = content


class _WindowButtons(QWidget):
    on_minimize = Signal()
    on_settings = Signal()
    on_exit = Signal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._layout()

    def _layout(self):
        layout = QHBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addStretch(1)

        drag_area = _DragHandle(self)
        layout.addWidget(drag_area, alignment=Qt.AlignmentFlag.AlignTop)

        minimize_button = QPushButton(self)
        minimize_button.clicked.connect(self.on_minimize)
        minimize_button.setStyleSheet(
            self.button_style("minimize.png", "minimizeHover.png")
        )
        layout.addWidget(minimize_button, alignment=Qt.AlignmentFlag.AlignTop)

        # settings_button = QPushButton(self)
        # settings_button.clicked.connect(self.on_settings)
        # settings_button.setStyleSheet(
        #     self.button_style("settings.png", "settingsHover.png")
        # )
        # layout.addWidget(settings_button, alignment=Qt.AlignmentFlag.AlignTop)

        exit_button = QPushButton(self)
        exit_button.clicked.connect(self.on_exit)
        exit_button.setStyleSheet(self.button_style("exit.png", "exitHover.png"))
        layout.addWidget(exit_button, alignment=Qt.AlignmentFlag.AlignTop)

    def button_style(self, normal, hover):
        return f"""
        QPushButton {{
            image: url({SKIN}{normal});
            border: none;
            padding: 0;
            margin: 0;
            width: 12px;
            height: 12px;
        }}
        QPushButton::hover {{
            image: url({SKIN}{hover});
        }}
        """


class _DragHandle(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.setPixmap(QPixmap(SKIN + "borderDrag.png"))
        self.setCursor(Qt.CursorShape.OpenHandCursor)

    def mousePressEvent(self, ev):
        self.window().windowHandle().startSystemMove()


class _ResizeHandle(QLabel):
    def __init__(self, edge, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.edge = edge

        if edge == Qt.Edge.TopEdge & Qt.Edge.LeftEdge:
            self.setCursor(Qt.CursorShape.SizeFDiagCursor)
        elif edge == Qt.Edge.TopEdge:
            self.setCursor(Qt.CursorShape.SizeVerCursor)
        elif edge == Qt.Edge.TopEdge & Qt.Edge.RightEdge:
            self.setCursor(Qt.CursorShape.SizeBDiagCursor)
        elif edge == Qt.Edge.LeftEdge:
            self.setCursor(Qt.CursorShape.SizeHorCursor)
        elif edge == Qt.Edge.RightEdge:
            self.setCursor(Qt.CursorShape.SizeHorCursor)
        elif edge == Qt.Edge.BottomEdge & Qt.Edge.LeftEdge:
            self.setCursor(Qt.CursorShape.SizeBDiagCursor)
        elif edge == Qt.Edge.BottomEdge:
            self.setCursor(Qt.CursorShape.SizeVerCursor)
        elif edge == Qt.Edge.BottomEdge & Qt.Edge.RightEdge:
            self.setCursor(Qt.CursorShape.SizeFDiagCursor)

    def mousePressEvent(self, ev):
        if self.edge:
            self.window().windowHandle().startSystemResize(self.edge)
