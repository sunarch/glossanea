# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Unit"""

# imports: library
import os.path
from typing import Any

# imports: project
from glossanea import tasks
from glossanea.structure import data
from glossanea.structure import data_version
from glossanea.structure.exceptions import DataError


MIN_WEEK_NUMBER: int = 1
MAX_WEEK_NUMBER: int = 12
UNITS_PER_WEEK: int = 7
MIN_DAY_NUMBER: int = 1
MAX_DAY_NUMBER: int = 6
WEEKLY_REVIEW_INDEX: int = 0

# Day only
KEY_NEW_WORDS_EXTENSION: str = 'new_words_extension'


# pylint: disable=too-many-public-methods
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

    @property
    def unit_number_display(self) -> str:
        """Get display of unit number"""

        if self.is_weekly_review:
            return 'WR'

        return f'{self._unit_number}'

    @property
    def is_weekly_review(self) -> bool:
        """Get whether unit is a Weekly Review"""
        return self._unit_number == WEEKLY_REVIEW_INDEX

    # content getters ------------------------------------------------ #

    @property
    def task_names(self) -> list[str]:
        """Return a list of keys in the data file which describe tasks"""

        key_list: list[str] = list(self._data.keys())
        try:
            key_list.remove(KEY_NEW_WORDS_EXTENSION)
        except ValueError:
            pass

        return key_list

    # Common --------------------------------------------------------- #

    @property
    def title(self) -> str:
        """Get title"""
        return self._data.get(tasks.c_1_title.DATA_KEY)

    @property
    def intro_text(self) -> list[str]:
        """Get intro text"""
        return self._data.get(tasks.c_2_intro_text.DATA_KEY)

    # Day only ------------------------------------------------------- #

    @property
    def new_words(self) -> list[dict[str, str]]:
        """Get new words"""
        return self._data.get(tasks.new_words.DATA_KEY)

    @property
    def new_words_extension(self) -> list[str]:
        """Get new words extension"""
        return self._data.get(KEY_NEW_WORDS_EXTENSION)

    @property
    def sample_sentences(self) -> dict[str, Any]:
        """Get sample sentences"""
        return self._data.get(tasks.t_2_sample_sentences.DATA_KEY)

    @property
    def definitions(self) -> dict[str, Any]:
        """Get definitions"""
        return self._data.get(tasks.t_3_definitions.DATA_KEY)

    @property
    def matching(self) -> dict[str, Any]:
        """Get matching"""
        return self._data.get(tasks.t_4_matching.DATA_KEY)

    @property
    def other_new_words(self) -> dict[str, str]:
        """Get other new words"""
        return self._data.get(tasks.t_5_other_new_words.DATA_KEY)

    # Weekly Review only --------------------------------------------- #

    @property
    def wr_before_the_test(self) -> dict[str, Any]:
        """Get before the test"""
        return self._data.get(tasks.wr_01_before_the_test.DATA_KEY)

    @property
    def wr_definitions(self) -> dict[str, Any]:
        """Get WR definitions"""
        return self._data.get(tasks.wr_02_definitions.DATA_KEY)

    @property
    def wr_word_combinations(self) -> dict[str, Any]:
        """Get WR word combinations"""
        return self._data.get(tasks.wr_03_word_combinations.DATA_KEY)

    @property
    def wr_skeletons(self) -> dict[str, Any]:
        """Get WR skeletons"""
        return self._data.get(tasks.wr_04_skeletons.DATA_KEY)

    @property
    def wr_substitution(self) -> dict[str, Any]:
        """Get WR substitution"""
        return self._data.get(tasks.wr_05_substitution.DATA_KEY)

    @property
    def wr_translation(self) -> dict[str, Any]:
        """Get WR translation"""
        return self._data.get(tasks.wr_06_translation.DATA_KEY)

    @property
    def wr_sit_back_and_relax(self) -> dict[str, Any]:
        """Get WR sit back and relax"""
        return self._data.get(tasks.wr_07_sit_back_and_relax.DATA_KEY)

    @property
    def wr_word_formation(self) -> dict[str, Any]:
        """Get WR word formation"""
        return self._data.get(tasks.wr_08_word_formation.DATA_KEY)

    @property
    def wr_usage(self) -> dict[str, list[str]]:
        """Get WR usage"""
        return self._data.get(tasks.wr_09_usage.DATA_KEY)

    @property
    def wr_extra_cards(self) -> list[str]:
        """Get  WR extra cards"""
        return self._data.get(tasks.wr_10_extra_cards.DATA_KEY)

    # init and data load --------------------------------------------- #

    def __init__(self, week_number: int, unit_number: int) -> None:

        try:
            validate_week_number(week_number)
            validate_unit_number(unit_number)
        except ValueError as exc:
            raise ValueError from exc

        self._week_number = week_number
        self._unit_number = unit_number

        if self.unit_number == WEEKLY_REVIEW_INDEX:
            file_path: str = build_path_weekly_review(self._week_number)
        else:
            file_path: str = build_path_day(self._week_number, self._unit_number)

        self._data: dict[str, Any] = data.load_json_file(file_path)

        match data_version.validate(self._data):
            case data_version.ValidationResult.OK, _:
                del self._data[data_version.DATA_KEY]
            case _, reason:
                msg: str = f'{reason} (Week {self._week_number} / Day {self.unit_number_display})'
                raise DataError(msg)


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
