from dataclasses import dataclass
from typing import List


@dataclass
class Vocabulary:
    idx: int
    name: str
    words: List[str]

    def __init__(self, idx: int, name: str, words: List[str]):
        self.idx = idx
        self.name = name
        self.words = words

    def get_word_count(self) -> int:
        return len(self.words)

    def get_word(self, idx) -> str:
        return self.words[idx]