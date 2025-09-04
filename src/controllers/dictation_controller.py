
from rich.align import Align
from rich.columns import Columns
from rich.console import Group
from rich.text import Text

import questionary

from src.components.dictation_table import DictationTable
from src.models import Vocabulary
from src.views import Render


class DictationController:
    def __init__(self, vocabulary: Vocabulary, render: Render):
        self.vocabulary = vocabulary
        self.render = render
        self.dictation_table = DictationTable(vocabulary.get_word_count())
        self.answers = []

    def start_dictation(self):
        self._process_words()
        self._show_results()

    def _process_words(self):
        self.render.layout.update_content(Align(self.dictation_table.get_rich_table_portion(0)))
        self.render.refresh_screen()
        for i, word in enumerate(self.vocabulary.words):
            answer = questionary.text(f"{i + 1}").ask()
            if answer == "q!":
                questionary.press_any_key_to_continue().ask()
                return
            self.answers.append(answer)
            self.dictation_table.set_word_by_idx(i, answer)
            table = self.dictation_table.get_rich_table_portion(i)
            self.render.layout.update_content(Align(table))
            self.render.refresh_screen()

    def _show_results(self):
        correct = 0
        incorrect = []

        for i in range(self.vocabulary.get_word_count()):
            answer = self.vocabulary.get_word(i)
            user_answer = self.answers[i]

            if answer.lower() == user_answer.lower():
                correct += 1
            else:
                incorrect.append((answer, user_answer))

        score = int((correct / self.vocabulary.get_word_count()) * 100) if self.vocabulary.get_word_count() > 0 else 0

        # 显示结果
        compare_results = []
        for answer, user_answer in incorrect:
            compare_results.append(Text(f"{user_answer}\n{answer}"))
        results = Columns(compare_results, equal=True, expand=True)

        g = Group(
            results,
            Text(f"Your score: {str(score)}", justify="right"),
        )

        self.render.layout.update_content(g)
        self.render.refresh_screen()
        questionary.press_any_key_to_continue().ask()
