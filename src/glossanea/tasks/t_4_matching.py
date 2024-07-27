# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Other new words"""

# imports: library
from typing import Any

# imports: project
from glossanea.cli import output
from glossanea.tasks._common import TaskResult, answer_cycle

DATA_KEY: str = 'matching'


def task(unit_data: dict[str, Any]) -> TaskResult:
    """Display 'matching' task"""

    assert DATA_KEY in unit_data

    task_data: dict[str, Any] = unit_data[DATA_KEY]

    output.section_title(task_data['name'].upper())

    output.empty_line()
    output.simple(task_data['prompt'])

    output.empty_line()
    for sentence in task_data['sentences']:
        output.numbered_sentence(sentence['id'], sentence['text'], output.Formatting.INDENTED)

    def l_words() -> None:
        """l_words"""
        for word in task_data['words']:
            output.numbered_sentence(word['id'], word['text'], output.Formatting.INDENTED)

    for sentence in task_data['sentences']:

        prompt: str = f'{sentence["id"]}. '

        def l_pr_question() -> None:
            """l_pr_question"""
            output.numbered_sentence(sentence['id'], sentence['text'])

        answers: list[str] = []
        answer_id: str = [
            value
            for (item_id, value) in task_data['answers']
            if item_id == sentence['id']
        ][0]
        answers.append(answer_id)
        answer_text: str = [
            item['text']
            for item in task_data['words']
            if item['id'] == answer_id
        ][0]
        answers.append(answer_text)

        def l_pr_answer() -> None:
            """l_pr_answer"""
            l_pr_question()
            output.numbered_sentence(answer_id, answer_text)

        # answer cycle

        output.empty_line()
        l_words()
        output.empty_line()
        l_pr_question()

        task_result: TaskResult = answer_cycle(prompt,
                                               l_pr_question,
                                               answers,
                                               l_pr_answer,
                                               unit_data)
        match task_result:
            case TaskResult.SUBTASK_CORRECT_ANSWER | TaskResult.SUBTASK_SKIP_TO_NEXT:
                continue
            case _:
                return task_result

    return TaskResult.FINISHED
