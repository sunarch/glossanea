# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""App"""

# imports: library
import json
import os.path

# imports: project
from glossanea.files.config import data_dir_path


REQUIRED_VERSION_DAY: str = 'v2_day'
REQUIRED_VERSION_WEEKLY_REVIEW = 'v2_weekly_review'


def data_file_path(file_subpath: str):
    """Add data folder prefix to data file path"""

    if not isinstance(file_subpath, str):
        raise ValueError('The given data file path is not a string!')

    return os.path.join(data_dir_path(), file_subpath)


def load_data_file(file_subpath: str):
    """Load a data file"""

    full_path: str = data_file_path(file_subpath)

    with open(full_path, mode='r', encoding='UTF-8', newline=None) as data_file:
        return json.load(data_file)
