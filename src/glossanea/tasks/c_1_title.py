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
from glossanea.tasks._common import TaskResult, validate_unit_data_on_task

DATA_KEY: str = 'title'
DATA_SCHEMA = schema.schema_text_single(DATA_KEY)
DATA_VALIDATOR = Draft202012Validator(DATA_SCHEMA)


@validate_unit_data_on_task(data_validator=DATA_VALIDATOR)
def task(unit_data: dict[str, Any]) -> TaskResult:
    """Display title"""

    text: str = unit_data[DATA_KEY]

    output.empty_line()
    output.center(text)

    user_input.wait_for_enter()

    return TaskResult.FINISHED
