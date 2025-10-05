from typing import EXCLUDED_ATTRIBUTES

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

FUNCTION_NODE_TYPES = ['function_declaration', 'function_definition', 'method_declaration', 'lambda_expression']

CONTROL_STRUCTURE_TYPES = ['if_statement', 'while_statement', 'for_statement', 'switch_statement', 'case_statement', 'do_statement', 'try_statement', 'elif_clause', 'else_clause']

BRACKET_STRUCTURE_TYPES = ['enum_specifier', 'class_specifier', 'struct_specifier', 'union_specifier', 'try_statement', 'namespace_definition']

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

EXCLUDED_TYPES= {
    '{', '}', '(', ')', 'identifier', 'parameter_list',
    'type_identifier', 'function_declarator', 'parameter',
    'type_qualifier', 'storage_class_specifier'
}



