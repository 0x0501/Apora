from aqt import mw
from aqt.qt import (
    Qt,
    QDialog,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QPixmap
)
import os
from pathlib import Path

icon_path = Path(os.path.dirname(__file__)).parent.joinpath("static", "icon_apora.png")

class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent or mw)
        self.setWindowTitle("Apora — About")
        self.setMinimumWidth(400)
        layout = QVBoxLayout()
        title = QLabel("<b>Apora - Anki integration</b>")
        title.setTextFormat(Qt.TextFormat.RichText)
        layout.addWidget(title)
        
        image_label = QLabel(self)
          
        icon = QPixmap(icon_path.as_posix())
        scaled_pixmap = icon.scaled(100, 100, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio)
        image_label.setPixmap(scaled_pixmap)
        
        layout.addWidget(image_label)

        purpose = QLabel(
            'Apora provide tools out of box that can boost your learning experience, for more visit: <a href="https://apora.sumku.cc" style="color: #1e88e5; text-decoration: none;">https://apora.sumku.cc</a>'
        )
        purpose.setOpenExternalLinks(True)
        purpose.setWordWrap(True)
        layout.addWidget(purpose)

        btns = QHBoxLayout()
        close = QPushButton("Close")
        btns.addStretch(1)
        btns.addWidget(close)
        layout.addLayout(btns)

        close.clicked.connect(self.accept)
        self.setLayout(layout)
