# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Word combinations"""

# imports: library
from typing import Any

# imports: dependencies
from jsonschema import Draft202012Validator

# imports: project
from glossanea.cli import output
# from glossanea.cli import user_input
from glossanea.tasks._common import TaskResult, validate_unit_data_on_task

DATA_KEY: str = 'wr_word_combinations'
TITLE: str = 'word combinations'.upper()

SCHEMA = {
    "type": "object",
    "required": [DATA_KEY],
    "properties": {
        DATA_KEY: {
            "type": "object",
            "properties": {
                "task_number": {"type": "integer"},
                "prompt": {"type": "string"},
                "scoring": {"type": "string"},
                "extra_words": {
                    "type": "array",
                    "minItems": 1,
                    "items": {"type": "string"},
                },
                "items": {
                    "type": "array",
                    "minItems": 1,
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "string"},
                            "answer_before": {"type": "string"},
                            "accept_before": {
                                "type": "array",
                                "minItems": 0,
                                "items": {"type": "string"},
                            },
                            "word": {"type": "string"},
                            "answer_after": {"type": "string"},
                            "accept_after": {
                                "type": "array",
                                "minItems": 0,
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


@validate_unit_data_on_task(data_validator=DATA_VALIDATOR)
def task(unit_data: dict[str, Any]) -> TaskResult:
    """Display word combinations section"""

    # skip until data files are complete
    return TaskResult.NOT_IMPLEMENTED

    task_data: dict[str, Any] = unit_data[DATA_KEY]

    output.section_title(f'{TITLE}:')
