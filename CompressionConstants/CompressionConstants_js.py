FUNCTION_NODE_TYPES = [
    "function_declaration",
    "generator_function_declaration",
    "function",
    "generator_function",
    "method_definition",
    "arrow_function",
    "call_expression",
    "new_expression",
    "await_expression",
]

CONTROL_STRUCTURE_TYPES = [
    "if_statement",
    "else_clause",
    "switch_statement",
    "case_clause",
    "default_clause",
    "while_statement",
    "do_statement",
    "for_statement",
    "for_in_statement",
    "for_of_statement",
    "try_statement",
    "catch_clause",
    "finally_clause",
    "throw_statement",
    "return_statement",
    "break_statement",
    "continue_statement",
    "debugger_statement",
]

BRACKET_STRUCTURE_TYPES = [
    "class_declaration",
    "class_body",
    "lexical_declaration",
    "variable_declaration",
    "object_pattern",
    "object_assignment_pattern",
    "object_type",
    "interface_declaration",
    "type_alias_declaration",
    "enum_declaration",
    "module",
    "program",
    "jsx_element",
    "jsx_fragment",
    "jsx_opening_element",
    "jsx_closing_element",
    "jsx_self_closing_element",
]

EXCLUDED_TYPES = {
    '{', '}', '(', ')', '[', ']', ';', ',',
    'identifier', 'property_identifier', 'shorthand_property_identifier',
    'shorthand_property_identifier_pattern',
    'type_identifier', 'jsx_identifier',
    'formal_parameters', 'parameters',
    'statement_block', 'parenthesized_expression',
}

DICTIONARY_SOLID_STRUCTURES = {
    "function_declaration": [
        "identifier", "formal_parameters", "statement_block",
        "generator_star", "async", "function"
    ],
    "generator_function_declaration": [
        "identifier", "formal_parameters", "statement_block",
        "generator_star", "function"
    ],
    "arrow_function": [
        "formal_parameters", "statement_block", "expression",
        "arrow", "async"
    ],
    "method_definition": [
        "property_name", "formal_parameters", "statement_block",
        "get", "set", "async", "generator_star", "static"
    ],
    "call_expression": [
        "identifier", "member_expression", "new", "arguments",
        "optional_chain", "template_string"
    ],
    "new_expression": [
        "new", "identifier", "member_expression", "arguments"
    ],
    "if_statement": [
        "parenthesized_expression", "statement", "else_clause",
        "if"
    ],
    "else_clause": [
        "else", "statement"
    ],
    "switch_statement": [
        "parenthesized_expression", "switch_body", "switch"
    ],
    "case_clause": [
        "expression", "statement_list"
    ],
    "for_statement": [
        "for", "parenthesized_expression", "statement",
        "variable_declaration", "expression", "assignment_expression"
    ],
    "for_of_statement": [
        "for", "of", "parenthesized_expression", "statement"
    ],
    "while_statement": [
        "parenthesized_expression", "statement", "while"
    ],
    "do_statement": [
        "statement", "parenthesized_expression", "do", "while"
    ],
    "try_statement": [
        "try", "statement_block", "catch_clause", "finally_clause"
    ],
    "catch_clause": [
        "catch", "formal_parameters", "statement_block"
    ],
    "finally_clause": [
        "finally", "statement_block"
    ],
    "class_declaration": [
        "class", "identifier", "class_heritage", "class_body"
    ],
    "class_body": [
        "method_definition", "field_definition", "public_field_definition",
        "getter_definition", "setter_definition"
    ],
    "jsx_element": [
        "jsx_opening_element", "jsx_closing_element", "jsx_text",
        "jsx_expression", "jsx_self_closing_element"
    ],
    "jsx_fragment": [
        "<", ">", "jsx_text", "jsx_expression"
    ],
    "object": [
        "pair", "shorthand_property_identifier", "spread_element",
        "object_pattern", "method_definition"
    ],
    "import_statement": [
        "import", "string", "identifier", "namespace_import",
        "named_imports", "default_import"
    ],
    "export_statement": [
        "export", "default", "declaration", "named_exports"
    ]
}

BRACKET_TO_NODE_TYPES = {
    '{': [
        "statement_block",
        "class_body",
        "object",
        "object_pattern",
        "switch_body",
        "lexical_declaration",
        "variable_declaration",
        "enum_declaration",
        "module",
        "jsx_expression",
    ],
    '(': [
        "formal_parameters",
        "arguments",
        "parenthesized_expression",
        "condition",
        "for_condition"
    ],
    '[': [
        "array",
        "array_pattern",
        "subscript_expression",
        "type_arguments"
    ],
    '<': [
        "jsx_opening_element",
        "jsx_self_closing_element",
        "type_arguments",
        "jsx_fragment"
    ],
    ':': [
        "case_clause",
        "default_clause",
        "pair"
    ]
}

NESTED_STRUCTURES = [
    "statement_block", "formal_parameters", "arguments", "parenthesized_expression",
    "object", "array", "call_expression", "new_expression", "member_expression",
    "jsx_element", "jsx_fragment", "jsx_opening_element", "jsx_expression",
    "arrow_function", "function", "generator_function", "class_body",
    "lexical_declaration", "variable_declaration", "for_statement",
    "for_of_statement", "for_in_statement", "if_statement", "switch_statement",
    "try_statement", "catch_clause", "finally_clause", "conditional_expression",
    "assignment_expression", "augmented_assignment_expression",
    "binary_expression", "unary_expression", "update_expression",
    "template_string", "template_substitution", "regex_pattern",
    "object_pattern", "array_pattern", "pair", "spread_element"
]