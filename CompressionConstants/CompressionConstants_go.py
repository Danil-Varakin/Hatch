
FUNCTION_NODE_TYPES = [
    'function_declaration',
    'method_declaration',
    'method_spec',
    'call_expression',
]

CONTROL_STRUCTURE_TYPES = [
    'if_statement',
    'for_statement',
    'switch_statement',
    'select_statement',
    'type_switch_statement',
    'else_clause',
    'case_clause',
    'default_clause',
    'communication_case_clause',
]

BRACKET_STRUCTURE_TYPES = [
    'block',
    'struct_type',
    'interface_type',
    'type_declaration',
    'type_spec',
    'func_type',
    'composite_literal',
    'map_type',
    'slice_type',
    'array_type',
    'channel_type',
]

EXCLUDED_TYPES = {
    '{', '}', '(', ')', '[', ']',
    'identifier', 'package_identifier', 'field_identifier', 'type_identifier',
    'parameter_list', 'parameter_declaration',
    'field_declaration_list', 'field_declaration',
    'type_parameter_list',
}

DICTIONARY_SOLID_STRUCTURES = {
    "function_declaration": [
        "package_identifier", "identifier", "parameter_list",
        "parameter_declaration", "type", "block", "func"
    ],
    "method_declaration": [
        "receiver", "parameter_list", "identifier", "type",
        "pointer_type", "type_identifier", "block", "func"
    ],
    "call_expression": [
        "identifier", "field_expression", "selector_expression",
        "argument_list", "expression"
    ],
    "if_statement": [
        "if", "expression", "block", "else_clause", "short_variable_declaration"
    ],
    "else_clause": [
        "else", "block", "if_statement"
    ],
    "for_statement": [
        "for", "block", "expression", "range_clause", "init_statement",
        "update_statement", "short_variable_declaration"
    ],
    "range_clause": [
        "range", "expression", "left_hand_side", "short_variable_declaration"
    ],
    "switch_statement": [
        "switch", "expression", "block", "case_clause", "default_clause"
    ],
    "type_switch_statement": [
        "switch", "type", "short_variable_declaration", "expression"
    ],
    "select_statement": [
        "select", "block", "communication_case_clause"
    ],
    "case_clause": [
        "case", "expression_list", "statement_list", ":"
    ],
    "default_clause": [
        "default", "statement_list", ":"
    ],
    "communication_case_clause": [
        "case", "send_statement", "receive_statement", "statement_list", ":"
    ],
    "return_statement": [
        "return", "expression_list"
    ],
    "break_statement": [
        "break", "label"
    ],
    "continue_statement": [
        "continue", "label"
    ],
    "goto_statement": [
        "goto", "label"
    ],
    "fallthrough_statement": [
        "fallthrough"
    ],
    "block": [
        "statement", "declaration", "expression_statement", "short_variable_declaration"
    ],
    "composite_literal": [
        "literal_type", "literal_value", "keyed_element", "element"
    ],
    "literal_value": [
        "element_list", "keyed_element", "element"
    ],
    "struct_type": [
        "struct", "field_declaration_list", "field_declaration", "tag"
    ],
    "interface_type": [
        "interface", "method_spec", "type_name", "type_constraint"
    ],
    "type_declaration": [
        "type", "type_spec", "type_identifier", "type"
    ],
    "map_type": [
        "map", "type"
    ],
    "channel_type": [
        "chan", "direction", "type"
    ],
}

BRACKET_TO_NODE_TYPES = {
    '{': [
        'function_declaration', 'method_declaration',
        'if_statement', 'for_statement', 'switch_statement',
        'select_statement', 'type_switch_statement',
        'else_clause', 'case_clause', 'default_clause',
        'communication_case_clause',
        'block',
        'struct_type', 'interface_type',
        'composite_literal', 'literal_value',
        'func_type'
    ],
    '(': [
        'parameter_list',
        'argument_list',
        'type_parameter_list',
        'type_constraint',
        'expression',
        'call_expression',
        'conversion_expression',
        'type_assertion_expression'
    ],
    '[': [
        'array_type', 'slice_type',
        'index_expression', 'slice_expression',
        'composite_literal',
    ],
    ':': [
        'case_clause',
        'default_clause',
        'communication_case_clause',
        'keyed_element'
    ]
}

NESTED_STRUCTURES = [
    "block",
    "expression_statement",
    "declaration",
    "short_variable_declaration",
    "assignment_statement",
    "inc_dec_statement",
    "return_statement",
    "break_statement",
    "continue_statement",
    "goto_statement",
    "fallthrough_statement",
    "labeled_statement",
    "if_statement",
    "for_statement",
    "switch_statement",
    "select_statement",
    "type_switch_statement",
    "case_clause",
    "default_clause",
    "communication_case_clause",
    "else_clause",
    "parameter_list",
    "argument_list",
    "field_declaration_list",
    "element_list",
    "literal_value",
    "composite_literal",
    "struct_type",
    "interface_type",
    "func_type",
    "map_type",
    "channel_type",
    "slice_type",
    "array_type",
    "pointer_type",
    "type_conversion_expression",
    "type_assertion_expression",
    "call_expression",
    "index_expression",
    "slice_expression",
    "selector_expression",
    "unary_expression",
    "binary_expression",
    "parenthesized_expression",
    "type_parameter_list",
    "constraint_element",
    "type_constraint"
]