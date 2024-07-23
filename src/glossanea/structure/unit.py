# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Unit"""

# imports: library
import abc
import os.path
from typing import Generator


class Unit(abc.ABC):
    """Unit"""

    # constants ------------------------------------------------------ #

    TYPE_DAY: str = 'day'
    TYPE_WEEKLY_REVIEW: str = 'weekly review'

    MIN_WEEK_NUMBER: int = 1
    MAX_WEEK_NUMBER: int = 12
    UNITS_PER_WEEK = 7
    MIN_DAY_NUMBER: int = 1
    MAX_DAY_NUMBER: int = 6
    WEEKLY_REVIEW_INDEX: int = 0

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
    def get_unit_type(cls) -> str:
        """Get unit type"""
        raise NotImplementedError

# validators --------------------------------------------------------- #

    @classmethod
    def validate_week_number(cls, week_number: int) -> bool:
        """Validate a week number"""

        if not isinstance(week_number, int):
            raise ValueError('Given week number value is not an integer!')

        if week_number < cls.MIN_WEEK_NUMBER or week_number > cls.MAX_WEEK_NUMBER:
            raise ValueError('Wrong week number!')

        return True

    @classmethod
    def validate_day_number(cls, day_number: int) -> bool:
        """Validate a day number"""

        if not isinstance(day_number, int):
            raise ValueError('Given day number value is not an integer!')

        if day_number < cls.MIN_DAY_NUMBER or day_number > cls.MAX_DAY_NUMBER:
            raise ValueError('Wrong day number!')

        return True

# builders ----------------------------------------------------------- #

    @staticmethod
    def build_path_day(week_number: int, day_number: int) -> str:
        """Build path day"""

        file_dir: str = f'week_{week_number:0>2}'
        file_name: str = f'day_{day_number}.json'

        return os.path.join(file_dir, file_name)

    @staticmethod
    def build_path_weekly_review(week_number: int) -> str:
        """Build path weekly review"""

        file_dir: str = f'week_{week_number:0>2}'
        file_name: str = 'weekly_review.json'

        return os.path.join(file_dir, file_name)

# generators --------------------------------------------------------- #

    @classmethod
    def generator_weeks(cls) -> Generator[int, None, None]:
        """Generator weeks"""
        yield from range(cls.MIN_WEEK_NUMBER, cls.MAX_WEEK_NUMBER + 1)

    @classmethod
    def generator_days(cls) -> Generator[int, None, None]:
        """Generator days"""
        yield from range(cls.MIN_DAY_NUMBER, cls.MAX_DAY_NUMBER + 1)

    @classmethod
    def generator_day_tuples(cls) -> Generator[tuple[int, int], None, None]:
        """Generator day tuples"""
        for week in cls.generator_weeks():
            for day in cls.generator_days():
                yield week, day
