# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Other new words"""

# imports: library
from typing import Any

# imports: project
from glossanea.cli import output
from glossanea.cli import user_input
from glossanea.tasks._common import TaskResult
from glossanea.tasks import t_1_new_words_common as new_words

TITLE: str = 'new words'.upper()


def task(unit_data: dict[str, Any]) -> TaskResult:
    """Display intro text"""

    output.section_title(TITLE)

    new_words.new_words_full(unit_data)

    user_input.wait_for_enter()

    return TaskResult.FINISHED
