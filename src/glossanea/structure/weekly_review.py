# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Weekly Review"""

# imports: library
from typing import Any

# imports: project
from glossanea.structure import unit
from glossanea.structure.unit import Unit
from glossanea.files.data import load_data_file, REQUIRED_VERSION_WEEKLY_REVIEW


class WeeklyReview(Unit):
    """Weekly Review"""

    # general variables ---------------------------------------------- #

    _week_number: int = 1

    # content variables ---------------------------------------------- #

    _data = None

    # overridden getters --------------------------------------------- #

    @property
    def week_number(self) -> int:
        """Get week number"""
        return self._week_number

    @property
    def unit_number(self) -> int:
        """Get unit number"""
        return unit.WEEKLY_REVIEW_INDEX

    @property
    def unit_type(self) -> unit.UnitType:
        """Get unit type"""
        return unit.UnitType.WEEKLY_REVIEW

    # content getters ------------------------------------------------ #

    def get_data(self) -> dict[str, Any]:
        """Get data"""
        # pylint: disable=unnecessary-pass
        pass

    # init and data load --------------------------------------------- #

    def __init__(self, week_number: int) -> None:

        try:
            unit.validate_week_number(week_number)
        except ValueError as exc:
            raise ValueError from exc

        self._week_number = week_number

        self._load()

    def _load(self) -> None:
        """Load"""

        file_path: str = unit.build_path_weekly_review(self._week_number)

        self._data = load_data_file(file_path)

        if self._data['version'] != REQUIRED_VERSION_WEEKLY_REVIEW:
            raise ValueError(f'Incorrect data file version: {self._week_number}/WR')

    def __del__(self):
        pass
