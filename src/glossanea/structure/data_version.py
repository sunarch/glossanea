# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Data version"""

# imports: library
import enum
from typing import Any

# imports: project
from glossanea.version import REQUIRED_DATA_VERSION

DATA_KEY: str = 'version'


class ValidationResult(enum.Enum):
    """Data validation """

    OK = enum.auto()

    VERSION_INCORRECT = enum.auto()


def validate(data_dict: dict[str, Any]) -> tuple[ValidationResult, str]:
    """Validate a data version"""

    data_version: int = data_dict[DATA_KEY]

    if data_dict[DATA_KEY] != REQUIRED_DATA_VERSION:
        return (
            ValidationResult.VERSION_INCORRECT,
            'Incorrect data file version: ' +
            f'FOUND "{data_version}", REQUIRED: "{REQUIRED_DATA_VERSION}"'
        )

    return ValidationResult.OK, ""
