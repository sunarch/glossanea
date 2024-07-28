# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Data version"""

# imports: library
from typing import Any

# imports: dependencies
from jsonschema import Draft202012Validator

# imports: project
from glossanea.structure import schema
from glossanea.structure.schema import ValidationResult
from glossanea.version import REQUIRED_DATA_VERSION

DATA_KEY: str = 'version'


def validate(unit_data: dict[str, Any]) -> tuple[ValidationResult, str]:
    """Validate a data version"""

    match schema.validate_unit_data(DATA_VALIDATOR, unit_data):
        case ValidationResult.OK, _:
            pass
        case result, reason:
            return result, reason

    data_version: int = unit_data[DATA_KEY]

    if unit_data[DATA_KEY] != REQUIRED_DATA_VERSION:
        return (
            ValidationResult.VERSION_INCORRECT,
            'Incorrect data file version: ' +
            f'FOUND "{data_version}", REQUIRED: "{REQUIRED_DATA_VERSION}"'
        )

    return ValidationResult.OK, ""


SCHEMA = {
    "type": "object",
    "required": ["version", "title"],
    "properties": {
        "version": {
            "type": "integer",
            "minimum": 1,
        },
        "title": {
            "type": "string",
        },
    },
}

DATA_VALIDATOR = Draft202012Validator(SCHEMA)
