from aqt.editor import Editor
from typing import List
from pathlib import Path
from ..utils.config import get_config
import os

icon_path = Path(os.path.dirname(__file__)).parent.joinpath("static", "icon_trans.png")


def on_handle_translation_generate(editor: Editor):
    print("ok")


def on_setup_translation_button(buttons: List[str], editor: Editor):
    name = "Generate Translation"

    config = get_config()

    print("Config:")
    print(config)

    print(icon_path)

    btn = editor.addButton(
        id="editor_trans_button",
        icon=icon_path.as_posix(),
        cmd=name,
        func=on_handle_translation_generate,
        tip="Apora: Generate translation.",
        # keys=config['ipa_shortcut'],
    )

    buttons.append(btn)
