from collections import Counter
from typing import List, Set, Dict

from textblob import WordList, TextBlob


class Ngram:
    @staticmethod
    def simple_ngram(text: str, sizes: Set[int], limit: int = 10) -> Dict[str, int]:
        ngrams: List[str] = []
        for size in sizes:
            ngram_object = TextBlob(text.strip().lower())
            words_list: List[WordList] = ngram_object.ngrams(n=size)
            ngrams += [' '.join(ngram) for ngram in words_list]
        counter = Counter(ngrams)
        return dict(counter.most_common(limit))
