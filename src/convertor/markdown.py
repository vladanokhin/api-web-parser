import re
from dataclasses import dataclass
from typing import List, Optional, Dict

from nltk import sent_tokenize

from .ngram import Ngram


class Markdown:
    def __init__(self, config: dataclass) -> None:
        self.cfg: dataclass = config
        part = self.Part
        self.parts: List[part] = []
        self.filename: str = ''
        self.text: str = ''
        self.parts_count: int = 0
        self.is_valid: bool = False
        self.is_cleaned: bool = False
        self.parts_removed: int = 0
        self.parts_removed_percent: int = 0
        self.is_modified: bool = False
        self.fail_reason: Optional[str] = None

    class Part:
        def __init__(self, text: str, config: dataclass) -> None:
            self.number: int = 0
            self.text: str = text
            self.cfg: dataclass = config
            self.title: Optional[str] = None
            self.content: Optional[str] = None
            self.sentences: Optional[List[str]] = None
            self.sentences_count: int = 0
            self.is_valid: bool = False
            self.is_modified: bool = False
            self.fail_reason: Optional[str] = None

        def parse(self) -> None:
            part = self.text.lstrip()
            blocks: List[str] = part.split('\n')
            self.title: str = blocks[0].strip()
            self.content: str = '\n'.join(blocks[1:]).strip()
            if not self.content:
                return None
            self.sentences: List[str] = sent_tokenize(self.content)
            self.sentences_count = len(self.sentences)

        def validate(self) -> None:
            if self.is_modified:
                self.is_valid = True
                return None

            content_len: int = len(self.content) if self.content else 0
            conditions: List[bool] = [
                self.cfg.min_part_size <= content_len <= self.cfg.max_part_size,
                self.cfg.min_part_sentences <= self.sentences_count <= self.cfg.max_part_sentences,
                len(re.sub(r'[^a-z #0-9.]', '', self.title.lower())) >= len(self.title) // 2
            ]
            reasons: List[str] = [
                f'Content size is {content_len} (must be {self.cfg.min_part_size} - {self.cfg.max_part_size})',
                f'Sentences count is {self.sentences_count} (must be {self.cfg.min_part_sentences} - {self.cfg.max_part_sentences})'
                'The half of title should contains letters',
            ]
            if all(conditions):
                self.is_valid = True
            else:
                fail_reasons: List[str] = [reasons[i] for i, condition in enumerate(conditions) if not condition]
                self.fail_reason = '; '.join(fail_reasons) if fail_reasons else None

        def modify(self):
            conditions: List[bool] = [
                len(self.content) < self.cfg.min_part_size,
                self.sentences_count < self.cfg.min_part_sentences,
            ]
            if any(conditions):
                self.content = None
            if not self.content:
                if self.number == 0:
                    self.content = self.cfg.no_content_marker
                elif self.title.startswith('## '):
                    self.title = f'#{self.title}'
                self.is_modified = True
            else:
                if self.number == 0:
                    self.content = f'{self.cfg.intro_marker}\n{self.content}'
                    self.is_modified = True

        def __str__(self) -> str:
            return f'{self.title}\n{self.content}'

        def __repr__(self) -> str:
            return self.__str__()

    @staticmethod
    def read_file(filename: str) -> str:
        with open(file=filename, mode='r') as file:
            content: str = file.read()
        return content

    @staticmethod
    def save_file(text: str, filename: str) -> None:
        with open(file=filename, mode='w+') as file:
            file.write(text)

    def resave(self):
        self.save_file(text=self.__str__(), filename=self.filename)

    def split_to_parts(self, text: str) -> List[str]:
        marker: str = self.cfg.split_section_marker
        parts: List[str] = text.split(self.cfg.split_section_marker)
        parts: List[str] = parts[:1] + [f'{marker}{item}' for i, item in enumerate(parts) if i != 0]
        return parts

    def load(self, filename: str) -> None:
        self.filename = filename
        text: str = self.read_file(filename=filename)
        self.text = text
        text_parts: List[str] = self.split_to_parts(text=text)
        for i, text_part in enumerate(text_parts):
            part = self.Part(text=text_part, config=self.cfg)
            part.number = i
            part.parse()
            self.parts.append(part)
        self.parts_count = len(self.parts)

    def validate(self) -> None:
        for part in self.parts:
            part.validate()

    def analyze(self) -> None:
        conditions: List[bool] = [
            self.cfg.min_parts <= self.parts_count <= self.cfg.max_parts,
            self.cfg.min_article_size <= len(self.text) <= self.cfg.max_article_size,
            all([part.is_valid for part in self.parts]),
            self.parts_removed_percent <= self.cfg.removed_parts_allowable_percent,
        ]
        reasons: List[str] = [
            f'Parts count is {self.parts_count} (must be {self.cfg.min_parts} - {self.cfg.max_parts})',
            f'Article size is {len(self.text)} (must be {self.cfg.min_article_size} - {self.cfg.max_article_size})',
            '; '.join([f'Part {part.number}: {part.fail_reason}' for part in self.parts if not part.is_valid]),
            f'{self.parts_removed_percent} % of parts was removed. (must be {self.cfg.removed_parts_allowable_percent}',
        ]
        if all(conditions):
            self.is_valid = True
        else:
            fail_reasons: List[str] = [reasons[i] for i, condition in enumerate(conditions) if not condition]
            self.fail_reason = '; '.join(fail_reasons) if fail_reasons else None

    @property
    def ngrams(self) -> Dict[str, int]:
        ngram_service = Ngram()
        text = ' '.join([part.content.strip() for part in self.parts if part.content])
        return ngram_service.simple_ngram(text=text, sizes=self.cfg.ngram_sizes, limit=self.cfg.ngram_limit)

    def modify(self):
        for part in self.parts:
            part.modify()
            if part.is_modified:
                self.is_modified = True

    def clear(self) -> None:
        valid_parts = [self.parts[0]] + [part for part in self.parts[1:] if part.is_valid]
        valid_parts_count: int = len(valid_parts)
        if valid_parts_count < self.parts_count:
            self.parts_removed = self.parts_count - valid_parts_count
            self.parts = valid_parts
            self.parts_removed_percent = round(self.parts_removed / self.parts_count * 100)
            self.parts_count = valid_parts_count
            self.is_cleaned = True

    @property
    def content(self) -> str:
        return '\n'.join([part.content.strip() for part in self.parts])

    def __str__(self) -> str:
        return '\n\n'.join([str(part) for part in self.parts])

    def __repr__(self) -> str:
        return self.__str__()
