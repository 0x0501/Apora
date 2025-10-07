import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import List, Union

import requests
from anki.collection import Collection
from aqt import mw
from aqt.editor import Editor
from aqt.operations import QueryOp
from aqt.utils import showInfo

from ..utils.config import get_api_base, get_config

icon_path = Path(os.path.dirname(__file__)).parent.joinpath("static", "icon_ipa.png")

config = get_config()


@dataclass
class ResponseType:
    input: str
    output: str
    editor: Editor


def bg_ipa_generate(
    source: str, col: Collection, editor: Editor
) -> Union[ResponseType, None]:
    api_url = f"{get_api_base()}/api/ipa"

    token = config["token"]

    variant = "US" if config["variant"] == "US" else "GB" if config["variant"] else "US"

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    data = {"input": source, "variant": variant}

    print(f"IPA Generate API: {api_url}")
    print(f"Token: {token}")

    # 发送 POST 请求
    response = requests.post(api_url, headers=headers, json=data)

    if response.status_code == 200:
        raw_res = response.json()

        try:
            raw_res_success_status: bool = raw_res["success"]

            raw_res_data_wrapper = raw_res["data"]

            if raw_res_success_status:
                res_type = ResponseType(
                    input=raw_res_data_wrapper["input"],
                    output=raw_res_data_wrapper["output"],
                    editor=editor,
                )
                return res_type
        except KeyError:
            showInfo(f"Invalid key, the original response: {json.dumps(raw_res)}")
            print(f"Invalid key, the original response: {json.dumps(raw_res)}")
            print(raw_res)
            return None
    else:
        showInfo(f"Response error ({response.status_code}): {response.reason}")
        print(f"Response error code: {response.status_code}, reason: {response.reason}")
        return None


def on_bg_success(data: Union[ResponseType, None]) -> None:
    if data is None or data.editor.note is None:
        return

    data.editor.note[config["ipa_target_field_name"]] = data.output
    data.editor.loadNote()  # refresh note

    print(data)


def on_handle_ipa_generate(editor: Editor):
    if editor.note is None:
        showInfo("Error: editor.note is None.")
        print("Error: editor.note is None.")
        return

    try:
        source_ipa_field = editor.note[config["ipa_source_field_name"]]
        target_ipa_field = editor.note[config["ipa_target_field_name"]]
    except KeyError:
        showInfo("IPA Source/Target field didn't match the field name in config.json")
        print("IPA Source/Target field didn't match the field name in config.json")
    else:
        # If no error occurred

        editor.loadNote()  # refresh note

        # remove all the html tags except raw text
        pattern = re.compile(r"<[^>]+>")
        source_purified = pattern.sub("", source_ipa_field)

        editor.note[config["ipa_source_field_name"]] = source_purified
        editor.loadNote()  # refresh note

        print(f"source_ipa_field: {source_ipa_field}")
        print(f"target_ipa_field: {target_ipa_field}")

        op = QueryOp(
            parent=mw,
            op=lambda col: bg_ipa_generate(
                source=source_purified, col=col, editor=editor
            ),
            success=on_bg_success,
        )

        if source_purified != "":
            op.without_collection().run_in_background()
        else:
            print(f"Source IPA field `{config['ipa_source_field_name']}` is empty.")


def on_setup_ipa_button(buttons: List[str], editor: Editor):
    name = "Generate IPA"

    btn = editor.addButton(
        id="editor_ipa_button",
        icon=icon_path.as_posix(),
        cmd=name,
        func=on_handle_ipa_generate,
        tip="Apora: Generate IPA for the word/phrase/sentence",
        # keys=config['ipa_shortcut'],
    )

    buttons.append(btn)
