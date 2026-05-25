
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

MAX_NUMBER_OF_LINES_IN_SIBLINGS = 5

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
    '.rs': 'rust', '.md': 'markdown', '.cc': 'cpp', '.gn': 'gn', '.gni': 'gn', '.ninja': 'gn'}

COMMENT_NODES = {
    "python":     {"comment"},
    "javascript": {"comment"},
    "typescript": {"comment"},
    "rust":       {"line_comment", "block_comment"},
    "go":         {"comment"},
    "java":       {"line_comment", "block_comment"},
    "c":          {"comment"},
    "cpp":        {"comment"},
    "c_sharp":    {"comment", "multiline_comment"},
    "ruby":       {"comment"},
    "php":        {"comment", "doc_comment"},
    "swift":      {"comment", "multiline_comment"},
    "kotlin":     {"line_comment", "multiline_comment"},
    "bash":       {"comment"},
    "html":       {"comment"},
    "css":        {"comment"},
    "json":       set(),  # нет комментариев
    "toml":       {"comment"},
    "yaml":       {"comment"},
    "sql":        {"comment", "marginalia"},
}

LANGUAGE_MAP = {
    "python":     "tree_sitter_python",
    "javascript": "tree_sitter_javascript",
    "typescript": "tree_sitter_typescript",
    "rust":       "tree_sitter_rust",
    "go":         "tree_sitter_go",
    "java":       "tree_sitter_java",
    "c":          "tree_sitter_c",
    "cpp":        "tree_sitter_cpp",
    "c_sharp":    "tree_sitter_c_sharp",
    "ruby":       "tree_sitter_ruby",
    "php":        "tree_sitter_php",
    "swift":      "tree_sitter_swift",
    "kotlin":     "tree_sitter_kotlin",
    "bash":       "tree_sitter_bash",
    "html":       "tree_sitter_html",
    "css":        "tree_sitter_css",
    "json":       "tree_sitter_json",
    "toml":       "tree_sitter_toml",
    "yaml":       "tree_sitter_yaml",
    "sql":        "tree_sitter_sql",
}

STRING_PATTERNS = {
    'python':     r"""(?x) (?: r?b?u? (?: " (?: [^"\\] | \\. )* " | ' (?: [^'\\] | \\. )* ' ) )""",
    'javascript': r"""(?x) (?: " (?: [^"\\] | \\. )* " | ' (?: [^'\\] | \\. )* ' | ` (?: [^`\\] | \\. )* ` )""",
    'typescript': r"""(?x) (?: " (?: [^"\\] | \\. )* " | ' (?: [^'\\] | \\. )* ' | ` (?: [^`\\] | \\. )* ` )""",
    'ruby':       r"""(?x) (?: " (?: [^"\\] | \\. | \#{.*?} )* " | ' (?: [^'\\] | \\. )* ' | %[qQwWixrs](.) .*? \1 | <<[-~]?["'`]?(\w+)["'`]? .*?^\s*\2$ )""",
    'cpp':    r"""(?x) (?: " (?: [^"\\] | \\. )* " | ' (?: [^'\\] | \\. ) ' | R"[^"]*\([^"]*\)" )""",
    'c':      r"""(?x) (?: " (?: [^"\\] | \\. )* " | ' (?: [^'\\] | \\. ) ' )""",
    'java':   r"""(?x) (?: " (?: [^"\\] | \\. )* " | ' (?: [^'\\] | \\. ) ' )""",
    'csharp': r"""(?x) (?: @?" (?: [^"] | "" )* " | ' (?: [^'\\] | \\. ) ' | @' (?: [^'] | '' )* ' )""",
    'go':     r"""(?x) (?: " (?: [^"\\] | \\. )* " | ' (?: [^'\\] | \\. ) ' | ` [^`]* ` )""",
    'rust':   r"""(?x) (?: b? " (?: [^"\\] | \\. )* " | b?' (?: [^'\\] | \\. )? ' | r#* " (?: . )*? " #* )""",
    'markdown': r'(?x) (?: `+ (?: [^`]+ | `(?![`]) )*? `+ )',
    'gn':       r"""(?x) (?: " (?: [^"\\] | \\. )* " )"""
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

SPECIAL_OPERATORS_AND_NESTING_MARKERS_PATTERN = r"(\.\.\.|>>>|<<<|\^\.\.|\.\.\^|\^[1-9]\d*\.\.|\(|\)|\[|\]|\{|\})"

