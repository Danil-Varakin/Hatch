import re
from constants import SPECIAL_OPERATORS, TAB_DEPENDENT_LANGUAGES, C_STYLE_LANGUAGES_COMMENT, SCRIPT_STYLE_LANGUAGES_COMMENT, NESTING_MARKERS, LANGUAGE_MAP, NESTING_CONTEXTS, EXTENSIONS_FILE
from Utilities import FindNthNOperators
from tree_sitter import Language, Parser
from typing import List

def TokenizeCode(CodeString: str, Language: str):
    if Language not in TAB_DEPENDENT_LANGUAGES:
       return CodeString.replace(" ", "").replace("\n", "").replace("\t", "")

    else:
        lines = CodeString.splitlines()
        ProcessedLines = []
        for line in lines:
            LeadingSpaces = len(line) - len(line.lstrip(' '))
            StrippedLine = line.strip()
            ProcessedLine = ' ' * LeadingSpaces + StrippedLine
            ProcessedLines.append(ProcessedLine)
        return ''.join(ProcessedLines)

def FindSpecialOperatorIndixes(CodeString: str, CommentPattern: str, Language: str):
    ReComments = [(m.start(), m.end()) for m in re.finditer(CommentPattern, CodeString, re.DOTALL | re.MULTILINE)]
    ReStrings = [(m.start(), m.end()) for m in re.finditer(r'"[^"\\]*(?:\\.[^"\\]*)*"|\'[^\'\\]*(?:\\.[^\'\\]*)*\'', CodeString, re.DOTALL)]
    patterns = r"(\.\.\.|>>>|<<<|\(|\)|\[|\]|\{|\}|\^\.\.|\$\.\.|\_\d*\.|i:\.)"
    if Language in TAB_DEPENDENT_LANGUAGES:
        patterns = r"(\.\.\.|>>>|<<<|\(|\)|\[|\]|\{|\}|\^\.\.|\$\.\.|\_\d*\.|i:\.| )"
    ReMatches = re.finditer(patterns, CodeString)
    OperatorIndexesList = []

    for ReMatch in ReMatches:
        ReOperatorStart = ReMatch.start()
        if not any(start <= ReOperatorStart < end for start, end in ReComments + ReStrings):
            OperatorIndexesList.append(ReOperatorStart)
    return OperatorIndexesList


def FindSpecialOperatorsWithLanguage(CodeString: str, language: str):
    CStyleCommentPattern = r"//.*?$|/\*.*?\*/"
    ScriptStyleCommentPattern = r"#.*?$|=begin.*?=end"
    if language in C_STYLE_LANGUAGES_COMMENT:
        return FindSpecialOperatorIndixes(CodeString, CStyleCommentPattern, language)
    elif language in SCRIPT_STYLE_LANGUAGES_COMMENT:
        return FindSpecialOperatorIndixes(CodeString, ScriptStyleCommentPattern, language)
    return None


def TokenizeWithSpecialOperators(CodeString: str, language: str, OperatorIndixesList: list):
    TokensList = []
    PositionInCodeString = 0
    for i in OperatorIndixesList + [len(CodeString)]:
        Token = CodeString[PositionInCodeString:i]
        if i > PositionInCodeString:
            Token = TokenizeCode(Token, language)
            if len(Token) > 0:
                TokensList.append(Token)
        if i < len(CodeString):
            NthNOperator = FindNthNOperators(CodeString, i)
            if CodeString[i: i + 3] in SPECIAL_OPERATORS:
                TokensList.append(CodeString[i : i + 3])
                PositionInCodeString = i + 3
            elif NthNOperator:
                TokensList.append(NthNOperator)
                PositionInCodeString = i + len(NthNOperator)
            elif CodeString[i] in NESTING_MARKERS:
                TokensList.append(CodeString[i])
                PositionInCodeString = i + 1
    return TokensList




def CheckAndRunTokenize(CodeString: str, language: str):
    OperatorIndixesList = FindSpecialOperatorsWithLanguage(CodeString, language)
    if not OperatorIndixesList:
        return TokenizeCode(CodeString, language)
    else:
        return TokenizeWithSpecialOperators(CodeString, language, OperatorIndixesList)

def find_nesting_brackets(language, code):
    if not language:
        raise ValueError(f"Не поддерживаемый язык: {language}. Поддерживаемые языки: {list(EXTENSIONS_FILE.keys())}")
    if language not in LANGUAGE_MAP or LANGUAGE_MAP[language] is None:
        return []

    language_obj = Language(LANGUAGE_MAP[language])
    parser = Parser(language=language_obj)
    tree = parser.parse(code.encode())
    root = tree.root_node
    positions: List[int] = []

    def traverse(node):
        if node.type in NESTING_CONTEXTS.get(language, []):
            for child in node.children:
                if child.type in ('<', '>'):
                    positions.append(child.start_byte)
                elif child.type in ('generic_type', 'type_identifier', 'preproc_arg'):
                    for sub_child in child.children:
                        if sub_child.type in ('<', '>'):
                            positions.append(sub_child.start_byte)
        for child in node.children:
            traverse(child)


    traverse(root)
    return sorted(positions)

