# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Other new words"""

# imports: library
from typing import Any

# imports: project
from glossanea.cli import output
from glossanea.cli.output import Formatting
from glossanea.tasks._common import TaskResult, answer_cycle

DATA_KEY: str = 'definitions'
TITLE: str = 'definitions'.upper()


def task(data: dict[str, Any],
         data_for_new_words: list[dict[str, str]],
         *_args,
         **_kwargs,
         ) -> TaskResult:
    """Display 'definitions' task"""

    output.section_title(TITLE)

    output.empty_line()
    output.simple(data['prompt'])

    output.empty_line()
    for definition in data['definitions']:
        output.numbered_sentence(definition['id'], definition['text'], Formatting.INDENTED)

    def l_words() -> None:
        """l_words"""
        output.words_table(
            [word['id'] for word in data['words']],
            [word['text'] for word in data['words']],
        )

    for definition in data['definitions']:

        prompt: str = f'{definition["id"]}. '

        def l_pr_question() -> None:
            """l_pr_question"""
            output.numbered_sentence(definition['id'], definition['text'])

        answers: list[str] = []
        answer_id: str = [
            value
            for (item_id, value) in data['answers']
            if item_id == definition['id']
        ][0]
        answers.append(answer_id)
        answer_text: str = [
            item['text']
            for item in data['words']
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
                                               data_for_new_words)
        match task_result:
            case TaskResult.SUBTASK_CORRECT_ANSWER | TaskResult.SUBTASK_SKIP_TO_NEXT:
                continue
            case _:
                return task_result

    return TaskResult.FINISHED
