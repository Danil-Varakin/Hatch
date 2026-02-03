FUNCTION_NODE_TYPES = [
    "function_declaration",
    "generator_function_declaration",
    "function",
    "generator_function",
    "method_definition",
    "arrow_function",
    "call_expression",
    "new_expression",
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
    "break_statement",
    "continue_statement",
    "return_statement",
    "debugger_statement",
]

BRACKET_STRUCTURE_TYPES = [
    "statement_block",
    "class_declaration",
    "class_heritage",
    "interface_declaration",
    "object_pattern",
    "object_type",
    "object",
    "enum_declaration",
    "lexical_declaration",
    "variable_declaration",
    "export_statement",
    "import_statement",
    "module",
    "type_alias_declaration",
    "interface_declaration",
    "enum_declaration",
    "module_dot_item",
    "internal_module",
]

EXCLUDED_TYPES = {
    "{", "}", "(", ")", "[", "]", ";", ",",
    "identifier", "property_identifier", "shorthand_property_identifier",
    "private_property_identifier",
    "type_identifier",
    "formal_parameters",
    "parameters",
    "type_annotation",
    "accessibility_modifier",
    "readonly",
    "optional",
    "required",
    "omit_pattern",
}

DICTIONARY_SOLID_STRUCTURES = {
    "function_declaration": [
        "identifier", "formal_parameters", "statement_block",
        "type_annotation", "accessibility_modifier"
    ],
    "generator_function_declaration": [
        "identifier", "formal_parameters", "statement_block",
        "type_annotation"
    ],
    "arrow_function": [
        "formal_parameters", "statement_block", "expression",
        "type_annotation", "return_type"
    ],
    "method_definition": [
        "property_name", "formal_parameters", "statement_block",
        "accessibility_modifier", "async", "get", "set", "static", "override"
    ],
    "call_expression": [
        "identifier", "member_expression", "arguments", "template_string",
        "optional_chain"
    ],
    "new_expression": [
        "identifier", "member_expression", "arguments"
    ],
    "if_statement": [
        "parenthesized_expression", "statement", "else_clause",
        "statement_block"
    ],
    "else_clause": [
        "statement", "statement_block"
    ],
    "switch_statement": [
        "parenthesized_expression", "statement_block",
        "case_clause", "default_clause"
    ],
    "case_clause": [
        "expression", "statements"
    ],
    "for_statement": [
        "parenthesized_expression", "statement", "statement_block",
        "variable_declaration", "expression"
    ],
    "for_of_statement": [
        "for", "of", "variable_declaration", "expression", "statement"
    ],
    "for_in_statement": [
        "for", "in", "variable_declaration", "expression", "statement"
    ],
    "while_statement": [
        "parenthesized_expression", "statement", "statement_block"
    ],
    "do_statement": [
        "statement", "parenthesized_expression"
    ],
    "try_statement": [
        "statement_block", "catch_clause", "finally_clause"
    ],
    "catch_clause": [
        "formal_parameters", "statement_block"
    ],
    "finally_clause": [
        "statement_block"
    ],
    "class_declaration": [
        "identifier", "class_heritage", "class_body",
        "type_annotation", "accessibility_modifier"
    ],
    "class_body": [
        "method_definition", "field_definition", "public_field_definition"
    ],
    "object": [
        "pair", "shorthand_property_identifier", "spread_element",
        "method_definition", "object_pattern"
    ],
    "object_pattern": [
        "shorthand_property_identifier_pattern", "pair_pattern",
        "object_assignment_pattern", "rest_pattern"
    ],
    "statement_block": [
        "statement", "expression_statement", "declaration"
    ],
    "lexical_declaration": [
        "variable_declarator"
    ],
    "type_alias_declaration": [
        "identifier", "type_annotation", "type_parameters"
    ],
    "interface_declaration": [
        "identifier", "interface_body", "extends_type_clause"
    ],
    "enum_declaration": [
        "identifier", "enum_body"
    ]
}

BRACKET_TO_NODE_TYPES = {
    "{": [
        "statement_block",
        "class_body",
        "enum_body",
        "object",
        "interface_body",
        "object_type",
        "object_pattern",
        "switch_body",
        "module",
        "export_statement"
    ],
    "(": [
        "formal_parameters",
        "parameters",
        "arguments",
        "parenthesized_expression",
        "condition_clause",
        "call_expression"
    ],
    "[": [
        "array",
        "array_pattern",
        "subscript_expression"
    ],
    "<": [
        "type_arguments",
        "type_parameters",
        "jsx_opening_element",
        "jsx_self_closing_element"
    ],
    "=>": [
        "arrow_function"
    ]
}

NESTED_STRUCTURES = [
    "statement_block", "class_body", "object", "array",
    "interface_body", "enum_body", "object_type", "object_pattern",
    "arguments", "formal_parameters", "parameters",
    "parenthesized_expression", "conditional_type", "union_type",
    "intersection_type", "type_literal", "tuple_type",
    "call_expression", "new_expression", "await_expression",
    "if_statement", "switch_statement", "for_statement",
    "while_statement", "do_statement", "try_statement",
    "arrow_function", "function", "generator_function",
    "jsx_element", "jsx_fragment", "jsx_expression",
    "template_string", "jsx_opening_element", "jsx_closing_element"
]