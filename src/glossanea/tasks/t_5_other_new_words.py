# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Other new words"""

# imports: library
from typing import Any

# imports: project
from glossanea.cli import output
from glossanea.tasks._common import TaskResult

DATA_KEY: str = 'other_new_words'
TITLE: str = 'other new words'.upper()


def task(unit_data: dict[str, Any]) -> TaskResult:
    """Display other new words section"""

    assert DATA_KEY in unit_data

    task_data: dict[str, str] = unit_data[DATA_KEY]

    output.section_title(f'{TITLE}:')

    output.empty_line()
    output.simple(task_data['prompt'])

    output.empty_line()
    _ = input()

    output.empty_line()

    return TaskResult.FINISHED
