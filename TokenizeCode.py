import re
from constants import SPECIAL_OPERATORS, TAB_DEPENDENT_LANGUAGES, NESTING_MARKERS, SPECIAL_OPERATORS_PATTERN, SPECIAL_OPERATORS_AND_NESTING_MARKERS_PATTERN, COMMENT_PATTERN
from Utilities import FindNthNOperators
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
    ReMatches = re.finditer(SPECIAL_OPERATORS_AND_NESTING_MARKERS_PATTERN, CodeString)
    OperatorIndexesList = []
    for ReMatch in ReMatches:
        ReOperatorStart = ReMatch.start()
        if not any(start <= ReOperatorStart < end for start, end in CommentsList):
            OperatorIndexesList.append(ReOperatorStart)
    IsSpecialOperatorsInCommentsList, SpecialOperatorIndexesList = IsSpecialOperatorsInComments(CodeString, CommentsList)
    return OperatorIndexesList, IsSpecialOperatorsInCommentsList, CommentsList, SpecialOperatorIndexesList

@log_function(args=False, result=False)
def IsSpecialOperatorsInComments(CodeString, CommentsList):
    ReSpecialOperators = re.finditer(SPECIAL_OPERATORS_PATTERN, CodeString)
    result = []
    SpecialOperatorIndexesList = []
    for match in ReSpecialOperators:
        OperatorStart = match.start()
        IsInComment = False
        for start, end in CommentsList:
            if start <= OperatorStart < end:
                IsInComment = True
                break
        result.append((OperatorStart, IsInComment))
        SpecialOperatorIndexesList.append(OperatorStart)
        SpecialOperatorIndexesList = sorted(SpecialOperatorIndexesList)
    return sorted(result, key=lambda x: x[0]), SpecialOperatorIndexesList


@log_function(args=False, result=False)
def TokenizeWithSpecialOperators(CodeString: str, language: str, OperatorIndexesList: list, IsSpecialOperatorsInCommentsList: list, CommentsList: list, SpecialOperatorIndexesList: list):
    TokensList = []
    PositionInCodeString = 0
    OperatorIndexesList = sorted(set(OperatorIndexesList + SpecialOperatorIndexesList))
    for i in OperatorIndexesList + [len(CodeString)]:
        SkipFlag = False
        if IsSpecialOperatorsInCommentsList:
            for idx, (CommentStart, CommentEnd) in enumerate(CommentsList):
                if CommentStart < i < CommentEnd:
                    if CodeString[i] not in NESTING_MARKERS:
                        break
                    else:
                        SkipFlag = True
                    break
        if SkipFlag:
            continue
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
        OperatorIndexesList, IsSpecialOperatorsInCommentsList, CommentsList, SpecialOperatorIndexesList = FindSpecialOperatorIndexes(CodeString, language)
        if not OperatorIndexesList:
            return TokenizeCode(CodeString, language)
        else:
            return TokenizeWithSpecialOperators(CodeString, language, OperatorIndexesList, IsSpecialOperatorsInCommentsList, CommentsList, SpecialOperatorIndexesList)
    except ValueError as e:
        logger.error(f"Logic error: {e}")
        return 0



