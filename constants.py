
LOG_COLORS = {
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red'}

LOG_ENABLE_TRUNCATION: bool = True

LOG_MAX_REPR_LENGTH: int = 1000

LOG_MAX_ITEMS_TO_SHOW: int = 10

LOG_TRUNCATE_MESSAGE: str = "<...truncated...>"

SPECIAL_OPERATORS = ["...", ">>>", "<<<", "^..","..^"]#  + "^n.."

PASS_OPERATORS = ["^..","..^","..."]#  + "^n.."

TAB_DEPENDENT_LANGUAGES = ["python", "yaml"]

NESTING_MARKERS = ["}", ")", "]", "{", "(", "["]

OPEN_NESTING_MARKERS = [ "{", "(", "["]

CLOSE_NESTING_MARKERS = ["}", ")", "]"]

CLOSE_TO_OPEN_NESTING_MARKERS = {')': '(', '}': '{', ']': '['}

OPEN_TO_CLOSE_NESTING_MARKERS = {'(': ')', '{': '}', '[': ']'}

EXTENSIONS_FILE = {
    '.py': 'python', '.java': 'java', '.cpp': 'cpp',
    '.c': 'c', '.cs': 'csharp', '.js': 'javascript',
    '.rb': 'ruby', '.ts': 'typescript', '.go': 'go',
    '.rs': ' ', '.md': 'markdown', '.cc': 'cpp', '.gn': 'gn', '.gni': 'gn', '.ninja': 'gn'}


COMMENT_PATTERN = {
        'python': r"#.*?$",
        'java': r"//.*?$|/\*.*?\*/",
        'cpp': r"//.*?$|/\*.*?\*/",
        'c': r"//.*?$|/\*.*?\*/",
        'csharp': r"//.*?$|/\*.*?\*/",
        'javascript': r"//.*?$|/\*.*?\*/",
        'ruby': r"#.*?$|=begin.*?=end",
        'typescript': r"//.*?$|/\*.*?\*/",
        'go': r"//.*?$|/\*.*?\*/",
        'rust': r"//.*?$|/\*.*?\*/",
        'markdown': r"<!--.*?-->",
        'gn': r"#.*?$"
    }

RE_STRING_PATTERN = r'"[^"\\]*(?:\\.[^"\\]*)*"|\'[^\'\\]*(?:\\.[^\'\\]*)*\''

SPECIAL_OPERATORS_AND_NESTING_MARKERS_PATTERN = r"(\.\.\.|>>>|<<<|\^\.\.|\.\.\^|\^[1-9]\d*\.\.|\(|\)|\[|\]|\{|\})"

SPECIAL_OPERATORS_PATTERN = r"\.\.\.|>>>|<<<|\^\.\.|\.\.\^|\^[1-9]\d*\.\."
