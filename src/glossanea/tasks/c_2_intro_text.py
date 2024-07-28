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
from glossanea.cli import user_input
from glossanea.structure import schema
from glossanea.structure.schema import ValidationResult
from glossanea.tasks._common import TaskResult

DATA_KEY: str = 'intro_text'
INTRO_TEXT_WIDTH_FRACTION: float = 0.6

SCHEMA = {
    "type": "object",
    "required": ["intro_text"],
    "properties": {
        "intro_text": schema.subschema_prompt_list(1),
    },
}

DATA_VALIDATOR = Draft202012Validator(SCHEMA)


def task(unit_data: dict[str, Any]) -> TaskResult:
    """Display intro text"""

    match schema.validate_unit_data(DATA_VALIDATOR, unit_data):
        case ValidationResult.OK:
            pass
        case _:
            return TaskResult.DATA_VALIDATION_FAILED

    parts: list[str] = unit_data[DATA_KEY]

    output.empty_line()
    output.framed(parts, INTRO_TEXT_WIDTH_FRACTION)

    user_input.wait_for_enter()

    return TaskResult.FINISHED
