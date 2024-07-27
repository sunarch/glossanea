# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Before the test"""

# imports: library
from typing import Any

# imports: project
from glossanea.cli import output
# from glossanea.cli import user_input
from glossanea.tasks._common import TaskResult

DATA_KEY: str = 'wr_before_the_test'
TITLE: str = 'before the test'.upper()


def task(data: dict[str, Any], *_args, **_kwargs) -> TaskResult:
    """Display before the test section"""

    # skip until data files are complete
    return TaskResult.NOT_IMPLEMENTED

    output.section_title(f'{TITLE}:')
