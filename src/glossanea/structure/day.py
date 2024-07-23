# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Day"""

# imports: library
from typing import Any

# imports: project
from glossanea.structure.unit import Unit
from glossanea.files.data import load_data_file, REQUIRED_VERSION_DAY


class Day(Unit):
    """Day"""

    # general variables ---------------------------------------------- #

    _week_number: int = 1
    _day_number: int = 1

    # class methods -------------------------------------------------- #

    @classmethod
    def get_unit_type(cls) -> str:
        """Get unit type"""
        return Unit.TYPE_DAY

    # content variables ---------------------------------------------- #

    _title: str | None = None
    _new_words: list[dict[str, str]] | None = None
    _new_words_extension: list[str] | None = None
    _intro_text: list[str] | None = None
    _sample_sentences: dict[str, Any] | None = None
    _definitions: dict[str, Any] | None = None
    _matching: dict[str, Any] | None = None
    _other_new_words: dict[str, str]| None  = None

    # overridden getters --------------------------------------------- #

    def get_week_no(self) -> int:
        """Get week number"""
        return self._week_number

    def get_unit_no(self) -> int:
        """Get unit number"""
        return self._day_number

    # content getters ------------------------------------------------ #

    def get_title(self) -> str:
        """Get title"""
        return self._title

    def get_new_words(self) -> list[dict[str, str]]:
        """Get new words"""
        return self._new_words

    def get_new_words_extension(self) -> list[str]:
        """Get new words extension"""
        return self._new_words_extension

    def get_intro_text(self) -> list[str]:
        """Get intro text"""
        return self._intro_text

    def get_sample_sentences(self) -> dict[str, Any]:
        """Get sample sentences"""
        return self._sample_sentences

    def get_definitions(self) -> dict[str, Any]:
        """Get definitions"""
        return self._definitions

    def get_matching(self) -> dict[str, Any]:
        """Get matching"""
        return self._matching

    def get_other_new_words(self) -> dict[str, str]:
        """Get other new words"""
        return self._other_new_words

    # init and data load --------------------------------------------- #

    def __init__(self, week_number: int, day_number: int) -> None:

        try:
            Unit.validate_week_number(week_number)
            Unit.validate_day_number(day_number)
        except ValueError as exc:
            raise ValueError from exc

        self._week_number = week_number
        self._day_number = day_number

        self._load()

    def _load(self) -> None:
        """Load"""

        file_path: str = Unit.build_path_day(self._week_number, self._day_number)

        data: dict[str, Any] = load_data_file(file_path)

        if data['version'] != REQUIRED_VERSION_DAY:
            raise ValueError(f'Incorrect data file version: {self._week_number}/{self._day_number}')

        self._title = data['title']
        self._new_words = data['new_words']
        self._new_words_extension = data['new_words_extension']
        self._intro_text = data['intro_text']
        self._sample_sentences = data['sample_sentences']
        self._definitions = data['definitions']
        self._matching = data['matching']
        self._other_new_words = data['other_new_words']

    def __del__(self) -> None:
        pass
