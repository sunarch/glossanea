# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""App"""

# imports: library
import json
import os.path
from typing import Any

# imports: dependencies
from xdg_base_dirs import xdg_config_home

# imports: project
from glossanea import version


config_v1: dict[str, Any] = {}

default: dict[str, Any] = config_v1


def _config_dir_path() -> str:
    """Config dir path"""

    config_dir_path: str = os.path.join(xdg_config_home(), version.PROGRAM_NAME)

    if not os.path.isdir(config_dir_path):
        os.makedirs(config_dir_path, mode=0o740, exist_ok=True)

    return config_dir_path


def _data_folder_path_file_path() -> str:
    """Data folder path file path"""
    return os.path.join(_config_dir_path(), 'data-folder.txt')


def data_dir_path() -> str:
    """Data dir path"""

    data_folder_path_file_path: str = _data_folder_path_file_path()

    try:
        with open(data_folder_path_file_path, 'r', encoding='UTF-8') as fh_data_folder_path_file:
            data_folder_path: str = fh_data_folder_path_file.read().strip()
    except FileNotFoundError:
        data_folder_path: str = ''

    while not os.path.isdir(data_folder_path):
        try:
            data_folder_path: str = input('Please specify the location of the data directory: ')
        except KeyboardInterrupt:
            data_folder_path: str = ''

    with open(data_folder_path_file_path, 'w', encoding='UTF-8') as fh_data_folder_path_file:
        fh_data_folder_path_file.write(data_folder_path)

    return data_folder_path


def check_data_dir_path() -> None:
    """Check data dir path"""
    _ = data_dir_path()


def _config_file_path() -> str:
    """Config file path"""
    return os.path.join(_config_dir_path(), 'config.json')


def config() -> dict[str, Any]:
    """Config"""

    config_file_path: str = _config_file_path()

    try:
        with open(config_file_path, 'r', encoding='UTF-8') as fh_config_file:
            config_dict: dict = json.load(fh_config_file)
    except FileNotFoundError:
        config_dict: dict = default

        with open(config_file_path, 'w', encoding='UTF-8') as fh_config_file:
            json.dump(config_dict, fh_config_file, indent=2)

    return config_dict
