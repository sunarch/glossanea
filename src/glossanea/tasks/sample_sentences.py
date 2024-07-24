# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Other new words"""

# imports: library
from typing import Any

# imports: project
from glossanea.cli import output
from glossanea.tasks._common import TaskResult, answer_cycle
from glossanea.tasks.new_words_common import new_words


def task(data: dict[str, Any],
         new_words_extension: list[str],
         data_for_new_words: list[dict[str, str]],
         ) -> TaskResult:
    """Display 'sample sentences' task"""

    output.section_title('SAMPLE SENTENCES')

    output.empty_line(1)
    output.simple(data['prompt'])

    output.empty_line(1)

    for sentence in data['sentences']:
        output.numbered_sentence(sentence['id'],
                                 sentence['beginning'] + output.BLANK + sentence['end'],
                                 output.Formatting.INDENTED)

    output.new_words_extension(new_words_extension)

    output.empty_line(1)

    for sentence in data['sentences']:

        prompt: str = f'{sentence["id"]}. '

        def l_pr_question() -> None:
            """l_pr_question"""
            return output.numbered_sentence(sentence['id'],
                                            sentence['beginning'] + output.BLANK + sentence['end'])

        answers: list[str] = [sentence['answer']]

        full_answer: str = sentence['answer']
        if len(sentence['beginning']) > 0:
            full_answer = f'{sentence["beginning"]} {full_answer}'
        if len(sentence['end']) > 0:
            if sentence['end'] not in ['.', '!', '?', '?!', '!?']:
                full_answer += ' '
            full_answer += sentence['end']

        def l_pr_answer() -> None:
            """l_pr_answer"""
            return output.simple(full_answer)

        # answer cycle

        new_words(data_for_new_words, False)
        output.empty_line(1)
        l_pr_question()

        task_result: TaskResult = answer_cycle(prompt, l_pr_question, answers, l_pr_answer, data_for_new_words)

        if task_result in {
            TaskResult.SUBTASK_CORRECT_ANSWER,
            TaskResult.SUBTASK_SKIP_TO_NEXT,
        }:
            continue

        return task_result

    return TaskResult.FINISHED
