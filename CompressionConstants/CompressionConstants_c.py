FUNCTION_NODE_TYPES = [
    'function_definition',
    'declaration',
    'call_expression',
    'preproc_function_def',
]

CONTROL_STRUCTURE_TYPES = [
    'if_statement',
    'while_statement',
    'for_statement',
    'switch_statement',
    'else_clause',
    'case_statement',
    'do_statement',
    'preproc_if',
    'preproc_elif',
    'preproc_else',
    'preproc_ifdef',
    'preproc_elifdef',
]

BRACKET_STRUCTURE_TYPES = [
    'struct_specifier',
    'union_specifier',
    'enum_specifier',
    'compound_statement',
    'statement_expression',
]

EXCLUDED_TYPES = {
    '{', '}', '(', ')', '[', ']',
    'identifier',
    'type_identifier',
    'field_identifier',
    'primitive_type',
    'sized_type_specifier',
    'type_qualifier',
    'storage_class_specifier',
    'type_definition',
    'parameter_declaration',
    'parameter_list',
    'init_declarator',
    'declaration',
    ';',
}

DICTIONARY_SOLID_STRUCTURES = {
    "function_definition": [
        "compound_statement", "type_specifier", "primitive_type",
        "sized_type_specifier", "identifier", "function_declarator",
        "declaration", "statement", "expression"
    ],

    "call_expression": [
        "function", "argument_list", "identifier", "field_expression"
    ],

    "expression_statement": [
        "expression", "assignment_expression", "binary_expression",
        "unary_expression", "call_expression", "identifier",
        "number_literal", "string_literal", "cast_expression"
    ],

    "if_statement": [
        "condition", "compound_statement", "statement",
        "else_clause", "if"
    ],

    "else_clause": [
        "else", "statement", "compound_statement"
    ],

    "for_statement": [
        "initializer", "condition", "update", "compound_statement",
        "statement", "for"
    ],

    "while_statement": [
        "condition", "compound_statement", "statement", "while"
    ],

    "do_statement": [
        "statement", "compound_statement", "condition", "do", "while"
    ],

    "switch_statement": [
        "condition", "compound_statement", "statement",
        "case_statement", "switch"
    ],

    "case_statement": [
        "expression", "statement", "case", "default"
    ],

    "return_statement": [
        "expression", "return"
    ],

    "break_statement": [
        "break"
    ],

    "continue_statement": [
        "continue"
    ],

    "goto_statement": [
        "goto", "statement_identifier"
    ],

    "labeled_statement": [
        "statement_identifier", "statement"
    ],

    "compound_statement": [
        "statement", "declaration", "expression_statement"
    ],

    "struct_specifier": [
        "struct", "type_identifier", "field_declaration_list"
    ],

    "union_specifier": [
        "union", "type_identifier", "field_declaration_list"
    ],

    "enum_specifier": [
        "enum", "type_identifier", "enumerator_list"
    ],

    "preproc_if": [
        "preproc_directive", "expression", "#if", "#endif",
        "preproc_elif", "preproc_else", "statement"
    ],

    "preproc_ifdef": [
        "preproc_directive", "identifier", "#ifdef", "#ifndef", "#endif",
        "preproc_elif", "preproc_else"
    ],

    "preproc_elif": [
        "preproc_directive", "expression", "#elif"
    ],

    "preproc_elifdef": [
        "preproc_directive", "identifier", "#elifdef", "#elifndef"
    ],

    "preproc_else": [
        "preproc_directive", "#else"
    ],

    "preproc_include": [
        "preproc_directive", "string_literal", "system_lib_string", "#include"
    ],

    "preproc_def": [
        "preproc_directive", "identifier", "preproc_arg", "#define"
    ],

    "preproc_function_def": [
        "preproc_directive", "identifier", "preproc_params", "preproc_arg", "#define"
    ],

    "cast_expression": [
        "type_descriptor", "expression"
    ],

    "sizeof_expression": [
        "sizeof", "type_descriptor", "expression"
    ],

    "alignof_expression": [
        "_Alignof", "__alignof", "__alignof__"
    ],
}

BRACKET_TO_NODE_TYPES = {
    '{': [
        'function_definition',
        'compound_statement',
        'if_statement',
        'while_statement',
        'for_statement',
        'do_statement',
        'switch_statement',
        'else_clause',
        'struct_specifier',
        'union_specifier',
        'enum_specifier',
        'statement_expression',
    ],
    '(': [
        'function_declarator',
        'parameter_list',
        'argument_list',
        'call_expression',
        'condition',
        'parenthesized_expression',
        'cast_expression',
        'sizeof_expression',
        'alignof_expression',
        'preproc_function_def',
    ],
    ')': [
        'preproc_if',
        'preproc_elif',
    ],
    '[': [
        'subscript_expression',
        'array_declarator',
    ],
    ':': [
        'case_statement',
    ],
    'else': [
        'preproc_else',
    ],
    'ifdef': [
        'preproc_ifdef',
        'preproc_elifdef',
    ]
}

NESTED_STRUCTURES = [
    "compound_statement",
    "statement",
    "declaration",
    "function_definition",
    "if_statement",
    "else_clause",
    "for_statement",
    "while_statement",
    "do_statement",
    "switch_statement",
    "case_statement",
    "struct_specifier",
    "union_specifier",
    "enum_specifier",
    "initializer_list",
    "field_declaration_list",
    "enumerator_list",
    "argument_list",
    "parameter_list",
    "preproc_if",
    "preproc_ifdef",
    "preproc_elif",
    "preproc_elifdef",
    "preproc_else",
    "translation_unit",
    "statement_expression",
]