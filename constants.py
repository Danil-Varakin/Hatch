import tree_sitter_cpp
import tree_sitter_c
import tree_sitter_java
import tree_sitter_c_sharp
import tree_sitter_javascript
import tree_sitter_typescript
import tree_sitter_ruby
import tree_sitter_go
import tree_sitter_rust

SPECIAL_OPERATORS = ["...", ">>>", "<<<", "^..","$.."]#  + "_n."

PASS_OPERATORS = ["^..","$..","..."]#  + "_n."

TAB_DEPENDENT_LANGUAGES = ["python", "yaml"]

C_STYLE_LANGUAGES_COMMENT = ["cpp", "js", "java", "typescript", "c", "c#", "rust", "go", "gn"]

SCRIPT_STYLE_LANGUAGES_COMMENT = ["python", "ruby"]

NESTING_MARKERS = ["}", ")", "]", "{", "(", "["]

OPEN_NESTING_MARKERS = [ "{", "(", "["]

CLOSE_NESTING_MARKERS = ["}", ")", "]"]

DICTIONARY_NESTING_MARKERS = {')': '(', '}': '{', ']': '['}

EXTENSIONS_FILE = {
    '.py': 'python', '.java': 'java', '.cpp': 'cpp',
    '.c': 'c', '.cs': 'csharp', '.js': 'javascript',
    '.rb': 'ruby', '.ts': 'typescript', '.go': 'go',
    '.rs': ' ', '.md': 'markdown', '.cc': 'cpp', '.gn': 'gn', '.gni': 'gn', '.ninja': 'gn'}

LANGUAGE_MAP = {
    'cpp': tree_sitter_cpp.language(),
    'c': tree_sitter_c.language(),
    'java': tree_sitter_java.language(),
    'csharp': tree_sitter_c_sharp.language(),
    'javascript': tree_sitter_javascript.language(),
    'typescript': tree_sitter_typescript.language_typescript(),
    'ruby': tree_sitter_ruby.language(),
    'go': tree_sitter_go.language(),
    'rust': tree_sitter_rust.language(),
}

NESTING_CONTEXTS = {
    'cpp': ['template_argument_list', 'template_declaration', 'preproc_include', 'template_parameter_list'],
    'c': [],
    'java': ['type_arguments'],
    'csharp': ['type_argument_list'],
    'javascript': ['jsx_opening_element', 'jsx_closing_element', 'type_arguments'],
    'typescript': ['type_arguments'],
    'ruby': [],
    'go': [],
    'rust': ['type_arguments'],
}