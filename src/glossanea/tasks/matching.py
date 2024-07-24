# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Other new words"""

# imports: library
from typing import Any

# imports: project
from glossanea.cli import output
from glossanea.tasks._common import TaskResult, answer_cycle


def task(data: dict[str, Any],
         data_for_new_words: list[dict[str, str]],
         ) -> TaskResult:
    """Display 'matching' task"""

    # skip until data files are complete
    return TaskResult.NOT_IMPLEMENTED

    output.section_title(data['name'])

    output.empty_line(1)
    output.simple(data['prompt'])

    output.empty_line(1)
    for sentence in data['sentences']:
        output.numbered_sentence(sentence['id'], sentence['text'], output.Formatting.INDENTED)

    def l_words() -> list[None]:
        """l_words"""
        return [output.numbered_sentence(word['id'], word['text'], output.Formatting.INDENTED)
                for word in data['words']]

    for sentence in data['sentences']:

        prompt: str = f'{definition["id"]}. '

        def l_pr_question() -> None:
            """l_pr_question"""
            return output.numbered_sentence(sentence['id'], sentence['text'])

        answers: list[str] = []
        answer_id: str = [
            value
            for (item_id, value) in data['answers']
            if item_id == sentence['id']
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
            return output.numbered_sentence(answer_id, answer_text)

        # answer cycle

        output.empty_line(2)
        l_words()
        output.empty_line(1)
        l_pr_question()

        task_result: TaskResult = answer_cycle(prompt, l_pr_question, answers, l_pr_answer, data_for_new_words)
        match task_result:
            case TaskResult.SUBTASK_CORRECT_ANSWER | TaskResult.SUBTASK_SKIP_TO_NEXT:
                continue
            case _:
                return task_result

    return TaskResult.FINISHED
