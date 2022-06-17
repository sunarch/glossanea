# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import json


class DataFileLoader:

    VERSION_COUNT = 2
    VERSIONS_DAY = (
        "v1_day",
        "v2_day"
    )
    VERSIONS_WEEKLY_REVIEW = (
        None,
        "v2_weekly_review"
    )

# file loader -------------------------------------------------------- #

    @classmethod
    def load(cls, arg_file_path):
        """Load a data file"""

        file_path = cls.build_full_path(arg_file_path)

        with open(file_path, mode='rt', encoding='utf-8', newline=None) as data_file:
            return json.load(data_file)

    @classmethod
    def build_full_path(cls, arg_file_path):
        """Add data folder prefix to data file path"""

        if not isinstance(arg_file_path, str):
            raise ValueError("The given data file path is not a string!")

        return "../glossanea-data/" + arg_file_path
