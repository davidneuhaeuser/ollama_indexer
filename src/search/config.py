MAX_CHARS_PER_CHUNKED_FILE = 5000

WIKI_DIR  = './wiki/'

INDEX_FILE_PATH = WIKI_DIR + 'index.txt'

MODEL='qwen3:8b'

SYSTEM_PROMPT= \
'''
Choose ten keywords that fit well with the context.
Only output those ten keywords, separated by commas.

If an important name that consists of multiple words
should be condensed into a keyword, the output keyword
should simply be the multiple words concatenated.
'''