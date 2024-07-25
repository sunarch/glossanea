# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Unit"""

# imports: library
import os.path
from typing import Any

# imports: project
from glossanea.structure import data


MIN_WEEK_NUMBER: int = 1
MAX_WEEK_NUMBER: int = 12
UNITS_PER_WEEK: int = 7
MIN_DAY_NUMBER: int = 1
MAX_DAY_NUMBER: int = 6
WEEKLY_REVIEW_INDEX: int = 0

KEY_DATA_VERSION: str = 'version'

KEY_TITLE: str = 'title'
KEY_INTRO_TEXT: str = 'intro_text'

KEY_NEW_WORDS: str = 'new_words'
KEY_NEW_WORDS_EXTENSION: str = 'new_words_extension'
KEY_SAMPLE_SENTENCES: str = 'sample_sentences'
KEY_DEFINITIONS: str = 'definitions'
KEY_MATCHING: str = 'matching'
KEY_OTHER_NEW_WORDS: str = 'other_new_words'

KEY_WR_BEFORE_THE_TEST: str = 'wr_before_the_test'
KEY_WR_DEFINITIONS: str = 'wr_definitions'
KEY_WR_WORD_COMBINATIONS: str = 'wr_make_typical_word_combinations'
KEY_WR_SKELETONS: str = 'wr_skeletons'
KEY_WR_SUBSTITUTION: str = 'wr_substitution'
KEY_WR_TRANSLATION: str = 'wr_translation'
KEY_WR_SIT_BACK_AND_RELAX: str = 'wr_now_sit_back_and_relax'
KEY_WR_WORD_FORMATION: str = 'wr_word_formation'
KEY_WR_USAGE: str = 'wr_usage'
KEY_WR_EXTRA_CARDS: str = 'wr_fill_in_the_extra_cards'


class Unit:
    """Unit"""

    # general getters ------------------------------------------------ #

    @property
    def week_number(self) -> int:
        """Get week number"""
        return self._week_number

    @property
    def unit_number(self) -> int:
        """Get unit number"""
        return self._unit_number

    # content getters ------------------------------------------------ #

    @property
    def data_keys(self) -> list[str]:
        """Iterate through the keys in the data file"""

        return list(self._data.keys())

    @property
    def data_version(self) -> str:
        """Get data version"""
        return self._data[KEY_DATA_VERSION]

    # Common --------------------------------------------------------- #

    @property
    def title(self) -> str:
        """Get title"""
        return self._data[KEY_TITLE]

    @property
    def intro_text(self) -> list[str]:
        """Get intro text"""
        return self._data[KEY_INTRO_TEXT]

    # Day only ------------------------------------------------------- #

    @property
    def new_words(self) -> list[dict[str, str]]:
        """Get new words"""
        return self._data[KEY_NEW_WORDS]

    @property
    def new_words_extension(self) -> list[str]:
        """Get new words extension"""
        return self._data[KEY_NEW_WORDS_EXTENSION]

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

    # Weekly Review only --------------------------------------------- #

    @property
    def wr_before_the_test(self) -> dict[str, Any]:
        """Get before the test"""
        return self._data[KEY_WR_BEFORE_THE_TEST]

    @property
    def wr_definitions(self) -> dict[str, Any]:
        """Get WR definitions"""
        return self._data[KEY_WR_DEFINITIONS]

    @property
    def wr_word_combinations(self) -> dict[str, Any]:
        """Get WR word combinations"""
        return self._data[KEY_WR_WORD_COMBINATIONS]

    @property
    def wr_skeletons(self) -> dict[str, Any]:
        """Get WR skeletons"""
        return self._data[KEY_WR_SKELETONS]

    @property
    def wr_substitution(self) -> dict[str, Any]:
        """Get WR substitution"""
        return self._data[KEY_WR_SUBSTITUTION]

    @property
    def wr_translation(self) -> dict[str, Any]:
        """Get WR translation"""
        return self._data[KEY_WR_TRANSLATION]

    @property
    def wr_sit_back_and_relax(self) -> dict[str, Any]:
        """Get WR sit back and relax"""
        return self._data[KEY_WR_SIT_BACK_AND_RELAX]

    @property
    def wr_word_formation(self) -> dict[str, Any]:
        """Get WR word formation"""
        return self._data[KEY_WR_WORD_FORMATION]

    @property
    def wr_usage(self) -> dict[str, list[str]]:
        """Get WR usage"""
        return self._data[KEY_WR_USAGE]

    @property
    def wr_extra_cards(self) -> list[str]:
        """Get  WR extra cards"""
        return self._data[KEY_WR_EXTRA_CARDS]

    # init and data load --------------------------------------------- #

    def __init__(self, week_number: int, unit_number: int) -> None:

        try:
            validate_week_number(week_number)
            validate_unit_number(unit_number)
        except ValueError as exc:
            raise ValueError from exc

        self._week_number = week_number
        self._unit_number = unit_number

        if unit_number == WEEKLY_REVIEW_INDEX:
            unit_number_display: str = 'WR'
            file_path: str = build_path_weekly_review(self._week_number)
        else:
            unit_number_display: str = f'{unit_number}'
            file_path: str = build_path_day(self._week_number, self._unit_number)

        self._data: dict[str, Any] = data.load_json_file(file_path)

        if self.data_version != data.REQUIRED_VERSION:
            msg: str = f'Incorrect data file version: {self._week_number}/{unit_number_display}'
            raise ValueError(msg)


# validators --------------------------------------------------------- #

def validate_week_number(week_number: int) -> bool:
    """Validate a week number"""

    if not isinstance(week_number, int):
        raise ValueError('Given week number value is not an integer!')

    if week_number < MIN_WEEK_NUMBER or week_number > MAX_WEEK_NUMBER:
        raise ValueError('Wrong week number!')

    return True


def validate_unit_number(unit_number: int) -> bool:
    """Validate a day number"""

    if not isinstance(unit_number, int):
        raise ValueError('Given day number value is not an integer!')

    if unit_number == WEEKLY_REVIEW_INDEX:
        return True

    if unit_number < MIN_DAY_NUMBER or unit_number > MAX_DAY_NUMBER:
        raise ValueError('Wrong day number!')

    return True


# builders ----------------------------------------------------------- #

def build_path_day(week_number: int, day_number: int) -> str:
    """Build path day"""

    file_dir: str = f'week_{week_number:0>2}'
    file_name: str = f'day_{day_number}.json'

    return os.path.join(file_dir, file_name)


def build_path_weekly_review(week_number: int) -> str:
    """Build path weekly review"""

    file_dir: str = f'week_{week_number:0>2}'
    file_name: str = 'weekly_review.json'

    return os.path.join(file_dir, file_name)
