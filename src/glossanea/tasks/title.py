# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Other new words"""

# imports: project
from glossanea.cli import output
from glossanea.cli.user_input import CLIUserInput
from glossanea.tasks._common import TaskResult


def task(text: str) -> TaskResult:
    """Display title"""

    output.empty_line(1)
    output.center(text)

    output.empty_line(1)
    CLIUserInput.wait_for_enter()

    return TaskResult.FINISHED
