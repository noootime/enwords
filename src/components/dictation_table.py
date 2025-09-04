from src.models import WordGrid
from src.views import DictationTableView


class DictationTable:
    def __init__(self, words_count: int):
        self.word_grid = WordGrid(words_count)
        self.view = DictationTableView(self.word_grid)
        self.words_count = words_count

    def set_word_by_idx(self, idx: int, word: str):
        self.word_grid.update_word(idx, word)

    def get_rich_table_portion(self, idx: int):
        return self.view.create_table(idx)

