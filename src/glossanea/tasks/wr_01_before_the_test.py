# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Before the test"""

# imports: library
from typing import Any

# imports: dependencies
from jsonschema import Draft202012Validator

# imports: project
from glossanea.cli import output
# from glossanea.cli import user_input
from glossanea.tasks._common import TaskResult, validate_unit_data_on_task

DATA_KEY: str = 'wr_before_the_test'
TITLE: str = 'before the test'.upper()

SCHEMA = {
    "type": "object",
    "required": ["wr_before_the_test"],
    "properties": {
        "wr_before_the_test": {
            "type": "object",
            "properties": {
                "prompt": {"type": "string"},
                "words": {
                    "type": "array",
                    "minItems": 1,
                    "items": {
                        "type": "array",
                        "minItems": 1,
                        "items": {"type": "string"},
                    },
                },
                "after_text": {"type": "string"},
            },
        },
    },
}

DATA_VALIDATOR = Draft202012Validator(SCHEMA)


@validate_unit_data_on_task(data_validator=DATA_VALIDATOR)
def task(unit_data: dict[str, Any]) -> TaskResult:
    """Display before the test section"""

    # skip until data files are complete
    return TaskResult.NOT_IMPLEMENTED

    task_data: dict[str, Any] = unit_data[DATA_KEY]

    output.section_title(f'{TITLE}:')
