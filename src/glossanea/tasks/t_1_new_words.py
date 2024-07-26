# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Other new words"""

# imports: project
from glossanea.cli import output
from glossanea.cli import user_input
from glossanea.tasks._common import TaskResult
from glossanea.tasks.t_1_new_words_common import new_words

TITLE: str = 'new words'.upper()


def task(data: list[dict[str, str]], *_args, **_kwargs) -> TaskResult:
    """Display intro text"""

    output.section_title(TITLE)

    new_words(data)

    user_input.wait_for_enter()

    return TaskResult.FINISHED
