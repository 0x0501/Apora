from aqt import mw
from aqt.qt import (
    Qt,
    QDialog,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
)


class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent or mw)
        self.setWindowTitle("Paradox — About")
        self.setMinimumWidth(400)
        layout = QVBoxLayout()
        title = QLabel("<b>Paradox</b>")
        title.setTextFormat(Qt.TextFormat.RichText)
        layout.addWidget(title)

        purpose = QLabel(
            "Purpose: Provide tooling around deck options and token-based features."
        )
        purpose.setWordWrap(True)
        layout.addWidget(purpose)

        author = QLabel("Author: Your Name <your.email@example.com>")
        author.setWordWrap(True)
        layout.addWidget(author)

        notes = QLabel(
            "This add-on adds a top-level Paradox menu with Usage, Workshop and About windows."
        )
        notes.setWordWrap(True)
        layout.addWidget(notes)

        btns = QHBoxLayout()
        close = QPushButton("Close")
        btns.addStretch(1)
        btns.addWidget(close)
        layout.addLayout(btns)

        close.clicked.connect(self.accept)
        self.setLayout(layout)
