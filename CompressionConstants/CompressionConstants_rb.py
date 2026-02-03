
FUNCTION_NODE_TYPES = [
    'method',
    'singleton_method',
    'alias_method',
    'call',
    'super',
    'yield',
]

CONTROL_STRUCTURE_TYPES = [
    'if',
    'unless',
    'case',
    'when',
    'while',
    'until',
    'for',
    'begin',
    'rescue',
    'ensure',
    'else',
    'return',
    'break',
    'next',
    'redo',
]

BRACKET_STRUCTURE_TYPES = [
    'class',
    'module',
    'singleton_class',
    'block',
    'do_block',
    'program',
    'begin_block',
    'end_block',
]

EXCLUDED_TYPES = {
    '{', '}', '(', ')', '[', ']',
    'identifier', 'constant', 'self', 'super',
    'instance_variable', 'class_variable', 'global_variable',
    'symbol', 'hash_key_symbol',
    'end',
    'then', 'do', 'in',
    'comment',
    'program'
}

DICTIONARY_SOLID_STRUCTURES = {
    "method": [
        "identifier", "method_parameters", "body_statement",
        "rescue", "ensure", "end"
    ],
    "singleton_method": [
        "object_pattern", "identifier", "method_parameters", "body_statement"
    ],
    "call": [
        "receiver", "selector", "argument_list", "block",
        "identifier", "method_identifier", "operator"
    ],
    "if": [
        "condition", "consequence", "alternative", "elsif", "else", "then"
    ],
    "unless": [
        "condition", "consequence", "alternative", "else"
    ],
    "case": [
        "condition", "when", "else"
    ],
    "when": [
        "pattern", "body", "then"
    ],
    "while": [
        "condition", "body"
    ],
    "until": [
        "condition", "body"
    ],
    "for": [
        "pattern", "collection", "body"
    ],
    "begin": [
        "body_statement", "rescue", "else", "ensure"
    ],
    "rescue": [
        "exceptions", "variable", "body"
    ],
    "class": [
        "constant", "superclass", "body_statement"
    ],
    "module": [
        "constant", "body_statement"
    ],
    "block": [
        "parameters", "body_statement"
    ],
    "do_block": [
        "parameters", "body_statement"
    ],
    "return": [
        "return_value"
    ],
    "break": [
        "arguments"
    ],
    "next": [
        "arguments"
    ],
}

BRACKET_TO_NODE_TYPES = {
    '{': [
        'block',
        'hash',
        'begin_block',
        'end_block',
        'singleton_class',
    ],
    '(': [
        'method_parameters',
        'parameter_list',
        'argument_list',
        'parenthesized_expression',
        'array',
    ],
    '[': [
        'array',
        'element_reference',
    ],
    'do': [
        'do_block',
        'method',
    ],
    'end': [
        'method', 'singleton_method', 'class', 'module',
        'if', 'unless', 'case', 'while', 'until', 'for',
        'begin', 'block', 'do_block', 'singleton_class'
    ]
}

NESTED_STRUCTURES = [
    "program",
    "body_statement",
    "method",
    "singleton_method",
    "class",
    "module",
    "singleton_class",
    "block",
    "do_block",
    "if",
    "unless",
    "case",
    "when",
    "while",
    "until",
    "for",
    "begin",
    "rescue",
    "ensure",
    "else",
    "begin_block",
    "end_block",
    "array",
    "hash",
    "parenthesized_expression",
    "call",
    "method_parameters",
    "parameter_list",
    "argument_list",
    "then",
    "assignment",
    "binary",
    "unary",
    "conditional",
    "range",
    "string",
    "xstring",
    "regexp",
    "symbol_array",
    "word_array"
]