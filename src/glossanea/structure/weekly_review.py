# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Weekly Review"""

from glossanea.structure.unit import Unit
from glossanea.utils.data_file_loader import DataFileLoader


class WeeklyReview(Unit):
    """Weekly Review"""

    # general variables ---------------------------------------------- #

    _week_no = 1

    # class methods -------------------------------------------------- #

    @classmethod
    def get_unit_type(cls):
        """Get unit type"""
        return Unit.TYPE_WEEKLY_REVIEW

    # content variables ---------------------------------------------- #

    _data = None

    # overridden getters --------------------------------------------- #

    def get_week_no(self):
        """Get week number"""
        return self._week_no

    def get_unit_no(self):
        """Get unit number"""
        return Unit.WEEKLY_REVIEW_INDEX

    # content getters ------------------------------------------------ #

    def get_data(self):
        """Get data"""
        # pylint: disable=unnecessary-pass
        pass

    # init and data load --------------------------------------------- #

    def __init__(self, arg_week_no):

        try:
            Unit.validate_week_no(arg_week_no)
        except ValueError as exc:
            raise ValueError from exc

        self._week_no = arg_week_no

        self._load()

    def _load(self):
        """Load"""

        file_path = Unit.build_path_weekly_review(self._week_no)

        data = DataFileLoader.load(file_path)

        self._data = data

    def __del__(self):
        pass
