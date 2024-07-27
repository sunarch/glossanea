# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Tasks"""

from glossanea.tasks._common import TaskResult

# Common
import glossanea.tasks.c_1_title as title
import glossanea.tasks.c_2_intro_text as intro_text

# Day only
import glossanea.tasks.t_1_new_words as new_words
import glossanea.tasks.t_2_sample_sentences as sample_sentences
import glossanea.tasks.t_3_definitions as definitions
import glossanea.tasks.t_4_matching as matching
import glossanea.tasks.t_5_other_new_words as other_new_words

# Weekly Review only
import glossanea.tasks.wr_01_before_the_test as wr_before_the_test
import glossanea.tasks.wr_02_definitions as wr_definitions
import glossanea.tasks.wr_03_word_combinations as wr_word_combinations
import glossanea.tasks.wr_04_skeletons as wr_skeletons
import glossanea.tasks.wr_05_substitution as wr_substitution
import glossanea.tasks.wr_06_translation as wr_translation
import glossanea.tasks.wr_07_sit_back_and_relax as wr_sit_back_and_relax
import glossanea.tasks.wr_08_word_formation as wr_word_formation
import glossanea.tasks.wr_09_usage as wr_usage
import glossanea.tasks.wr_10_extra_cards as wr_extra_cards
