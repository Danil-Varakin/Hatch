FUNCTION_NODE_TYPES = [
    "function_definition",
    "lambda",
]

CONTROL_STRUCTURE_TYPES = [
    "if_statement",
    "for_statement",
    "while_statement",
    "try_statement",
    "with_statement",
    "match_statement",
    "elif_clause",
    "else_clause",
    "except_clause",
    "finally_clause",
    "case_clause",
]

BRACKET_STRUCTURE_TYPES = [
    "class_definition",
    "function_definition",
    "with_statement",
    "try_statement",
    "match_statement",
    "dictionary",
    "set",
    "parameters",
    "argument_list",
    "list",
    "tuple",
    "generator_expression",
    "list_comprehension",
    "set_comprehension",
    "dictionary_comprehension",
    "parameters",
]

EXCLUDED_TYPES = {
    "{", "}", "(", ")", "[", "]",
    "identifier",
    "variable_name",
    "type",
    "type_parameter",
    "parameter",
    "default_parameter",
    "typed_parameter",
    "list_pattern",
    "as_pattern",
}

DICTIONARY_SOLID_STRUCTURES = {
    "function_definition": [
        "block",
        "parameters",
        "identifier",
        "type_parameter",
        "return_type",
        "decorators",
        "->",
    ],
    "lambda": [
        "parameters",
        "expression",
        "lambda",
    ],
    "class_definition": [
        "block",
        "identifier",
        "argument_list",
        "decorators",
    ],
    "if_statement": [
        "condition",
        "consequence",
        "alternative",
        "elif_clause",
        "else_clause",
    ],
    "elif_clause": [
        "condition",
        "consequence",
    ],
    "else_clause": [
        "block",
    ],
    "for_statement": [
        "left",
        "right",
        "block",
        "else_clause",
    ],
    "while_statement": [
        "condition",
        "block",
        "else_clause",
    ],
    "try_statement": [
        "block",
        "except_clause",
        "else_clause",
        "finally_clause",
    ],
    "except_clause": [
        "expression",
        "as_clause",
        "block",
    ],
    "finally_clause": [
        "block",
    ],
    "with_statement": [
        "with_clause",
        "block",
    ],
    "with_clause": [
        "with_item",
    ],
    "match_statement": [
        "subject",
        "case_clause",
    ],
    "case_clause": [
        "case_pattern",
        "guard",
        "block",
    ],
    "dictionary": [
        "pair",
        "splat_pattern",
    ],
    "list": ["element", "splat_pattern"],
    "tuple": ["element", "splat_pattern"],
    "set": ["element", "splat_pattern"],
    "list_comprehension": [
        "element",
        "for_in_clause",
        "if_clause",
    ],
    "call": [
        "function",
        "argument_list",
        "identifier",
        "attribute",
    ],
    "return_statement": [
        "expression",
    ],
    "raise_statement": [
        "expression",
    ],
    "assert_statement": [
        "expression",
    ],
    "import_statement": [
        "import_clause",
        "aliased_import",
    ],
    "future_import_statement": [
        "future_import_clause",
    ],
    "import_from_statement": [
        "dotted_name",
        "wildcard_import",
        "import_clause",
    ],
}

BRACKET_TO_NODE_TYPES = {
    "{": [
        "dictionary",
        "set",
        "dictionary_comprehension",
        "class_definition",
        "function_definition",
        "match_statement",
        "with_statement",
        "try_statement",
    ],
    "(": [
        "parameters",
        "argument_list",
        "tuple",
        "generator_expression",
        "parenthesized_expression",
        "call",
        "lambda",
    ],
    "[": [
        "list",
        "list_comprehension",
        "subscript",
        "list_pattern",
    ],
    ":": [
        "case_clause",
    ],
}

NESTED_STRUCTURES = [
    "block",
    "module",
    "function_definition",
    "class_definition",
    "if_statement",
    "elif_clause",
    "else_clause",
    "for_statement",
    "while_statement",
    "try_statement",
    "except_clause",
    "finally_clause",
    "with_statement",
    "match_statement",
    "case_clause",
    "list_comprehension",
    "set_comprehension",
    "dictionary_comprehension",
    "generator_expression",
    "parameters",
    "argument_list",
    "tuple",
    "list",
    "set",
    "dictionary",
]