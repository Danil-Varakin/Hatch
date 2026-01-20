
FUNCTION_NODE_TYPES = [
    "method_declaration",
    "constructor_declaration",
    "destructor_declaration",
    "local_function_statement",
    "operator_declaration",
    "conversion_operator_declaration",
    "invocation_expression",
    "object_creation_expression",
]

CONTROL_STRUCTURE_TYPES = [
    "if_statement",
    "else_clause",
    "switch_statement",
    "switch_section",
    "case_switch_label",
    "default_switch_label",
    "while_statement",
    "do_statement",
    "for_statement",
    "foreach_statement",
    "try_statement",
    "catch_clause",
    "finally_clause",
    "using_statement",
    "lock_statement",
    "fixed_statement",
    "unsafe_statement",
    "checked_statement",
    "unchecked_statement",
    "yield_statement",
]

BRACKET_STRUCTURE_TYPES = [
    "class_declaration",
    "struct_declaration",
    "interface_declaration",
    "enum_declaration",
    "record_declaration",
    "namespace_declaration",
    "block",
    "catch_clause",
    "finally_clause",
    "accessor_declaration",
    "initializer_expression",
]

EXCLUDED_TYPES = {
    '{', '}', '(', ')', '[', ']',
    'identifier', 'global_identifier',
    'type_identifier', 'name',
    'parameter_list', 'parameter',
    'argument_list', 'argument',
    'modifier', 'predefined_type',
    'nullable_type', 'array_type',
    'qualified_name', 'alias_qualified_name',
}

DICTIONARY_SOLID_STRUCTURES = {
    "method_declaration": [
        "attribute_list", "modifier", "type", "identifier",
        "type_parameter_list", "parameter_list", "block", "arrow_expression_clause"
    ],
    "constructor_declaration": [
        "attribute_list", "modifier", "identifier", "parameter_list",
        "constructor_initializer", "block", "arrow_expression_clause"
    ],
    "invocation_expression": [
        "expression", "argument_list", "identifier", "member_access_expression"
    ],
    "object_creation_expression": [
        "object_creation_type", "argument_list", "initializer_expression"
    ],
    "if_statement": [
        "if_keyword", "parenthesized_expression", "statement", "else_clause"
    ],
    "else_clause": [
        "else_keyword", "statement"
    ],
    "switch_statement": [
        "switch_keyword", "parenthesized_expression", "switch_block", "switch_section"
    ],
    "switch_section": [
        "switch_label", "statements"
    ],
    "while_statement": [
        "while_keyword", "parenthesized_expression", "statement"
    ],
    "do_statement": [
        "do_keyword", "statement", "while_keyword", "parenthesized_expression"
    ],
    "for_statement": [
        "for_keyword", "for_initializer", "condition", "for_iterator", "statement"
    ],
    "foreach_statement": [
        "foreach_keyword", "type", "identifier", "in_keyword",
        "expression", "statement"
    ],
    "try_statement": [
        "try_keyword", "block", "catch_clause", "finally_clause"
    ],
    "catch_clause": [
        "catch_keyword", "catch_declaration", "catch_filter_clause", "block"
    ],
    "block": [
        "statement", "local_variable_declaration", "local_function_statement",
        "expression_statement", "return_statement", "yield_statement"
    ],
    "arrow_expression_clause": [
        "equals_greater_than_token", "expression"
    ],
    "class_declaration": [
        "attribute_list", "modifier", "class_keyword", "identifier",
        "type_parameter_list", "base_list", "type_parameter_constraint_clause",
        "class_body"
    ],
    "record_declaration": [
        "attribute_list", "modifier", "record_keyword", "identifier",
        "type_parameter_list", "parameter_list", "base_list", "record_body"
    ],
    "namespace_declaration": [
        "namespace_keyword", "qualified_name", "namespace_body", "semicolon"
    ],
    "using_statement": [
        "using_keyword", "parenthesized_expression", "statement"
    ],
    "yield_statement": [
        "yield_keyword", "return_keyword", "break_keyword", "expression"
    ]
}

BRACKET_TO_NODE_TYPES = {
    '{': [
        'block',
        'class_body',
        'struct_body',
        'interface_body',
        'enum_body',
        'namespace_body',
        'accessor_body',
        'record_body',
        'switch_block',
        'anonymous_object_creation_expression',
        'class_declaration',
        'struct_declaration',
        'interface_declaration',
        'record_declaration',
        'enum_declaration',
        'try_statement',
        'catch_clause',
        'finally_clause',
        'initializer_expression'
    ],
    '(': [
        'parenthesized_expression',
        'argument_list',
        'parameter_list',
        'invocation_expression',
        'object_creation_expression',
        'for_statement',
        'while_statement',
        'if_statement',
        'catch_declaration',
        'using_statement',
        'lock_statement',
        'fixed_statement',
        'checked_statement',
        'unchecked_statement'
    ],
    '[': [
        'array_type',
        'element_access_expression',
        'attribute_list',
        'implicit_array_creation_expression'
    ],
    ':': [
        'base_list',
        'type_parameter_constraint_clause',
        'case_switch_label'
    ]
}

NESTED_STRUCTURES = [
    "block",
    "class_body",
    "struct_body",
    "interface_body",
    "record_body",
    "namespace_body",
    "enum_body",
    "switch_block",
    "switch_section",
    "initializer_expression",
    "anonymous_object_creation_expression",
    "parenthesized_expression",
    "argument_list",
    "parameter_list",
    "attribute_list",
    "type_parameter_list",
    "base_list",
    "class_declaration",
    "struct_declaration",
    "interface_declaration",
    "record_declaration",
    "enum_declaration",
    "namespace_declaration",
    "method_declaration",
    "constructor_declaration",
    "local_function_statement",
    "if_statement",
    "else_clause",
    "try_statement",
    "catch_clause",
    "finally_clause",
    "switch_statement",
    "while_statement",
    "do_statement",
    "for_statement",
    "foreach_statement",
    "using_statement",
    "lock_statement",
    "fixed_statement"
]