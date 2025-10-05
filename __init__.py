# Set system path for external packages
from . import setup  # noqa: F401

from aqt import mw, gui_hooks, QAction
from aqt.editor import Editor
from .src.editor import on_setup_ipa_button, on_setup_translation_button
from .src.dialogs.usage import UsageDialog
from .src.dialogs.about import AboutDialog


ADDON_NAME = "Apora"


def show_usage():
    dlg = UsageDialog(mw)
    dlg.show()


def show_about():
    dlg = AboutDialog(mw)
    dlg.show()

def create_apora_menu(window=None):
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

        # act_usage = QAction("Usage", mw)
        # act_workshop = QAction("Workshop", mw)
        act_about = QAction("About", mw)

        # paradox_menu.addAction(act_usage)
        # paradox_menu.addAction(act_workshop)
        paradox_menu.addSeparator()
        paradox_menu.addAction(act_about)

        # act_usage.triggered.connect(show_usage)
        act_about.triggered.connect(show_about)
    except Exception:
        # silent fail to avoid breaking Anki UI on load
        pass


def change_appearance(editor: Editor):
    button_css = """
        #editor_ipa_button {
            min-width: 60px;
        }
        #editor_trans_button {
            min-width: 50px;
        }
    """

    js_insert = f"""
        const styleEl = document.createElement('style');
        styleEl.innerHTML = `{button_css}`;
        document.head.appendChild(styleEl);
        console.log("change_appearance ... js revoke")
    """

    if editor.web is None:
        print("editor.web is none in `change_appearance`")
    else:
        editor.web.eval(js_insert)
    print("change appearance")


# Hook menu creation after main window init (safe on reload)
gui_hooks.main_window_did_init.append(create_apora_menu)
gui_hooks.editor_did_init_buttons.append(on_setup_ipa_button)
gui_hooks.editor_did_init_buttons.append(on_setup_translation_button)
gui_hooks.editor_did_init.append(change_appearance)

