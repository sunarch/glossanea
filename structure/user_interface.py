# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import abc


class UserInterface(abc.ABC):

    @classmethod
    @abc.abstractmethod
    def start(cls):
        raise NotImplementedError
        
'''
    @classmethod
    @abc.abstractmethod
    def get_event(cls, arg_week_no, arg_lecture_no):
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def process_event(cls, arg_user_input):
        raise NotImplementedError

    # Message displays #

    @classmethod
    @abc.abstractmethod
    def display_warning(cls, arg_text):
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def display_error(cls, arg_text):
        raise NotImplementedError

    # General displays #

    @classmethod
    @abc.abstractmethod
    def display_introduction(cls):
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def display_help(cls):
        raise NotImplementedError

    # Lecture displays #

    @classmethod
    @abc.abstractmethod
    def display_lecture_intro(cls, arg_lecture):
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def display_lecture_title(cls, arg_title):
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def display_lecture_words(cls, arg_words):
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def display_lecture_intro_text(cls, arg_text):
        raise NotImplementedError

    # Task displays #

    @classmethod
    @abc.abstractmethod
    def display_task_1_gaps(cls, arg_lecture):
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def display_task_2_definitions(cls, arg_lecture):
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def display_task_3_matching(cls, arg_lecture):
        raise NotImplementedError
'''

# END ---------------------------------------------------------------- #
