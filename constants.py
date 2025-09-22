
SPECIAL_OPERATORS = ["...", ">>>", "<<<", "^..","..^"]#  + "^n.."

PASS_OPERATORS = ["^..","..^","..."]#  + "^n.."

TAB_DEPENDENT_LANGUAGES = ["python", "yaml"]

NESTING_MARKERS = ["}", ")", "]", "{", "(", "["]

OPEN_NESTING_MARKERS = [ "{", "(", "["]

CLOSE_NESTING_MARKERS = ["}", ")", "]"]

DICTIONARY_NESTING_MARKERS = {')': '(', '}': '{', ']': '['}

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
