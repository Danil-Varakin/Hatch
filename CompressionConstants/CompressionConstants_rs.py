
FUNCTION_NODE_TYPES = [
    'function_item',
    'method_item',
    'impl_item',
    'trait_item',
    'macro_definition',
    'macro_invocation',
    'inner_attribute_item',
    'outer_attribute_item',
]

CONTROL_STRUCTURE_TYPES = [
    'if_expression',
    'else_clause',
    'match_expression',
    'while_expression',
    'for_expression',
    'loop_expression',
    'block_expression',
    'try_expression',
    'unsafe_block',
]

BRACKET_STRUCTURE_TYPES = [
    'mod_item',
    'struct_item',
    'enum_item',
    'union_item',
    'trait_item',
    'impl_item',
    'extern_crate_declaration',
    'extern_block',
    'tuple_type',
    'tuple_pattern',
    'tuple_expression',
    'array_expression',
    'array_type',
]

EXCLUDED_TYPES = {
    '{', '}', '(', ')', '[', ']',
    'identifier',
    'type_identifier',
    'field_identifier',
    'self',
    'super',
    'crate',
    'mod',
    'use_declaration',
    'use_wildcard',
    'use_as_clause',
    'visibility_modifier',
    'attribute',
    'inner_attribute',
    'outer_attribute',
    'lifetime',
    'type_parameter',
    'type_bound',
}

DICTIONARY_SOLID_STRUCTURES = {
    "function_item": [
        "function_modifiers", "identifier", "parameter_list",
        "type_identifier", "block", "where_clause", "return_type"
    ],
    "method_item": [
        "identifier", "parameter_list", "block",
        "self_parameter", "where_clause", "return_type"
    ],
    "impl_item": [
        "type_identifier", "generic_type", "trait", "for",
        "where_clause", "function_item", "method_item"
    ],
    "trait_item": [
        "identifier", "type_parameter", "where_clause",
        "function_item", "type_item", "const_item"
    ],
    "if_expression": [
        "if", "condition", "consequence", "else_clause",
        "block_expression", "else_if_clause"
    ],
    "else_clause": [
        "else", "block_expression", "if_expression"
    ],
    "match_expression": [
        "match", "condition", "match_block", "match_arm"
    ],
    "while_expression": [
        "while", "condition", "block_expression"
    ],
    "for_expression": [
        "for", "pattern", "in", "expression", "block_expression"
    ],
    "loop_expression": [
        "loop", "block_expression", "label"
    ],
    "block_expression": [
        "statement", "expression", "let_declaration"
    ],
    "struct_item": [
        "identifier", "field_declaration_list",
        "type_parameter", "where_clause"
    ],
    "enum_item": [
        "identifier", "type_parameter", "where_clause",
        "variant_list", "variant"
    ],
    "macro_invocation": [
        "identifier", "macro", "token_tree"
    ],
    "unsafe_block": [
        "unsafe", "block"
    ],
    "let_declaration": [
        "let", "pattern", "type_annotation", "initializer"
    ],
    "call_expression": [
        "identifier", "field_expression", "arguments"
    ],
    "return_expression": [
        "return", "expression"
    ],
    "break_expression": [
        "break", "label", "expression"
    ],
    "continue_expression": [
        "continue", "label"
    ],
}

BRACKET_TO_NODE_TYPES = {
    '{': [
        'function_item', 'method_item', 'impl_item', 'trait_item',
        'mod_item', 'unsafe_block', 'block_expression',
        'struct_item', 'enum_item', 'extern_block',
        'match_block', 'match_arm', 'variant_list',
        'field_declaration_list', 'token_tree'
    ],
    '(': [
        'parameter_list', 'arguments',
        'tuple_expression', 'tuple_pattern', 'tuple_type',
        'condition', 'parenthesized_expression'
    ],
    '[': [
        'array_expression', 'array_type',
        'slice_pattern', 'index_expression'
    ],
    '<': [
        'type_arguments', 'type_parameters',
        'where_clause', 'generic_type'
    ]
}

NESTED_STRUCTURES = [
    "block", "block_expression", "unsafe_block",
    "function_item", "method_item", "impl_item", "trait_item", "mod_item",
    "if_expression", "else_clause", "match_expression", "match_block", "match_arm",
    "while_expression", "for_expression", "loop_expression",
    "struct_item", "enum_item", "union_item", "variant_list",
    "tuple_expression", "array_expression",
    "call_expression", "field_expression",
    "let_declaration", "assignment_expression", "compound_assignment_expr",
    "binary_expression", "unary_expression", "update_expression",
    "parenthesized_expression", "tuple_expression", "array_expression",
    "return_expression", "break_expression", "continue_expression",
    "try_expression", "await_expression", "closure_expression",
    "generic_type", "scoped_type_identifier", "where_clause",
    "token_tree", "macro_definition", "macro_invocation"
]