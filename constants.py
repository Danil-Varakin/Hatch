
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

FUNCTION_NODE_TYPES_CPP = ['function_declaration', 'function_definition', 'method_declaration', 'lambda_expression']

CONTROL_STRUCTURE_TYPES_CPP = ['if_statement', 'while_statement', 'for_statement', 'switch_statement', 'case_statement', 'do_statement', 'try_statement', 'elif_clause', 'else_clause', 'goto_statement', 'break_statement', 'continue_statement', 'return_statement', 'labeled_statement', 'seh_try_statement', 'seh_leave_statement', 'preproc_if', 'preproc_elif', 'preproc_else', 'preproc_ifdef', 'preproc_elifdef']

BRACKET_STRUCTURE_TYPES_CPP = ['enum_specifier', 'class_specifier', 'struct_specifier', 'union_specifier', 'try_statement', 'namespace_definition', 'attribute_declaration', 'compound_literal_expression', 'generic_expression']

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



DICTIONARY_SOLID_STRUCTURES_CPP = {
    "function_definition": [
        "_declarator", "function_declarator", "parameter_list", "parameter_declaration",
        "compound_statement", "type_specifier", "type_identifier", "identifier",
        "statement", "expression", ";", "{", "}", "(", ")", "primitive_type"
    ],
    "declaration": [
        "type_specifier", "_declarator", "init_declarator", "type_identifier",
        "identifier", "initializer_list", "expression", ";", "const", "volatile",
        "static", "extern", "type_qualifier", "storage_class_specifier"
    ],
    "expression_statement": [
        "expression", "assignment_expression", "binary_expression", "unary_expression",
        "call_expression", "identifier", "number_literal", "string_literal", ";"
    ],
    "if_statement": [
        "expression", "parenthesized_expression", "statement", "compound_statement",
        "else_clause", "if", "else", "(", ")", "{", "}"
    ],
    "for_statement": [
        "expression", "declaration", "init_declarator", "statement", "compound_statement",
        "for", "(", ")", ";", ",", "assignment_expression", "update_expression"
    ],
    "while_statement": [
        "expression", "parenthesized_expression", "statement", "compound_statement",
        "while", "(", ")", "{", "}"
    ],
    "do_statement": [
        "statement", "compound_statement", "expression", "parenthesized_expression",
        "do", "while", "(", ")", ";", "{", "}"
    ],
    "switch_statement": [
        "expression", "parenthesized_expression", "statement", "compound_statement",
        "case_statement", "switch", "case", "default", "(", ")", "{", "}"
    ],
    "return_statement": [
        "expression", "return", ";"
    ],
    "break_statement": [
        "break", ";"
    ],
    "continue_statement": [
        "continue", ";"
    ],
    "goto_statement": [
        "goto", "statement_identifier", ";"
    ],
    "labeled_statement": [
        "statement_identifier", "statement", ":", "case", "default"
    ],
    "compound_statement": [
        "statement", "declaration", "expression_statement", "{", "}"
    ],
    "case_statement": [
        "expression", "number_literal", "statement", "case", ":", "default"
    ],
    "preproc_if": [
        "preproc_directive", "expression", "preproc_defined", "#if", "#endif",
        "preproc_elif", "preproc_else", "statement"
    ],
    "preproc_ifdef": [
        "preproc_directive", "identifier", "#ifdef", "#ifndef", "#endif",
        "preproc_elif", "preproc_else"
    ],
    "preproc_elif": [
        "preproc_directive", "expression", "preproc_defined", "#elif"
    ],
    "preproc_elifdef": [
        "preproc_directive", "identifier", "#elifdef", "#elifndef"
    ],
    "preproc_else": [
        "preproc_directive", "#else"
    ],
    "preproc_include": [
        "preproc_directive", "system_lib_string", "#include"
    ],
    "preproc_def": [
        "preproc_directive", "identifier", "preproc_arg", "#define"
    ],
    "preproc_function_def": [
        "preproc_directive", "identifier", "preproc_params", "preproc_arg", "#define"
    ],
    "preproc_call": [
        "preproc_directive", "identifier", "preproc_arg"
    ],
    "type_definition": [
        "type_specifier", "type_identifier", "_type_declarator", "typedef", ";"
    ],
    "enum_specifier": [
        "type_identifier", "enumerator_list", "enumerator", "enum", "{", "}", ","
    ],
    "struct_specifier": [
        "type_identifier", "field_declaration_list", "field_declaration",
        "field_identifier", "struct", "{", "}", ";"
    ],
    "union_specifier": [
        "type_identifier", "field_declaration_list", "field_declaration",
        "field_identifier", "union", "{", "}", ";"
    ],
    "linkage_specification": [
        "extern", "string_literal", "declaration", "function_definition", "{", "}"
    ],
    "attributed_statement": [
        "attribute_specifier", "attribute", "statement"
    ],
    "seh_try_statement": [
        "__try", "compound_statement", "seh_except_clause", "seh_finally_clause"
    ],
    "seh_leave_statement": [
        "__leave", ";"
    ],
    "translation_unit": [
        "declaration", "function_definition", "preproc_include", "preproc_def"
    ],
    "gnu_asm_expression": [
        "__asm", "__asm__", "string_literal", "gnu_asm_input_operand",
        "gnu_asm_output_operand", "gnu_asm_clobber_list", "gnu_asm_goto_list",
        "gnu_asm_qualifier", "(", ")", ":"
    ],
    "alignof_expression": [
        "_alignof", "__alignof", "__alignof__", "type_identifier", "expression", "(", ")"
    ],
    "sizeof_expression": [
        "sizeof", "type_identifier", "expression", "(", ")"
    ],
    "offsetof_expression": [
        "offsetof", "type_identifier", "field_identifier", "(", ")", ","
    ],
    "cast_expression": [
        "type_descriptor", "expression", "(", ")"
    ],
    "compound_literal_expression": [
        "type_descriptor", "initializer_list", "(", ")", "{", "}"
    ],
    "generic_expression": [
        "_Generic", "expression", "type_descriptor", "(", ")", ","
    ],
    "attribute_declaration": [
        "attribute_specifier", "attribute", "declaration"
    ]
}
