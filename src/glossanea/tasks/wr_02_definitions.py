# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Definitions (WR)"""

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

DATA_KEY: str = 'wr_definitions'
TITLE: str = 'definitions'.upper()


def task(unit_data: dict[str, Any]) -> TaskResult:
    """Display definitions (WR) section"""

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
    "required": ["wr_definitions"],
    "properties": {
        "wr_definitions": schema.subschema_items_task(),
    },
}

DATA_VALIDATOR = Draft202012Validator(SCHEMA)
