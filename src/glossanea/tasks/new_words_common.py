# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Other new words"""

# imports: project
from glossanea.cli import output

INTRO_TEXT_WIDTH: int = 60


def new_words(data: list[dict[str, str]], display_in_full=True) -> None:
    """Display new words section"""

    regular: list[str] = []
    phonetic: list[str] = []

    for unit in data:
        regular.append(unit['regular'])
        phonetic.append(unit['phonetic'])

    if display_in_full:
        output.section_title('NEW WORDS')
        output.empty_line(1)

    output.empty_line(1)
    output.words_table(regular, phonetic)
