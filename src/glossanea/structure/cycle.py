# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import random

from glossanea.structure.unit import Unit
from glossanea.structure.day import Day
from glossanea.structure.weekly_review import WeeklyReview


class Cycle:

    # next unit ------------------------------------------------------ #

    @classmethod
    def get_next_unit(cls, arg_week_no, arg_unit_no):
        """Create an instance of the next unit"""

        unit_object = None

        next_week_no = arg_week_no
        next_unit_no = (arg_unit_no + 1) % Unit.UNITS_PER_WEEK

        if arg_unit_no == Unit.WEEKLY_REVIEW_INDEX:
            try:
                next_week_no = arg_week_no + 1
                Unit.validate_week_no(next_week_no)
                unit_object = Day(next_week_no, next_unit_no)
            except ValueError:
                raise IndexError('End of units reached!')
        else:

            if next_unit_no == Unit.WEEKLY_REVIEW_INDEX:
                unit_object = WeeklyReview(next_week_no)
            else:
                unit_object = Day(next_week_no, next_unit_no)

        return unit_object

    # random unit ---------------------------------------------------- #

    @classmethod
    def get_random_unit(cls, arg_unit_type):
        """Create an instance of a random unit"""

        week = random.randint(Unit.MIN_WEEK_NO, Unit.MAX_WEEK_NO)
        unit = Unit.MIN_DAY_NO

        if arg_unit_type is None:
            unit = random.randint(Unit.MIN_DAY_NO, Unit.UNITS_PER_WEEK)
            if unit == Unit.UNITS_PER_WEEK:
                unit = Unit.WEEKLY_REVIEW_INDEX
        elif arg_unit_type == Unit.TYPE_DAY:
            unit = random.randint(Unit.MIN_DAY_NO, Unit.MAX_DAY_NO)
        elif arg_unit_type == Unit.TYPE_WEEKLY_REVIEW:
            unit = Unit.WEEKLY_REVIEW_INDEX
        else:
            raise ValueError('Incorrect unit type.')

        if unit == Unit.WEEKLY_REVIEW_INDEX:
            return WeeklyReview(week)
        else:
            return Day(week, unit)

    # day getters ---------------------------------------------------- #

    @classmethod
    def get_first_day_by_week(cls, arg_week_no):
        """Create an instance of the first day in a specific week"""

        return Day(arg_week_no, Unit.MIN_DAY_NO)

    @classmethod
    def get_day_by_number(cls, arg_week_no, arg_day_no):
        """Create an instance of a specific day"""

        return Day(arg_week_no, arg_day_no)

    # weekly review getters ------------------------------------------ #

    @classmethod
    def get_weekly_review_by_week(cls, arg_week_no):
        """Create an instance of the weekly review in a specific week"""

        return WeeklyReview(arg_week_no)
