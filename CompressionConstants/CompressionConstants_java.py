
FUNCTION_NODE_TYPES = [
    'method_declaration',
    'constructor_declaration',
    'lambda_expression',
    'method_invocation',
    'object_creation_expression',
]

CONTROL_STRUCTURE_TYPES = [
    'if_statement',
    'while_statement',
    'for_statement',
    'enhanced_for_statement',
    'switch_expression',
    'switch_statement',
    'do_statement',
    'try_statement',
    'catch_clause',
    'finally_clause',
    'synchronized_statement',
    'ternary_expression',
]

BRACKET_STRUCTURE_TYPES = [
    'class_declaration',
    'interface_declaration',
    'enum_declaration',
    'record_declaration',
    'annotation_type_declaration',
    'try_statement',
    'synchronized_statement',
    'block',
    'static_initializer',
    'instance_initializer',
    'switch_block',
]

EXCLUDED_TYPES = {
    '{', '}', '(', ')', '[', ']',
    'identifier',
    'type_identifier',
    'formal_parameters',
    'parameter',
    'modifiers',
    'annotation',
    'dimensions',
}

DICTIONARY_SOLID_STRUCTURES = {
    "method_declaration": [
        "modifiers", "type_parameters", "formal_parameters",
        "block", "identifier", "type_identifier"
    ],
    "constructor_declaration": [
        "modifiers", "type_parameters", "formal_parameters",
        "constructor_body", "identifier"
    ],
    "lambda_expression": [
        "lambda_parameters", "block", "expression"
    ],
    "method_invocation": [
        "identifier", "argument_list", "type_arguments"
    ],
    "object_creation_expression": [
        "type_identifier", "argument_list", "type_arguments"
    ],
    "block": [
        "local_variable_declaration", "statement", "expression_statement"
    ],
    "if_statement": [
        "parenthesized_expression", "block", "statement",
        "else_statement", "if"
    ],
    "else_statement": [
        "block", "statement", "else"
    ],
    "for_statement": [
        "local_variable_declaration", "update", "condition",
        "statement", "block", "for"
    ],
    "enhanced_for_statement": [
        "variable_declarator", "iterable", "statement", "block"
    ],
    "while_statement": [
        "condition", "statement", "block", "while"
    ],
    "do_statement": [
        "statement", "block", "condition", "do", "while"
    ],
    "switch_statement": [
        "condition", "switch_block", "switch"
    ],
    "switch_expression": [
        "condition", "switch_block", "switch"
    ],
    "switch_block": [
        "switch_rule", "switch_label", "statement", "block"
    ],
    "try_statement": [
        "block", "catch_clause", "finally_clause", "resource_specification"
    ],
    "catch_clause": [
        "catch_formal_parameter", "block"
    ],
    "finally_clause": [
        "block"
    ],
    "synchronized_statement": [
        "parenthesized_expression", "block"
    ],
    "class_declaration": [
        "identifier", "type_parameters", "superclass",
        "super_interfaces", "class_body"
    ],
    "interface_declaration": [
        "identifier", "type_parameters", "super_interfaces", "interface_body"
    ],
    "enum_declaration": [
        "identifier", "super_interfaces", "enum_body"
    ],
    "record_declaration": [
        "identifier", "type_parameters", "formal_parameters",
        "super_interfaces", "record_body"
    ],
}

BRACKET_TO_NODE_TYPES = {
    '{': [
        'method_declaration',
        'constructor_declaration',
        'class_declaration',
        'interface_declaration',
        'enum_declaration',
        'record_declaration',
        'block',
        'static_initializer',
        'instance_initializer',
        'switch_block',
        'try_statement',
        'catch_clause',
        'finally_clause',
        'synchronized_statement',
    ],
    '(': [
        'formal_parameters',
        'argument_list',
        'parenthesized_expression',
        'cast_expression',
        'catch_formal_parameter',
        'resource_specification',
        'lambda_parameters',
    ],
    ')': [
    ],
    '[': [
        'array_type',
        'array_access',
        'array_creation_expression',
        'dimensions'
    ],
    '<': [
        'type_parameters',
        'type_arguments',
    ],
}

NESTED_STRUCTURES = [
    "block",
    "class_body",
    "interface_body",
    "enum_body",
    "record_body",
    "annotation_type_body",
    "constructor_body",
    "switch_block",
    "parenthesized_expression",
    "array_access",
    "array_creation_expression",
    "cast_expression",
    "method_invocation",
    "object_creation_expression",
    "lambda_expression",
    "ternary_expression",
    "binary_expression",
    "unary_expression",
    "update_expression",
    "assignment_expression",
    "formal_parameters",
    "argument_list",
    "type_arguments",
    "type_parameters",
    "local_variable_declaration",
    "resource_specification",
    "catch_formal_parameter",
    "enhanced_for_statement",
    "for_statement",
    "if_statement",
    "while_statement",
    "do_statement",
    "try_statement",
    "catch_clause",
    "finally_clause",
    "synchronized_statement",
    "switch_statement",
    "switch_expression",
    "switch_rule",
    "expression_statement",
    "return_statement",
    "throw_statement",
    "break_statement",
    "continue_statement",
    "yield_statement",
    "assert_statement",
]