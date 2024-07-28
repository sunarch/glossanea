# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Usage"""

# imports: library
from typing import Any

# imports: dependencies
from jsonschema import Draft202012Validator

# imports: project
from glossanea.cli import output
# from glossanea.cli import user_input
from glossanea.structure import schema
from glossanea.structure.schema import ValidationResult
from glossanea.tasks._common import TaskResult

DATA_KEY: str = 'wr_usage'
TITLE: str = 'usage'.upper()


def task(unit_data: dict[str, Any]) -> TaskResult:
    """Display usage section"""

    match schema.validate_unit_data(DATA_VALIDATOR, unit_data):
        case ValidationResult.OK:
            pass
        case _:
            return TaskResult.DATA_VALIDATION_FAILED

    # skip until data files are complete
    return TaskResult.NOT_IMPLEMENTED

    task_data: dict[str, Any] = unit_data[DATA_KEY]

    output.section_title(f'{TITLE}:')


SCHEMA = {
    "type": "object",
    "required": ["wr_usage"],
    "properties": {
        "wr_usage": {
            "type": "object",
            "properties": {
                "prompt": {"type": "string"},
                "items": {
                    "type": "array",
                    "minItems": 1,
                    "items": {
                        "type": "object",
                        "properties": {
                            "word": {"type": "string"},
                            "sentences": {
                                "type": "array",
                                "minItems": 1,
                                "items": {"type": "string"},
                            },
                        },
                    },
                },
            },
        },
    },
}

DATA_VALIDATOR = Draft202012Validator(SCHEMA)
