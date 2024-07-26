# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Other new words"""

# imports: project
from glossanea.cli import output


def new_words(data: list[dict[str, str]]) -> None:
    """Display new words section"""

    regular: list[str] = [item['regular'] for item in data]
    phonetic: list[str] = [item['phonetic'] for item in data]

    output.empty_line()
    output.words_table(regular, phonetic)
