# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Tasks"""

from glossanea.tasks._common import TaskResult

from glossanea.tasks.title import task as title
from glossanea.tasks.intro_text import task as intro_text

from glossanea.tasks.new_words import task as new_words
from glossanea.tasks.sample_sentences import task as sample_sentences
from glossanea.tasks.definitions import task as definitions
from glossanea.tasks.matching import task as matching
from glossanea.tasks.other_new_words import task as other_new_words
