import re
from constants import SPECIAL_OPERATORS, TAB_DEPENDENT_LANGUAGES, NESTING_MARKERS, RE_STRING_PATTERN, SPECIAL_OPERATORS_PATTERN, COMMENT_PATTERN
from Utilities import FindNthNOperators, FilteringListByOccurrence


def TokenizeCode(CodeString: str, Language: str):
    TokensList = []
    if Language not in TAB_DEPENDENT_LANGUAGES:
        Token = CodeString.replace(" ", "").replace("\n", "").replace("\t", "")
        if len(Token) > 0:
            TokensList.append(Token)
    else:
        lines = CodeString.splitlines()
        for line in lines:
            LeadingSpaces = len(line) - len(line.lstrip(' '))
            Token = line.replace(" ", "").replace("\n", "").replace("\t", "")
            Whitespace =  ' ' * LeadingSpaces
            if len(Token) > 0:
                TokensList.append(Token)
                if len(Whitespace) > 0:
                    TokensList.append(Whitespace)
    return TokensList

def FindSpecialOperatorIndixes(CodeString: str,  language: str):
    CommentPattern = COMMENT_PATTERN[language.lower()]
    ReComments = [(m.start(), m.end()) for m in re.finditer(CommentPattern, CodeString, re.DOTALL | re.MULTILINE)]
    ReStrings = [(m.start(), m.end()- 1) for m in re.finditer(RE_STRING_PATTERN, CodeString, re.DOTALL)]
    FilteredComments = FilteringListByOccurrence(ReComments, ReStrings)
    FilteredStrings =FilteringListByOccurrence(ReStrings, FilteredComments)
    ReMatches = re.finditer(SPECIAL_OPERATORS_PATTERN, CodeString)
    OperatorIndexesList = []
    for ReMatch in ReMatches:
        ReOperatorStart = ReMatch.start()
        if not any(start <= ReOperatorStart < end for start, end in FilteredComments + FilteredStrings):
            OperatorIndexesList.append(ReOperatorStart)
    return OperatorIndexesList

def TokenizeWithSpecialOperators(CodeString: str, language: str, OperatorIndixesList: list):
    TokensList = []
    PositionInCodeString = 0
    OperatorIndixesList = sorted(OperatorIndixesList)

    for i in OperatorIndixesList + [len(CodeString)]:
        Token = CodeString[PositionInCodeString:i]
        if i > PositionInCodeString:
            Token = TokenizeCode(Token, language.lower())
            if len(Token) > 0:
                TokensList.extend(Token)

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
    OperatorIndixesList = FindSpecialOperatorIndixes(CodeString, language)
    if not OperatorIndixesList:
        return TokenizeCode(CodeString, language)
    else:
        return TokenizeWithSpecialOperators(CodeString, language, OperatorIndixesList)



