import json
import os.path
from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Any


@dataclass
class Word:
    text: str
    pronunciation: Optional[str] = None
    definition: Optional[str] = None
    example: Optional[str] = None
    tags: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Word':
        return cls(**data)


@dataclass
class VocabularyMetadata:
    author: Optional[str] = None
    source: Optional[str] = None
    description: Optional[str] = None
    word_count: int = 0
    language: str = "en"


@dataclass
class Vocabulary:
    idx: int
    name: str
    words: List[Word] = field(default_factory=list)
    metadata: VocabularyMetadata = field(default_factory=VocabularyMetadata)

    def __post_init__(self):
        self.metadata.word_count = len(self.words)

    def get_word_count(self) -> int:
        return len(self.words)

    def get_word(self, idx: int) -> Word:
        if 0 <= idx < len(self.words):
            return self.words[idx]
        raise IndexError(f"Word index {idx} out of range")

    def add_word(self, word: Word) -> None:
        self.words.append(word)
        self.metadata.word_count += 1

    def remove_word(self, idx: int) -> None:
        if 0 <= idx < len(self.words):
            self.words.pop(idx)
            self.metadata.word_count -= 1
        else:
            raise IndexError(f"Word index {idx} out of range")

    def to_json(self) -> str:
        data = {
            'idx': self.idx,
            'name': self.name,
            'words': [word.to_dict() for word in self.words],
            'metadata': asdict(self.metadata)
        }
        return json.dumps(data, ensure_ascii=False, indent=2)

    @classmethod
    def from_json(cls, file_path: str, idx: int = 0) -> 'Vocabulary':
        name = os.path.basename(file_path).rsplit('.', 1)[0]
        words = []

        with open(file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if line and not line.startswith('#'):
                    parts = line.split('\t')
                    word_text = parts[0]
                    word = Word(text=word_text)

                    if len(parts) > 1:
                        word.definition = parts[1]
                        word.example = parts[2]

                    words.append(word)

        meta = VocabularyMetadata(
            source=file_path,
            word_count=len(words)
        )

        return cls(
            idx=idx,
            name=name,
            words=words,
            metadata=meta
        )

    @classmethod
    def from_text_file(cls, file_path: str, idx: int = 0) -> 'Vocabulary':
        name = os.path.basename(file_path).rsplit('.', 1)[0]
        words = []

        with open(file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if line and not line.startswith('#'):
                    parts = line.split('\t')
                    word_text = parts[0]
                    word = Word(text=word_text)

                    if len(parts) > 1:
                        word.definition = parts[1]
                    if len(parts) > 2:
                        word.example = parts[2]

                    words.append(word)

        meta = VocabularyMetadata(
            source=file_path,
            word_count=len(words)
        )

        return cls(
            idx = idx,
            name=name,
            words=words,
            metadata=meta
        )




