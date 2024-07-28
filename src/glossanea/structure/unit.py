# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Unit"""

# imports: library
import os.path
from typing import Any

# imports: project
from glossanea.structure import data
from glossanea.structure import data_version
from glossanea.structure import schema
from glossanea.structure.exceptions import DataError
from glossanea.tasks.t_1_new_words_common import DATA_KEY_NEW_WORDS_EXTENSION


MIN_WEEK_NUMBER: int = 1
MAX_WEEK_NUMBER: int = 12
UNITS_PER_WEEK: int = 7
MIN_DAY_NUMBER: int = 1
MAX_DAY_NUMBER: int = 6
WEEKLY_REVIEW_INDEX: int = 0


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

        key_list: list[str] = list(self.unit_data.keys())
        try:
            key_list.remove(DATA_KEY_NEW_WORDS_EXTENSION)
        except ValueError:
            pass

        return key_list

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

        self.unit_data: dict[str, Any] = data.load_json_file(file_path)

        schema.validate_unit_data(self.unit_data)

        match data_version.validate(self.unit_data):
            case data_version.ValidationResult.OK, _:
                del self.unit_data[data_version.DATA_KEY]
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
