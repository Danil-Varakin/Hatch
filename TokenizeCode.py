import re
from constants import SPECIAL_OPERATORS, TAB_DEPENDENT_LANGUAGES, NESTING_MARKERS, RE_STRING_PATTERN, SPECIAL_OPERATORS_PATTERN, SPECIAL_OPERATORS_AND_NESTING_MARKERS_PATTERN, COMMENT_PATTERN
from Utilities import FindNthNOperators, FilteringListByOccurrence
from Logging import setup_logger, log_function

logger = setup_logger(log_file='my_app.log')

@log_function
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

@log_function
def FindSpecialOperatorIndexes(CodeString: str,  language: str):
    CommentPattern = COMMENT_PATTERN[language.lower()]
    ReComments = [(m.start(), m.end()) for m in re.finditer(CommentPattern, CodeString, re.DOTALL | re.MULTILINE)]
    ReStrings = [(m.start(), m.end()- 1) for m in re.finditer(RE_STRING_PATTERN, CodeString, re.DOTALL)]
    FilteredComments = FilteringListByOccurrence(ReComments, ReStrings)
    FilteredStrings =FilteringListByOccurrence(ReStrings, FilteredComments)
    ReMatches = re.finditer(SPECIAL_OPERATORS_AND_NESTING_MARKERS_PATTERN, CodeString)
    OperatorIndexesList = []
    CommentsAndStringIndexList = FilteredComments + FilteredStrings
    for ReMatch in ReMatches:
        ReOperatorStart = ReMatch.start()
        if not any(start <= ReOperatorStart < end for start, end in FilteredComments + FilteredStrings):
            OperatorIndexesList.append(ReOperatorStart)
    IsSpecialOperatorsInCommentsOrStringList, SpecialOperatorIndexesList = IsSpecialOperatorsInCommentsOrString(CodeString, CommentsAndStringIndexList)
    return OperatorIndexesList, IsSpecialOperatorsInCommentsOrStringList, CommentsAndStringIndexList, SpecialOperatorIndexesList

@log_function
def IsSpecialOperatorsInCommentsOrString(CodeString, CommentsAndStringIndexList):
    ReSpecialOperators = re.finditer(SPECIAL_OPERATORS_PATTERN, CodeString)
    result = []
    SpecialOperatorIndexesList = []
    for match in ReSpecialOperators:
        OperatorStart = match.start()
        IsInCommentOrString = False
        for start, end in CommentsAndStringIndexList:
            if start <= OperatorStart < end:
                IsInCommentOrString = True
                break
        result.append((OperatorStart, IsInCommentOrString))
        SpecialOperatorIndexesList.append(OperatorStart)
        SpecialOperatorIndexesList = sorted(SpecialOperatorIndexesList)
    return sorted(result, key=lambda x: x[0]), SpecialOperatorIndexesList


@log_function
def TokenizeWithSpecialOperators(CodeString: str, language: str, OperatorIndexesList: list, IsSpecialOperatorsInCommentsOrStringList: list, CommentsAndStringIndexList: list, SpecialOperatorIndexesList: list):
    TokensList = []
    PositionInCodeString = 0
    OperatorIndexesList = sorted(set(OperatorIndexesList + SpecialOperatorIndexesList))
    for i in OperatorIndexesList + [len(CodeString)]:
        SkipFlag = False
        if IsSpecialOperatorsInCommentsOrStringList:
            for idx, (CommentOrStringStart, CommentOrStringEnd) in enumerate(CommentsAndStringIndexList):
                if CommentOrStringStart < i < CommentOrStringEnd:
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


@log_function
def CheckAndRunTokenize(CodeString: str, language: str):
    try:
        if language in TAB_DEPENDENT_LANGUAGES:
            raise ValueError("Tab dependent language are not being processed yet")
        OperatorIndexesList, IsSpecialOperatorsInCommentsOrStringList, CommentsAndStringIndexList, SpecialOperatorIndexesList = FindSpecialOperatorIndexes(CodeString, language)
        if not OperatorIndexesList:
            return TokenizeCode(CodeString, language)
        else:
            return TokenizeWithSpecialOperators(CodeString, language, OperatorIndexesList, IsSpecialOperatorsInCommentsOrStringList, CommentsAndStringIndexList, SpecialOperatorIndexesList)
    except ValueError as e:
        logger.error(f"Logic error: {e}")
        return 0



