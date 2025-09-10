import os
from typing import List, Optional
from src.models.vocabulary import Vocabulary
from src.config import Config

class VocabularyRepository:
    def __init__(self, config: Config):
        self.config = config
        self.exam_dir = config.get_exam_dir()

    def get_all_vocabularies(self) -> List[Vocabulary]:
        vocabularies = []
        files = self._list_vocabulary_files()

        for i, file in enumerate(files):
            file_path = os.path.join(self.exam_dir, file)
            try:
                vocabulary = Vocabulary.from_text_file(file_path, i)
                vocabularies.append(vocabulary)
            except Exception as e:
                print(f"Loading vocabulary files failed {file}: {str(e)}")

        return vocabularies

    def get_vocabulary_by_id(self, vocab_id: int) -> Optional[Vocabulary]:
        vocabularies = self.get_all_vocabularies()
        for vocab in vocabularies:
            if vocab.idx == vocab_id:
                return vocab
        return None

    def save_vocabulary(self, vocabulary: Vocabulary) -> bool:
        try:
            file_name = f"{vocabulary.name}.txt"
            file_path = os.path.join(self.exam_dir, file_name)

            with open(file_path, 'w', encoding=self.config.get('default_encoding')) as f:
                for word in vocabulary.words:
                    parts = [word.text]
                    if word.definition:
                        parts.append(word.definition)
                    if word.example:
                        parts.append(word.example)
                    f.write('\t'.join(parts) + '\n')
            return True
        except Exception as e:
            print(f"Save vocabulary failed: {str(e)}")
            return False

    def delete_vocabulary(self, vocabulary_name: str) -> bool:
        pass

    def _list_vocabulary_files(self) -> List[str]:
        if not os.path.exists(self.exam_dir):
            os.makedirs(self.exam_dir)
            return []

        files = [f for f in os.listdir(self.exam_dir)
                 if os.path.isfile(os.path.join(self.exam_dir, f))
                 and f.lower().endswith('.txt')]

        return sorted(files)