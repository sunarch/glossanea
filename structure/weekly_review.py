# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from structure.unit import Unit
from utils.data_file_loader import DataFileLoader


class WeeklyReview(Unit):

# general variables -------------------------------------------------- #

    _week_no = 1

# class methods ------------------------------------------------------ #

    @classmethod
    def get_unit_type(self):
        return Unit.TYPE_WEEKLY_REVIEW

# content variables -------------------------------------------------- #

    _data = None

# overridden getters ------------------------------------------------- #

    def get_week_no(self):
        return self._week_no
    
    def get_unit_no(self):
        return Unit.WEEKLY_REVIEW_INDEX

# content getters ---------------------------------------------------- #

    def get_data(self):
        pass

# init and data load ------------------------------------------------- #

    def __init__(self, arg_week_no):

        try:
            Unit.validate_week_no(arg_week_no)
        except ValueError:
            raise

        self._week_no = arg_week_no

        self._load()

    def _load(self):
        
        file_path = Unit.build_path_weekly_review(self._week_no)
        
        data = DataFileLoader.load(file_path)

        self._data = data

    def __del__(self):
        pass

# END ---------------------------------------------------------------- #
