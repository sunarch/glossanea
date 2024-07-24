# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Unit"""

# imports: library
import abc
import enum
import os.path

MIN_WEEK_NUMBER: int = 1
MAX_WEEK_NUMBER: int = 12
UNITS_PER_WEEK: int = 7
MIN_DAY_NUMBER: int = 1
MAX_DAY_NUMBER: int = 6
WEEKLY_REVIEW_INDEX: int = 0


class UnitType(enum.Enum):
    """Enum of unit types"""
    DAY = enum.auto()
    WEEKLY_REVIEW = enum.auto()


class Unit(abc.ABC):
    """Unit"""

# abstract content getters ------------------------------------------- #

    @abc.abstractmethod
    def get_week_no(self) -> int:
        """Get week number"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_unit_no(self) -> int:
        """Get unit number"""
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def get_unit_type(cls) -> UnitType:
        """Get unit type"""
        raise NotImplementedError


# validators --------------------------------------------------------- #

def validate_week_number(week_number: int) -> bool:
    """Validate a week number"""

    if not isinstance(week_number, int):
        raise ValueError('Given week number value is not an integer!')

    if week_number < MIN_WEEK_NUMBER or week_number > MAX_WEEK_NUMBER:
        raise ValueError('Wrong week number!')

    return True


def validate_day_number(day_number: int) -> bool:
    """Validate a day number"""

    if not isinstance(day_number, int):
        raise ValueError('Given day number value is not an integer!')

    if day_number < MIN_DAY_NUMBER or day_number > MAX_DAY_NUMBER:
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
