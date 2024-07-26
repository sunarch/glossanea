# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Other new words"""

# imports: project
from glossanea.cli import output


def new_words(data: list[dict[str, str]]) -> None:
    """Display new words section"""

    regular: list[str] = []
    phonetic: list[str] = []

    for unit in data:
        regular.append(unit['regular'])
        phonetic.append(unit['phonetic'])

    output.empty_line(1)
    output.words_table(regular, phonetic)
