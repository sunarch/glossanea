# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Other new words"""

# imports: library
from typing import Any

# imports: dependencies
from jsonschema import Draft202012Validator

# imports: project
from glossanea.cli import output
from glossanea.structure import schema
from glossanea.structure.schema import ValidationResult
from glossanea.tasks._common import TaskResult

DATA_KEY: str = 'other_new_words'
TITLE: str = 'other new words'.upper()

SCHEMA = {
    "type": "object",
    "required": ["other_new_words"],
    "properties": {
        "other_new_words": {
            "type": "object",
            "properties": {
                "prompt": {"type": "string"},
            },
        },
    },
}

DATA_VALIDATOR = Draft202012Validator(SCHEMA)


def task(unit_data: dict[str, Any]) -> TaskResult:
    """Display other new words section"""

    match schema.validate_unit_data(DATA_VALIDATOR, unit_data):
        case ValidationResult.OK:
            pass
        case _:
            return TaskResult.DATA_VALIDATION_FAILED

    task_data: dict[str, str] = unit_data[DATA_KEY]

    output.section_title(f'{TITLE}:')

    output.empty_line()
    output.simple(task_data['prompt'])

    output.empty_line()
    _ = input()

    output.empty_line()

    return TaskResult.FINISHED
