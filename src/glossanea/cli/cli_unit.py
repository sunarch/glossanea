# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""CLI Unit"""

# imports: project
from glossanea import tasks
from glossanea.tasks import TaskResult
from glossanea.cli import output
from glossanea.structure import unit
from glossanea.structure.unit import Unit


def run(unit_obj: Unit) -> None:
    """Run Unit"""

    task_list: list[str] = unit_obj.data_keys
    task_index: int = 0
    while True:

        if task_index < 0:
            raise IndexError(f'Step index out of bounds: {task_index}')

        if task_index >= len(task_list):
            break

        match task_list[task_index]:
            case unit.KEY_DATA_VERSION:
                task_result = TaskResult.HIDDEN

            # Common
            case unit.KEY_TITLE:
                task_result = tasks.title(unit_obj.title)
            case unit.KEY_INTRO_TEXT:
                task_result = tasks.intro_text(unit_obj.intro_text)

            # Day only
            case unit.KEY_NEW_WORDS:
                task_result = tasks.new_words(unit_obj.new_words)
            case unit.KEY_NEW_WORDS_EXTENSION:
                task_result = TaskResult.HIDDEN
            case unit.KEY_SAMPLE_SENTENCES:
                task_result = tasks.sample_sentences(unit_obj.sample_sentences,
                                                     unit_obj.new_words_extension,
                                                     unit_obj.new_words)
            case unit.KEY_DEFINITIONS:
                task_result = tasks.definitions(unit_obj.definitions,
                                                unit_obj.new_words)
            case unit.KEY_MATCHING:
                task_result = tasks.matching(unit_obj.matching,
                                             unit_obj.new_words)
            case unit.KEY_OTHER_NEW_WORDS:
                task_result = tasks.other_new_words(unit_obj.other_new_words)

            # Weekly Review only
            case unit.KEY_WR_BEFORE_THE_TEST:
                task_result = tasks.wr_before_the_test(unit_obj.wr_before_the_test)
            case unit.KEY_WR_DEFINITIONS:
                task_result = tasks.wr_definitions(unit_obj.wr_definitions)
            case unit.KEY_WR_WORD_COMBINATIONS:
                task_result = tasks.wr_word_combinations(unit_obj.wr_word_combinations)
            case unit.KEY_WR_SKELETONS:
                task_result = tasks.wr_skeletons(unit_obj.wr_skeletons)
            case unit.KEY_WR_SUBSTITUTION:
                task_result = tasks.wr_substitution(unit_obj.wr_substitution)
            case unit.KEY_WR_TRANSLATION:
                task_result = tasks.wr_translation(unit_obj.wr_translation)
            case unit.KEY_WR_SIT_BACK_AND_RELAX:
                task_result = tasks.wr_sit_back_and_relax(unit_obj.wr_sit_back_and_relax)
            case unit.KEY_WR_WORD_FORMATION:
                task_result = tasks.wr_word_formation(unit_obj.wr_word_formation)
            case unit.KEY_WR_USAGE:
                task_result = tasks.wr_usage(unit_obj.wr_usage)
            case unit.KEY_WR_EXTRA_CARDS:
                task_result = tasks.wr_extra_cards(unit_obj.wr_extra_cards)

            case _:
                raise ValueError(f'Unrecognized task type: {task_list[task_index]}')

        match task_result:

            case TaskResult.BACK_TO_PREVIOUS_TASK:
                task_index = max(0, task_index - 1)
                if task_index == 0:
                    output.general_message('This is the first task: Starting from the beginning.')
                continue

            case TaskResult.JUMP_TO_NEXT_TASK:
                task_index += 1
                continue

            case TaskResult.EXIT_TASK:
                break

            case TaskResult.NOT_IMPLEMENTED | TaskResult.HIDDEN | TaskResult.FINISHED:
                task_index += 1
                continue

            case _:
                raise ValueError(f'Unhandled task result: {task_result}')
