import re
from constants import SPECIAL_OPERATORS, TAB_DEPENDENT_LANGUAGES, C_STYLE_LANGUAGES_COMMENT, SCRIPT_STYLE_LANGUAGES_COMMENT, NESTING_MARKERS
from Utilities import FindNthNOperators


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
    OperatorIndixesList = sorted(OperatorIndixesList)

    for i in OperatorIndixesList + [len(CodeString)]:
        Token = CodeString[PositionInCodeString:i]
        if i > PositionInCodeString:
            Token = TokenizeCode(Token, language)
            if len(Token) > 0:
                TokensList.append(Token)

        if i < len(CodeString):
            NthNOperator = FindNthNOperators(CodeString, i)
            if NthNOperator:
                TokensList.append(NthNOperator)
                PositionInCodeString = i + len(NthNOperator)
            elif CodeString[i:i + 3] in SPECIAL_OPERATORS:
                TokensList.append(CodeString[i:i + 3])
                PositionInCodeString = i + 3
            elif CodeString[i] in NESTING_MARKERS:
                TokensList.append(CodeString[i])
                PositionInCodeString = i + 1
            else:
                TokensList.append(CodeString[i])
                PositionInCodeString = i + 1

    return TokensList



def CheckAndRunTokenize(CodeString: str, language: str):
    OperatorIndixesList = FindSpecialOperatorsWithLanguage(CodeString, language)
    if not OperatorIndixesList:
        return TokenizeCode(CodeString, language)
    else:
        return TokenizeWithSpecialOperators(CodeString, language, OperatorIndixesList)



