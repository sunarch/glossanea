# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from glossanea.structure.unit import Unit
from glossanea.utils.data_file_loader import DataFileLoader


class Day(Unit):

    # general variables ---------------------------------------------- #

    _week_no = 1
    _day_no = 1

    # class methods -------------------------------------------------- #

    @classmethod
    def get_unit_type(cls):
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
        return self._week_no

    def get_unit_no(self):
        return self._day_no

    # content getters ------------------------------------------------ #

    def get_title(self):
        return self._title

    def get_new_words(self):
        return self._new_words

    def get_new_words_extension(self):
        return self._new_words_extension

    def get_intro_text(self):
        return self._intro_text

    def get_sample_sentences(self):
        return self._sample_sentences

    def get_definitions(self):
        return self._definitions

    def get_matching(self):
        return self._matching

    def get_other_new_words(self):
        return self._other_new_words

    # init and data load --------------------------------------------- #

    def __init__(self, arg_week_no, arg_day_no):

        try:
            Unit.validate_week_no(arg_week_no)
            Unit.validate_day_no(arg_day_no)
        except ValueError:
            raise

        self._week_no = arg_week_no
        self._day_no = arg_day_no

        self._load()

    def _load(self):

        file_path = Unit.build_path_day(self._week_no, self._day_no)

        data = DataFileLoader.load(file_path)

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
