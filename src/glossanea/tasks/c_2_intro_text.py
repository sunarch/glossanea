# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Other new words"""

# imports: project
from glossanea.cli import output
from glossanea.cli import user_input
from glossanea.tasks._common import TaskResult

DATA_KEY: str = 'intro_text'
INTRO_TEXT_WIDTH_FRACTION: float = 0.6


def task(parts: list[str], *_args, **_kwargs) -> TaskResult:
    """Display intro text"""

    output.empty_line()
    output.framed(parts, INTRO_TEXT_WIDTH_FRACTION)

    user_input.wait_for_enter()

    return TaskResult.FINISHED
