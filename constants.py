SPECIAL_OPERATORS = ["...", ">>>", "<<<"]

TAB_DEPENDENT_LANGUAGES = ["python", "yaml"]

C_STYLE_LANGUAGES_COMMENT = ["cpp", "js", "java", "typescript", "c", "c#", "rust", "go"]

SCRIPT_STYLE_LANGUAGES_COMMENT = ["python", "ruby"]

NESTING_MARKERS = ["}", ")", "]", "{", "(", "["]

OPEN_NESTING_MARKERS = [ "{", "(", "["]

CLOSE_NESTING_MARKERS = ["}", ")", "]"]

DICTIONARY_NESTING_MARKERS = {')': '(', '}': '{', ']': '['}

EXTENSIONS_FILE = {
    '.py': 'python', '.java': 'java', '.cpp': 'cpp',
    '.c': 'c', '.cs': 'csharp', '.js': 'javascript',
    '.rb': 'ruby', '.ts': 'typescript', '.go': 'go',
    '.rs': ' ', '.md': 'markdown', '.cc': 'cpp'}
