# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Other new words"""

# imports: library
from typing import Any

# imports: project
from glossanea.cli import output

DATA_KEY: str = 'new_words'
DATA_KEY_NEW_WORDS_EXTENSION: str = 'new_words_extension'


def new_words_full(unit_data: dict[str, Any]) -> None:
    """Display new words section"""

    assert DATA_KEY in unit_data

    word_data: list[dict[str, str]] = unit_data[DATA_KEY]

    regular: list[str] = [item['regular'] for item in word_data]
    phonetic: list[str] = [item['phonetic'] for item in word_data]

    output.empty_line()
    output.words_table(regular, phonetic)


def new_words(unit_data: dict[str, Any]) -> None:
    """Display new words section"""

    assert DATA_KEY in unit_data

    word_data: list[dict[str, str]] = unit_data[DATA_KEY]

    regular: list[str] = [item['regular'] for item in word_data]

    output.empty_line()
    output.words_table(regular)
