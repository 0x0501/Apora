# Set system path for external packages
from . import setup  # noqa: F401

from aqt import mw, gui_hooks, QAction
from .src.dialogs.usage import UsageDialog
from .src.dialogs.about import AboutDialog
from .src.dialogs.workshop import WorkshopDialog

ADDON_NAME = "Paradox"


def show_usage():
    dlg = UsageDialog(mw)
    dlg.show()


def show_about():
    dlg = AboutDialog(mw)
    dlg.show()


def show_workshop():
    dlg = WorkshopDialog(mw)
    dlg.show()


def create_paradox_menu(window=None):
    # window param exists to match gui_hooks signature; ignore and use mw
    try:
        # add a top-level menu called "Paradox"
        menu_bar = mw.form.menubar
        # avoid duplicate menu on reload
        for action in menu_bar.actions():
            if action.text() == ADDON_NAME:
                return
        paradox_menu = menu_bar.addMenu(ADDON_NAME)

        if paradox_menu is None:
            raise Exception("Cannot find main menu.")

        act_usage = QAction("Usage", mw)
        act_workshop = QAction("Workshop", mw)
        act_about = QAction("About", mw)

        paradox_menu.addAction(act_usage)
        paradox_menu.addAction(act_workshop)
        paradox_menu.addSeparator()
        paradox_menu.addAction(act_about)

        act_usage.triggered.connect(show_usage)
        act_about.triggered.connect(show_about)
        act_workshop.triggered.connect(show_workshop)
    except Exception:
        # silent fail to avoid breaking Anki UI on load
        pass


# Hook menu creation after main window init (safe on reload)
gui_hooks.main_window_did_init.append(create_paradox_menu)
