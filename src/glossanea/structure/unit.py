# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Unit"""

import abc
import os.path


class Unit(abc.ABC):
    """Unit"""

    # constants ------------------------------------------------------ #

    TYPE_DAY = 'day'
    TYPE_WEEKLY_REVIEW = 'weekly review'

    MIN_WEEK_NO = 1
    MAX_WEEK_NO = 12
    UNITS_PER_WEEK = 7
    MIN_DAY_NO = 1
    MAX_DAY_NO = 6
    WEEKLY_REVIEW_INDEX = 0

# abstract content getters ------------------------------------------- #

    @abc.abstractmethod
    def get_week_no(self):
        """Get week number"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_unit_no(self):
        """Get unit number"""
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def get_unit_type(cls):
        """Get unit type"""
        raise NotImplementedError

# validators --------------------------------------------------------- #

    @classmethod
    def validate_week_no(cls, arg_week_no):
        """Validate a week number"""

        if not isinstance(arg_week_no, int):
            raise ValueError('Given week number value is not an integer!')

        if arg_week_no < cls.MIN_WEEK_NO or arg_week_no > cls.MAX_WEEK_NO:
            raise ValueError('Wrong week number!')

        return True

    @classmethod
    def validate_day_no(cls, arg_day_no):
        """Validate a day number"""

        if not isinstance(arg_day_no, int):
            raise ValueError('Given day number value is not an integer!')

        if arg_day_no < cls.MIN_DAY_NO or arg_day_no > cls.MAX_DAY_NO:
            raise ValueError('Wrong day number!')

        return True

# builders ----------------------------------------------------------- #

    @staticmethod
    def build_path_day(arg_week_no, arg_day_no):
        """Build path day"""

        file_dir = f'week_{arg_week_no:0>2}'
        file_name = f'day_{arg_day_no}.json'

        return os.path.join(file_dir, file_name)

    @staticmethod
    def build_path_weekly_review(arg_week_no):
        """Build path weekly review"""

        file_dir = f'week_{arg_week_no:0>2}'
        file_name = 'weekly_review.json'

        return os.path.join(file_dir, file_name)

# generators --------------------------------------------------------- #

    @classmethod
    def generator_weeks(cls):
        """Generator weeks"""
        yield from range(cls.MIN_WEEK_NO, cls.MAX_WEEK_NO + 1)

    @classmethod
    def generator_days(cls):
        """Generator days"""
        yield from range(cls.MIN_DAY_NO, cls.MAX_DAY_NO + 1)

    @classmethod
    def generator_day_tuples(cls):
        """Generator day tuples"""
        for week in cls.generator_weeks():
            for day in cls.generator_days():
                yield week, day
