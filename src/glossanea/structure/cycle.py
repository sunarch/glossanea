# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Cycle"""

# imports: library
import random

# imports: project
from glossanea.structure import unit
from glossanea.structure.unit import Unit


class Cycle:
    """Cycle"""

    # next unit ------------------------------------------------------ #

    @classmethod
    def get_next_unit(cls, week_number: int, unit_number: int) -> Unit:
        """Create an instance of the next unit"""

        next_week_no: int = week_number
        next_unit_no: int = (unit_number + 1) % unit.UNITS_PER_WEEK

        if unit_number == unit.WEEKLY_REVIEW_INDEX:
            next_week_no = week_number + 1

        if next_week_no > unit.MAX_WEEK_NUMBER:
            raise IndexError('End of units reached!')

        return Unit(next_week_no, next_unit_no)

    # random unit ---------------------------------------------------- #

    @classmethod
    def get_random_unit(cls, unit_type: str | None) -> Unit:
        """Create an instance of a random unit"""

        week_number: int = random.randint(unit.MIN_WEEK_NUMBER, unit.MAX_WEEK_NUMBER)
        unit_number: int = unit.MIN_DAY_NUMBER

        if unit_type is None:
            unit_number = random.randint(unit.MIN_DAY_NUMBER, unit.UNITS_PER_WEEK)
            if unit_number == unit.UNITS_PER_WEEK:
                unit_number = unit.WEEKLY_REVIEW_INDEX
        elif unit_type == unit.UnitType.DAY:
            unit_number = random.randint(unit.MIN_DAY_NUMBER, unit.MAX_DAY_NUMBER)
        elif unit_type == unit.UnitType.WEEKLY_REVIEW:
            unit_number = unit.WEEKLY_REVIEW_INDEX
        else:
            raise ValueError('Incorrect unit type.')

        return Unit(week_number, unit_number)

    # day getters ---------------------------------------------------- #

    @classmethod
    def get_first_day_by_week(cls, week_number: int) -> Unit:
        """Create an instance of the first day in a specific week"""

        return Unit(week_number, unit.MIN_DAY_NUMBER)

    @classmethod
    def get_day_by_number(cls, week_number: int, day_number: int) -> Unit:
        """Create an instance of a specific day"""

        return Unit(week_number, day_number)

    # weekly review getters ------------------------------------------ #

    @classmethod
    def get_weekly_review_by_week(cls, week_number: int) -> Unit:
        """Create an instance of the weekly review in a specific week"""

        return Unit(week_number, unit.WEEKLY_REVIEW_INDEX)
