import os
import sys
from importlib import import_module

dep_dir_name = "lib"
src_dir_name = "src"


def auto_import_modules():
    current_dir = os.path.dirname(__file__)

    for dir_name in ["src", "lib"]:
        dir_path = os.path.join(current_dir, dir_name)
        print(dir_path)
        if os.path.exists(dir_path):
            # 将目录添加到 sys.path
            if dir_path not in sys.path:
                sys.path.insert(0, dir_path)
                sys.path.append(dir_path)

            for file in os.listdir(dir_path):
                if file.endswith(".py") and not file.startswith("__"):
                    module_name = file[:-3]
                    try:
                        import_module(module_name)
                    except ImportError as e:
                        print(f"Failed to import {module_name}: {e}")


auto_import_modules()
