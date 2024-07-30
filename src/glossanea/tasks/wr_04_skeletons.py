# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Skeletons"""

# imports: library
from typing import Any

# imports: dependencies
from jsonschema import Draft202012Validator

# imports: project
from glossanea.structure import schema
from glossanea.tasks import wr_questions_common
from glossanea.tasks._common import TaskResult, validate_unit_data_on_task

DATA_KEY: str = 'wr_skeletons'
DATA_SCHEMA = schema.schema_wr_questions(DATA_KEY)
DATA_VALIDATOR = Draft202012Validator(DATA_SCHEMA)

TITLE: str = 'skeletons'.upper()


@validate_unit_data_on_task(data_validator=DATA_VALIDATOR)
def task(unit_data: dict[str, Any]) -> TaskResult:
    """Display skeletons section"""

    return wr_questions_common.questions(unit_data, DATA_KEY, TITLE)
