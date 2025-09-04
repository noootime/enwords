from typing import List, Tuple

class WordGrid:
    def __init__(self, words_count: int, cols: int = 6):
        self.cols = cols
        self.words_count = words_count
        self._grid: List[List[str]] = []
        self._init_grid()

    def _init_grid(self):
        items = [f"{i + 1}.__________" for i in range(self.words_count)]
        self._grid = [items[i:i + self.cols] for i in range(0, len(items), self.cols)]

    def get_position(self, idx: int) -> Tuple[int, int]:
        return idx // self.cols, idx % self.cols

    def update_word(self, idx: int, word: str, max_width: int = 10):
        if 0 <= idx < self.words_count:
            row, col = self.get_position(idx)
            formatted_word = word.ljust(max_width)[:max_width]
            self._grid[row][col] = f"{idx + 1}.{formatted_word}"

    def get_grid(self) -> List[List[str]]:
        return self._grid[:]