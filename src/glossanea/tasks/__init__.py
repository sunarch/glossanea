# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Tasks"""

from glossanea.tasks._common import TaskResult

# Common
from glossanea.tasks.c_1_title import task as title
from glossanea.tasks.c_2_intro_text import task as intro_text

# Day only
from glossanea.tasks.t_1_new_words import task as new_words
from glossanea.tasks.t_2_sample_sentences import task as sample_sentences
from glossanea.tasks.t_3_definitions import task as definitions
from glossanea.tasks.t_4_matching import task as matching
from glossanea.tasks.t_5_other_new_words import task as other_new_words

# Weekly Review only
from glossanea.tasks.wr_01_before_the_test import task as wr_before_the_test
from glossanea.tasks.wr_02_definitions import task as wr_definitions
from glossanea.tasks.wr_03_word_combinations import task as wr_word_combinations
from glossanea.tasks.wr_04_skeletons import task as wr_skeletons
from glossanea.tasks.wr_05_substitution import task as wr_substitution
from glossanea.tasks.wr_06_translation import task as wr_translation
from glossanea.tasks.wr_07_sit_back_and_relax import task as wr_sit_back_and_relax
from glossanea.tasks.wr_08_word_formation import task as wr_word_formation
from glossanea.tasks.wr_09_usage import task as wr_usage
from glossanea.tasks.wr_10_extra_cards import task as wr_extra_cards
