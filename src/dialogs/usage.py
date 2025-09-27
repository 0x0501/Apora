from aqt import mw
from aqt.qt import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QPushButton,
    QVBoxLayout,
)
from aqt.utils import showInfo
from utils.config import get_config


class UsageDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent or mw)
        self.setWindowTitle("Paradox — Usage")
        self.setMinimumWidth(360)
        cfg = get_config()
        used = cfg.get("tokens_used", 0)
        quota = cfg.get("tokens_quota", 1000)

        layout = QVBoxLayout()
        info = QLabel("Token usage for this account / addon:")
        info.setWordWrap(True)
        layout.addWidget(info)

        progress = QProgressBar()
        progress.setMinimum(0)
        progress.setMaximum(quota)
        progress.setValue(used)
        layout.addWidget(progress)

        stats = QLabel(f"Used: {used} tokens — Quota: {quota} tokens")
        layout.addWidget(stats)

        btns = QHBoxLayout()
        close = QPushButton("Close")
        reset_btn = QPushButton("Reset usage")
        btns.addWidget(reset_btn)
        btns.addStretch(1)
        btns.addWidget(close)
        layout.addLayout(btns)

        reset_btn.clicked.connect(self.reset_usage)
        close.clicked.connect(self.accept)

        self.setLayout(layout)

    def reset_usage(self):
        cfg = get_config()
        cfg["tokens_used"] = 0
        # write_config(cfg)
        showInfo("Token usage reset to 0.")
        self.accept()