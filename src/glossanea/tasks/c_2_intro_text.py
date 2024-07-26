# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Other new words"""

# imports: project
from glossanea.cli import output
from glossanea.cli import user_input
from glossanea.tasks._common import TaskResult

INTRO_TEXT_WIDTH: int = 60


def task(parts: list[str], *_args, **_kwargs) -> TaskResult:
    """Display intro text"""

    output.empty_line(1)
    output.framed(parts, INTRO_TEXT_WIDTH)

    user_input.wait_for_enter()

    return TaskResult.FINISHED
