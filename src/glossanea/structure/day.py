# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Day"""

# imports: library
from typing import Any

# imports: project
from glossanea.structure import unit
from glossanea.structure.unit import Unit
from glossanea.files.data import load_data_file, REQUIRED_VERSION_DAY

KEY_DATA_VERSION: str = 'version'
KEY_TITLE: str = 'title'
KEY_NEW_WORDS: str = 'new_words'
KEY_NEW_WORDS_EXTENSION: str = 'new_words_extension'
KEY_INTRO_TEXT: str = 'intro_text'
KEY_SAMPLE_SENTENCES: str = 'sample_sentences'
KEY_DEFINITIONS: str = 'definitions'
KEY_MATCHING: str = 'matching'
KEY_OTHER_NEW_WORDS: str = 'other_new_words'


class Day(Unit):
    """Day"""

    # general variables ---------------------------------------------- #

    _week_number: int = 1
    _day_number: int = 1

    # overridden getters --------------------------------------------- #

    @property
    def week_number(self) -> int:
        """Get week number"""
        return self._week_number

    @property
    def unit_number(self) -> int:
        """Get unit number"""
        return self._day_number

    @property
    def unit_type(self) -> unit.UnitType:
        """Get unit type"""
        return unit.UnitType.DAY

    # content getters ------------------------------------------------ #

    @property
    def data_version(self) -> str:
        """Get data version"""
        return self._data[KEY_DATA_VERSION]

    @property
    def title(self) -> str:
        """Get title"""
        return self._data[KEY_TITLE]

    @property
    def new_words(self) -> list[dict[str, str]]:
        """Get new words"""
        return self._data[KEY_NEW_WORDS]

    @property
    def new_words_extension(self) -> list[str]:
        """Get new words extension"""
        return self._data[KEY_NEW_WORDS_EXTENSION]

    @property
    def intro_text(self) -> list[str]:
        """Get intro text"""
        return self._data[KEY_INTRO_TEXT]

    @property
    def sample_sentences(self) -> dict[str, Any]:
        """Get sample sentences"""
        return self._data[KEY_SAMPLE_SENTENCES]

    @property
    def definitions(self) -> dict[str, Any]:
        """Get definitions"""
        return self._data[KEY_DEFINITIONS]

    @property
    def matching(self) -> dict[str, Any]:
        """Get matching"""
        return self._data[KEY_MATCHING]

    @property
    def other_new_words(self) -> dict[str, str]:
        """Get other new words"""
        return self._data[KEY_OTHER_NEW_WORDS]

    # init and data load --------------------------------------------- #

    def __init__(self, week_number: int, day_number: int) -> None:

        try:
            unit.validate_week_number(week_number)
            unit.validate_day_number(day_number)
        except ValueError as exc:
            raise ValueError from exc

        self._week_number = week_number
        self._day_number = day_number

        file_path: str = unit.build_path_day(self._week_number, self._day_number)

        self._data: dict[str, Any] = load_data_file(file_path)

        if self.data_version != REQUIRED_VERSION_DAY:
            raise ValueError(f'Incorrect data file version: {self._week_number}/{self._day_number}')
