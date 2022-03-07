import os

from conf.settings import settings

if __name__ == '__main__':
    from .add_table import flag_to_function

    for dirpath, _, filenames in os.walk(settings.base_dir / "data" / "example"):
        for filename in filenames:
            name = filename.split(".")[0]
            flag_to_function[name](f"{dirpath}/{filename}")
