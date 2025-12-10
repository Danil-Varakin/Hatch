FUNCTION_NODE_TYPES = ['function_declaration', 'function_definition', 'method_declaration', "call_expression", "preproc_function_def"]

CONTROL_STRUCTURE_TYPES =  ['if_statement', 'while_statement', 'for_statement', 'switch_statement', 'case_statement', 'do_statement', 'try_statement', 'elif_clause', 'else_clause', 'goto_statement',  'preproc_if', 'preproc_elif', 'preproc_else', 'preproc_ifdef', 'preproc_elifdef']

BRACKET_STRUCTURE_TYPES = ['enum_specifier', 'class_specifier', 'struct_specifier', 'union_specifier', 'try_statement', 'namespace_definition', 'attribute_declaration', 'compound_literal_expression', 'generic_expression', "seh_try_statement", "seh_except_clause", "seh_finally_clause"]

EXCLUDED_TYPES = {
    '{', '}', '(', ')', 'identifier', 'parameter_list',
    'type_identifier', 'function_declarator', 'parameter',
    'type_qualifier', 'storage_class_specifier'}

DICTIONARY_SOLID_STRUCTURES = {
    "function_definition": [
        "compound_statement", "type_specifier", "type_identifier", "identifier",
        "statement", "expression", "primitive_type"
    ],
    "function_declaration": [
        "type_specifier", "function_declarator", "parameter_list", "identifier",
        "type_identifier", "storage_class_specifier", "type_qualifier"
    ],
    "method_declaration": [
        "type_specifier", "function_declarator", "parameter_list", "field_identifier",
        "type_identifier", "virtual", "override", "final", "const", "volatile"
    ],
    "lambda_expression": [
        "lambda_capture_specifier", "compound_statement", "parameter_list",
        "type_descriptor", "mutable", "exception_specification"
    ],
    "call_expression": [
        "function", "argument_list", "identifier", "field_expression",
        "template_function"
    ],
    "expression_statement": [
        "expression", "assignment_expression", "binary_expression", "unary_expression",
        "call_expression", "identifier", "number_literal", "string_literal"
    ],
    "if_statement": [
        "expression", "parenthesized_expression", "statement", "compound_statement",
        "else_clause", "if", "else"
    ],
    "elif_clause": [
        "else", "if", "expression", "parenthesized_expression", "statement", "compound_statement"
    ],
    "else_clause": [
        "else", "statement", "compound_statement"
    ],
    "for_statement": [
        "expression", "init_declarator", "statement", "compound_statement",
        "for", "assignment_expression", "update_expression"
    ],
    "while_statement": [
        "expression", "parenthesized_expression", "statement", "compound_statement",
        "while"
    ],
    "do_statement": [
        "statement", "compound_statement", "expression", "parenthesized_expression",
        "do", "while"
    ],
    "switch_statement": [
        "expression", "parenthesized_expression", "statement", "compound_statement",
        "case_statement", "switch", "case", "default"
    ],
    "case_statement": [
        "expression", "number_literal", "statement", "case", "default"
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
        "statement_identifier", "statement", "case", "default"
    ],
    "compound_statement": [
        "statement", "expression_statement"
    ],
    "try_statement": [
        "try", "compound_statement", "catch_clause", "handler_sequence"
    ],
    "namespace_definition": [
        "namespace", "name", "compound_statement", "identifier"
    ],
    "class_specifier": [
        "class", "struct", "union", "type_identifier", "base_class_clause",
        "field_declaration_list", "field_declaration", "access_specifier",
        "public", "private", "protected"
    ],
    "enum_specifier": [
        "type_identifier", "enumerator_list", "enumerator", "enum"
    ],
    "struct_specifier": [
        "type_identifier", "field_declaration_list", "field_declaration",
        "field_identifier", "struct"
    ],
    "union_specifier": [
        "type_identifier", "field_declaration_list", "field_declaration",
        "field_identifier", "union"
    ],
    "linkage_specification": [
        "extern", "string_literal", "function_definition"
    ],
    "attributed_statement": [
        "attribute_specifier", "attribute", "statement"
    ],
    "attribute_declaration": [
        "attribute_specifier", "attribute"
    ],
    "seh_try_statement": [
        "__try", "compound_statement", "seh_except_clause", "seh_finally_clause"
    ],
    "seh_except_clause": [
        "__except", "expression", "compound_statement"
    ],
    "seh_finally_clause": [
        "__finally", "compound_statement"
    ],
    "seh_leave_statement": [
        "__leave"
    ],
    "translation_unit": [
     "function_definition", "preproc_include", "preproc_def"
    ],
    "gnu_asm_expression": [
        "__asm", "__asm__", "string_literal", "gnu_asm_input_operand",
        "gnu_asm_output_operand", "gnu_asm_clobber_list", "gnu_asm_goto_list",
        "gnu_asm_qualifier"
    ],
    "alignof_expression": [
        "_alignof", "__alignof", "__alignof__", "type_identifier", "expression"
    ],
    "sizeof_expression": [
        "sizeof", "type_identifier", "expression"
    ],
    "offsetof_expression": [
        "offsetof", "type_identifier", "field_identifier"
    ],
    "cast_expression": [
        "type_descriptor", "expression"
    ],
    "compound_literal_expression": [
        "type_descriptor", "initializer_list"
    ],
    "generic_expression": [
        "_Generic", "expression", "type_descriptor"
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
        "type_specifier", "type_identifier", "_type_declarator", "typedef"
    ],
    "template_declaration": [
        "template", "template_parameter_list", "function_definition",
        "class", "typename", "concept"
    ],
    "concept_definition": [
        "concept", "type_identifier", "constraint_expression"
    ],
    "requires_expression": [
        "requires", "parameter_list", "requirement_body"
    ]
}

BRACKET_TO_NODE_TYPES = {
    '{': [
        'function_definition', 'method_declaration', 'lambda_expression',
        'if_statement', 'while_statement', 'for_statement', 'switch_statement',
        'do_statement', 'try_statement', 'elif_clause', 'else_clause',
        'enum_specifier', 'class_specifier', 'struct_specifier', 'union_specifier',
        'namespace_definition', 'attribute_declaration', 'compound_literal_expression',
        'seh_try_statement', 'seh_except_clause', 'seh_finally_clause',
        'preproc_function_def'
    ],
    '(': [
        'function_declaration', 'method_declaration', 'lambda_expression',
        'call_expression', 'if_statement', 'while_statement', 'for_statement',
        'switch_statement', 'preproc_if', 'preproc_elif', 'preproc_else',
        'preproc_ifdef', 'preproc_elifdef'
    ],
    '[': [
        'lambda_expression'
    ],
    '<': [
        'generic_expression'
    ]
}

NESTED_STRUCTURES = ["abstract_array_declarator", "abstract_function_declarator", "abstract_parenthesized_declarator", "abstract_pointer_declarator", "array_declarator", "attributed_declarator", "function_declarator", "parenthesized_declarator", "pointer_declarator", "alignof_expression", "assignment_expression", "binary_expression", "call_expression", "cast_expression", "char_literal","compound_literal_expression","concatenated_string","conditional_expression","extension_expression","field_expression","generic_expression","gnu_asm_expression","offsetof_expression","parenthesized_expression","pointer_expression","sizeof_expression","subscript_expression","unary_expression","update_expression","attributed_statement","case_statement","compound_statement","do_statement","expression_statement","for_statement","goto_statement","if_statement","labeled_statement","return_statement","seh_try_statement","switch_statement","while_statement","enum_specifier","macro_type_specifier","sized_type_specifier","struct_specifier","union_specifier","alignas_qualifier","argument_list","attribute","attribute_declaration","attribute_specifier","bitfield_clause","comma_expression","declaration","declaration_list","else_clause","enumerator","enumerator_list","field_declaration","field_declaration_list","field_designator","function_definition","gnu_asm_clobber_list","gnu_asm_goto_list","gnu_asm_input_operand","gnu_asm_input_operand_list","gnu_asm_output_operand","gnu_asm_output_operand_list","init_declarator","initializer_list","initializer_pair","linkage_specification","ms_based_modifier","ms_declspec_modifier","ms_pointer_modifier","offsetof_expression","parameter_declaration","parameter_list","preproc_call","preproc_def","preproc_defined","preproc_elif","preproc_elifdef","preproc_else","preproc_function_def","preproc_if","preproc_ifdef","preproc_include","preproc_params","seh_except_clause","seh_finally_clause","string_literal","subscript_designator","subscript_range_designator","translation_unit","type_definition","type_descriptor","type_qualifier","compound_statement" ,"initializer_list", "parenthesized_expression", "function_definition", "translation_unit" ]