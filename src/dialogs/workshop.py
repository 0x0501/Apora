from aqt import mw
from aqt.qt import (
    Qt,
    QDialog,
    QHBoxLayout,
    QListWidget,
    QVBoxLayout,
    QPushButton,
    QCheckBox,
    QSpinBox,
    QFormLayout,
    QLineEdit,
)
from aqt.utils import showInfo
from utils.config import get_config


class WorkshopDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent or mw)
        self.setWindowTitle("Paradox — Workshop")
        self.setMinimumWidth(520)
        self.cfg = get_config()

        main = QHBoxLayout()
        # Left: deck list
        self.deck_list = QListWidget()
        self.deck_list.setMinimumWidth(220)
        main.addWidget(self.deck_list)

        # Right: deck options
        right = QVBoxLayout()
        form = QFormLayout()

        self.enable_checkbox = QCheckBox("Enable Paradox for this deck")
        form.addRow(self.enable_checkbox)

        self.token_limit_spin = QSpinBox()
        self.token_limit_spin.setRange(0, 1000000)
        form.addRow("Token limit for deck:", self.token_limit_spin)

        self.notes_edit = QLineEdit()
        form.addRow("Notes / tag:", self.notes_edit)

        right.addLayout(form)

        btns = QHBoxLayout()
        save = QPushButton("Save")
        close = QPushButton("Close")
        btns.addStretch(1)
        btns.addWidget(save)
        btns.addWidget(close)
        right.addLayout(btns)

        main.addLayout(right)
        self.setLayout(main)

        self.decks_map = {}  # id->name
        # self.populate_decks()
        self.deck_list.currentItemChanged.connect(self.on_deck_select)
        save.clicked.connect(self.save_settings)
        close.clicked.connect(self.accept)

    # def populate_decks(self):
    #     # Anki API: decks list
    #     try:
    #         if mw.col is None:
    #             raise Exception("Cannot get collections.")

    #         decks = mw.col.decks
    #         # all_names returns dict id->name in many versions
    #         for name in decks:
    #             item = QListWidgetItem(name)
    #             item.setData(Qt.ItemDataRole.UserRole, str(did))
    #             self.deck_list.addItem(item)
    #             self.decks_map[str(did)] = name
    #     except Exception:
    #         # fallback: use deck tree
    #         try:
    #             names = mw.col.decks.top_level()
    #             for name in names:
    #                 item = QListWidgetItem(name)
    #                 item.setData(Qt.ItemDataRole.UserRole, name)
    #                 self.deck_list.addItem(item)
    #                 self.decks_map[name] = name
    #         except Exception:
    #             # no decks found
    #             pass

    def on_deck_select(self, current, previous=None):
        if not current:
            return
        did = current.data(Qt.ItemDataRole.UserRole)
        deck_cfg = self.cfg.get("decks", {}).get(did, {})
        self.enable_checkbox.setChecked(deck_cfg.get("enabled", False))
        self.token_limit_spin.setValue(deck_cfg.get("token_limit", 0))
        self.notes_edit.setText(deck_cfg.get("notes", ""))

    def save_settings(self):
        item = self.deck_list.currentItem()
        if not item:
            showInfo("Please select a deck first.")
            return
        did = item.data(Qt.ItemDataRole.UserRole)
        if "decks" not in self.cfg:
            self.cfg["decks"] = {}
        self.cfg["decks"][did] = {
            "enabled": bool(self.enable_checkbox.isChecked()),
            "token_limit": int(self.token_limit_spin.value()),
            "notes": str(self.notes_edit.text()),
        }
        # write_config(self.cfg)
        showInfo(f"Saved settings for deck: {self.decks_map.get(str(did), did)}")
