
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

IMPORTANT_TYPES = {
    'function_definition', 'method_definition',
    'for_statement', 'while_statement', 'do_statement',
    'if_statement', 'switch_statement', 'conditional_expression'
}

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


OUTPUT_PATH = 'CodeComprasion/my-languages.so'

GRAMMAR_PATHS = [
    'tree-sitter-grammars/tree-sitter-python',
    'tree-sitter-grammars/tree-sitter-cpp',
    'tree-sitter-grammars/tree-sitter-java',
    'tree-sitter-grammars/tree-sitter-c',
    'tree-sitter-grammars/tree-sitter-c-sharp',
    'tree-sitter-grammars/tree-sitter-javascript',
    'tree-sitter-grammars/tree-sitter-ruby',
    'tree-sitter-grammars/tree-sitter-typescript/tsx',
    'tree-sitter-grammars/tree-sitter-go',
    'tree-sitter-grammars/tree-sitter-rust',
    'tree-sitter-grammars/tree-sitter-markdown',
]


