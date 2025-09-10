import os
from typing import List

from src.models import Vocabulary, Word

EXAM_DIR = "exams"

class VocabularyManager:
    def __init__(self):
        create_exam_dir()
        self.vocabularies = load_vocabularies()

    def list_vocabularies(self) -> List[Vocabulary]:
        return self.vocabularies

def load_vocabularies() -> List[Vocabulary]:
    files = list_exam_files()
    vocabularies = []
    for i, file in enumerate(files, 1):
        file_path = os.path.join(EXAM_DIR, file)
        with open(file_path, 'r', encoding='utf-8') as f:
            words = [Word(line.strip()) for line in f if line.strip()]
        vocabularies.append(Vocabulary(i, file, words))
    return vocabularies

def create_exam_dir():
    if not os.path.exists(EXAM_DIR):
        os.makedirs(EXAM_DIR)
        print(f"已创建考试目录 {os.path.abspath(EXAM_DIR)}")
    else:
        print(f"使用考试目录 {os.path.abspath(EXAM_DIR)}")

def list_exam_files():
    if not os.path.exists(EXAM_DIR):
        return []
    files = [f for f in os.listdir(EXAM_DIR)
             if os.path.isfile(os.path.join(os.path.abspath(EXAM_DIR), f))
             and f.lower().endswith('.txt')]
    return sorted(files)
