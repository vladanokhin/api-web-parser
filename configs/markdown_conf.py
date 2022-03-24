from dataclasses import field


class MarkDownConfig:
    
    SPLIT_SECTION_MARKER = '\n##'    # marker to split text sections
    
    EOL_MARKER = '\\n'               # end of line delimiter
    
    EOF_MARKER = '<|endoftext|>'     # article delimiter
    
    NO_CONTENT_MARKER = '<|pass|>'   # marker for empty part content
    
    INTRO_MARKER = '## Intro:'       # marker for intro content
    
    MIN_PART_SIZE = 40               # minimum letters in one part to make it valid
    
    MAX_PART_SIZE = 3000             # maximum letters in one part to make it valid
    
    MIN_PART_SENTENCES = 2           # minimum sentences in one part to make it valid
    
    MAX_PART_SENTENCES = 200         # maximum sentences in one part to make it valid
    
    MIN_PARTS = 3                    # minimum titles per article
    
    MAX_PARTS = 20                   # maximum titles per article
    
    MIN_ARTICLE_SIZE = 1500          # minimum letters per article
    
    MAX_ARTICLE_SIZE = 10000         # maximum letters per article
    
    MIN_SCORE: float = 0.7           # minimal classifier score to gather markdown file
    
    NGRAM_SIZES = field(             # sizes of ngrams, collected from text
        default_factory=lambda: {8, 9}
    )  
    
    NGRAM_LIMIT = 10                 # max ngram number per one article
    
    MAX_NGRAM_DUPLICATES = 2         # max ngram duplicates to mark the article as correct
    
    REMOVED_PARTS_ALLOWABLE_PERCENT = 20  # how match parts can be removed in article (percent)
    