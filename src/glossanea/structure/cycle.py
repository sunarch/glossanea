# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Cycle"""

# imports: library
import random

# imports: project
from glossanea.structure.unit import Unit
from glossanea.structure.day import Day
from glossanea.structure.weekly_review import WeeklyReview


class Cycle:
    """Cycle"""

    # next unit ------------------------------------------------------ #

    @classmethod
    def get_next_unit(cls, week_number: int, unit_number: int) -> Unit:
        """Create an instance of the next unit"""

        unit_object = None

        next_week_no: int = week_number
        next_unit_no: int = (unit_number + 1) % Unit.UNITS_PER_WEEK

        if unit_number == Unit.WEEKLY_REVIEW_INDEX:
            try:
                next_week_no = week_number + 1
                Unit.validate_week_number(next_week_no)
                unit_object = Day(next_week_no, next_unit_no)
            except ValueError as exc:
                raise IndexError('End of units reached!') from exc
        else:

            if next_unit_no == Unit.WEEKLY_REVIEW_INDEX:
                unit_object = WeeklyReview(next_week_no)
            else:
                unit_object = Day(next_week_no, next_unit_no)

        return unit_object

    # random unit ---------------------------------------------------- #

    @classmethod
    def get_random_unit(cls, unit_type: str | None) -> Unit:
        """Create an instance of a random unit"""

        week_number: int = random.randint(Unit.MIN_WEEK_NUMBER, Unit.MAX_WEEK_NUMBER)
        unit_number: int = Unit.MIN_DAY_NUMBER

        if unit_type is None:
            unit_number = random.randint(Unit.MIN_DAY_NUMBER, Unit.UNITS_PER_WEEK)
            if unit_number == Unit.UNITS_PER_WEEK:
                unit_number = Unit.WEEKLY_REVIEW_INDEX
        elif unit_type == Unit.TYPE_DAY:
            unit_number = random.randint(Unit.MIN_DAY_NUMBER, Unit.MAX_DAY_NUMBER)
        elif unit_type == Unit.TYPE_WEEKLY_REVIEW:
            unit_number = Unit.WEEKLY_REVIEW_INDEX
        else:
            raise ValueError('Incorrect unit type.')

        # pylint: disable=no-else-return
        if unit_number == Unit.WEEKLY_REVIEW_INDEX:
            return WeeklyReview(week_number)
        else:
            return Day(week_number, unit_number)

    # day getters ---------------------------------------------------- #

    @classmethod
    def get_first_day_by_week(cls, week_number: int) -> Day:
        """Create an instance of the first day in a specific week"""

        return Day(week_number, Unit.MIN_DAY_NUMBER)

    @classmethod
    def get_day_by_number(cls, week_number: int, day_number: int) -> Day:
        """Create an instance of a specific day"""

        return Day(week_number, day_number)

    # weekly review getters ------------------------------------------ #

    @classmethod
    def get_weekly_review_by_week(cls, week_number: int) -> WeeklyReview:
        """Create an instance of the weekly review in a specific week"""

        return WeeklyReview(week_number)
