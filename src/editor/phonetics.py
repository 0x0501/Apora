from aqt.editor import Editor
from typing import List
from pathlib import Path
from ..utils.config import get_config
import os

icon_path = Path(os.path.dirname(__file__)).parent.joinpath("static", "icon_ipa.png")


def on_handle_ipa_generate(editor: Editor):
    print("ok")


def on_setup_ipa_button(buttons: List[str], editor: Editor):
    name = "Generate IPA"

    config = get_config()

    print("Config:")
    print(config)

    print(icon_path)

    btn = editor.addButton(
        id="editor_ipa_button",
        icon=icon_path.as_posix(),
        cmd=name,
        func=on_handle_ipa_generate,
        tip="Apora: Generate IPA for the word/phrase/sentence",
        # keys=config['ipa_shortcut'],
    )

    buttons.append(btn)
