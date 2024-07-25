# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Other new words"""

# imports: project
from glossanea.cli import output
from glossanea.cli import user_input
from glossanea.tasks._common import TaskResult

TITLE: str = 'other new words'.upper()


def task(data: dict[str, str], *_args, **_kwargs) -> TaskResult:
    """Display other new words section"""

    output.section_title(f'{TITLE}:')

    output.empty_line(1)
    output.simple(data['prompt'])

    output.empty_line(1)
    _, _ = user_input.get_answer('')

    output.empty_line(1)

    return TaskResult.FINISHED
