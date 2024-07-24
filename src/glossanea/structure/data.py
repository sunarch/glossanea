# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""App"""

# imports: library
import json
import os.path
from typing import Any

# imports: project
from glossanea.structure import config


REQUIRED_VERSION: int = 2


def data_file_path(file_subpath: str) -> str:
    """Add data folder prefix to data file path"""

    if not isinstance(file_subpath, str):
        raise ValueError('The given data file path is not a string!')

    return os.path.join(config.data_dir_path(), file_subpath)


def load_json_file(file_subpath: str) -> dict[str, Any]:
    """Load a data file"""

    full_path: str = data_file_path(file_subpath)

    with open(full_path, mode='r', encoding='UTF-8', newline=None) as fh:
        return json.load(fh)


def load_text_file_lines(file_subpath: str) -> list[str]:
    """Load a data file"""

    full_path: str = data_file_path(file_subpath)

    with open(full_path, 'r', encoding='UTF-8') as fh:
        return fh.readlines()
