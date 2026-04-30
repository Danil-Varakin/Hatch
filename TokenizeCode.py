import re
from constants import SPECIAL_OPERATORS, TAB_DEPENDENT_LANGUAGES, NESTING_MARKERS, SPECIAL_OPERATORS_PATTERN, SPECIAL_OPERATORS_AND_NESTING_MARKERS_PATTERN, COMMENT_PATTERN, STRING_PATTERNS
from Utilities import FindNthNOperators, IntervalsIntersect
from Logging import setup_logger, log_function

logger = setup_logger()

@log_function(args=False, result=False)
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

@log_function(args=False, result=False)
def FindSpecialOperatorIndexes(CodeString: str,  language: str):
    CommentPattern = COMMENT_PATTERN[language.lower()]
    CommentsList = [(m.start(), m.end()) for m in re.finditer(CommentPattern, CodeString, re.DOTALL | re.MULTILINE)]
    StringsPattern =  STRING_PATTERNS[language.lower()]
    StringsList = [(m.start(), m.end()) for m in re.finditer(StringsPattern, CodeString, re.DOTALL | re.MULTILINE)]

    FilteredStringsList = sorted([interval for interval in StringsList if not any(IntervalsIntersect(interval, other) for other in CommentsList)])
    FilteredCommentsList = sorted([interval for interval in CommentsList if not any(IntervalsIntersect(interval, other) for other in FilteredStringsList)])

    ReMatches = re.finditer(SPECIAL_OPERATORS_AND_NESTING_MARKERS_PATTERN, CodeString)
    OperatorIndexesList = []
    for ReMatch in ReMatches:
        ReOperatorStart = ReMatch.start()
        if not any(start <= ReOperatorStart < end for start, end in FilteredCommentsList):
            OperatorIndexesList.append(ReOperatorStart)
    return OperatorIndexesList




@log_function(args=False, result=False)
def TokenizeWithSpecialOperators(CodeString: str, language: str, OperatorIndexesList: list):
    TokensList = []
    PositionInCodeString = 0
    OperatorIndexesList = sorted(set(OperatorIndexesList))
    for i in OperatorIndexesList + [len(CodeString)]:
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


@log_function(args=False, result=False)
def CheckAndRunTokenize(CodeString: str, language: str):
    try:
        if language in TAB_DEPENDENT_LANGUAGES:
            raise ValueError("Tab dependent language are not being processed yet")
        OperatorIndexesList  = FindSpecialOperatorIndexes(CodeString, language)
        return TokenizeWithSpecialOperators(CodeString, language, OperatorIndexesList)
    except ValueError as e:
        logger.error(f"Logic error: {e}")
        return 0



