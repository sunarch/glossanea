# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Day"""

from glossanea.structure.unit import Unit
from glossanea.files.data import load_data_file, REQUIRED_VERSION_DAY


class Day(Unit):
    """Day"""

    # general variables ---------------------------------------------- #

    _week_no = 1
    _day_no = 1

    # class methods -------------------------------------------------- #

    @classmethod
    def get_unit_type(cls):
        """Get unit type"""
        return Unit.TYPE_DAY

    # content variables ---------------------------------------------- #

    _title = None
    _new_words = None
    _new_words_extension = None
    _intro_text = None
    _sample_sentences = None
    _definitions = None
    _matching = None
    _other_new_words = None

    # overridden getters --------------------------------------------- #

    def get_week_no(self):
        """Get week number"""
        return self._week_no

    def get_unit_no(self):
        """Get unit number"""
        return self._day_no

    # content getters ------------------------------------------------ #

    def get_title(self):
        """Get title"""
        return self._title

    def get_new_words(self):
        """Get new words"""
        return self._new_words

    def get_new_words_extension(self):
        """Get new words extension"""
        return self._new_words_extension

    def get_intro_text(self):
        """Get intro text"""
        return self._intro_text

    def get_sample_sentences(self):
        """Get sample sentences"""
        return self._sample_sentences

    def get_definitions(self):
        """Get definitions"""
        return self._definitions

    def get_matching(self):
        """Get matching"""
        return self._matching

    def get_other_new_words(self):
        """Get other new words"""
        return self._other_new_words

    # init and data load --------------------------------------------- #

    def __init__(self, arg_week_no, arg_day_no):

        try:
            Unit.validate_week_no(arg_week_no)
            Unit.validate_day_no(arg_day_no)
        except ValueError as exc:
            raise ValueError from exc

        self._week_no = arg_week_no
        self._day_no = arg_day_no

        self._load()

    def _load(self):
        """Load"""

        file_path = Unit.build_path_day(self._week_no, self._day_no)

        data = load_data_file(file_path)

        if data['version'] != REQUIRED_VERSION_DAY:
            raise ValueError(f'Incorrect data file version: {self._week_no}/{self._day_no}')

        self._title = data['title']
        self._new_words = data['new_words']
        self._new_words_extension = data['new_words_extension']
        self._intro_text = data['intro_text']
        self._sample_sentences = data['sample_sentences']
        self._definitions = data['definitions']
        self._matching = data['matching']
        self._other_new_words = data['other_new_words']

    def __del__(self):
        pass
