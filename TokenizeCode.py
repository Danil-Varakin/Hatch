import re
from constants import TAB_DEPENDENT_LANGUAGES, NESTING_MARKERS, SPECIAL_OPERATORS_AND_NESTING_MARKERS_PATTERN, COMMENT_PATTERN, STRING_PATTERNS, CLOSE_TO_OPEN_NESTING_MARKERS
from Utilities import CheckBalancedMarkers
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
def FindFilteredCommentRanges(CodeString: str, language: str):
    CommentPattern = COMMENT_PATTERN[language.lower()]
    StringsPattern = STRING_PATTERNS[language.lower()]

    StringRanges = [(m.start(), m.end()) for m in re.finditer(StringsPattern, CodeString, re.DOTALL | re.MULTILINE)]

    FilteredCommentsList = []
    for m in re.finditer(CommentPattern, CodeString, re.DOTALL | re.MULTILINE):
        if not any(m.start() < StringEnd and StringStart < m.end() for StringStart, StringEnd in StringRanges):
            FilteredCommentsList.append((m.start(), m.end()))
    return FilteredCommentsList

@log_function(args=False, result=False)
def FindSpecialOperatorIndexes(CodeString: str, language: str, IsBalancedMarkers):
    FilteredCommentsList = FindFilteredCommentRanges(CodeString, language)
    OperatorIndexesList = []
    stack = []
    for m in re.finditer(SPECIAL_OPERATORS_AND_NESTING_MARKERS_PATTERN, CodeString):

        if any(CommentStart <=  m.start() < CommentEnd for CommentStart, CommentEnd in FilteredCommentsList):
            continue

        OperatorIndexesList.append(( m.start(), m.end()))
        if IsBalancedMarkers:
            if m.end() -  m.start() == 1:
                char = CodeString[ m.start()]
                if char in '{([':
                    stack.append(char)
                elif char in '})]':
                    if not stack or stack.pop() != CLOSE_TO_OPEN_NESTING_MARKERS[char]:
                        return None

    return OperatorIndexesList if not stack else None

@log_function(args=False, result=False)
def TokenizeWithSpecialOperators(CodeString: str, language: str, OperatorIndexesList: list):
    TokensList = []
    PositionInCodeString = 0
    for OperatorStart, OperatorEnd in OperatorIndexesList + [(len(CodeString), len(CodeString))]:
        if OperatorStart > PositionInCodeString:
            Token = TokenizeCode(CodeString[PositionInCodeString:OperatorStart], language.lower())
            if len(Token) > 0:
                TokensList.extend(Token)

        if OperatorStart < len(CodeString):
            if CodeString[OperatorStart] in NESTING_MARKERS:
                TokensList.append(CodeString[OperatorStart])
                PositionInCodeString = OperatorEnd
            else:
                TokensList.append(CodeString[OperatorStart:OperatorEnd])
                PositionInCodeString = OperatorEnd
    return TokensList


@log_function(args=False, result=False)
def RunTokenize(CodeString: str, language: str):
    try:
        if language in TAB_DEPENDENT_LANGUAGES:
            raise ValueError("Tab dependent language are not being processed yet")

        IsBalancedMarkers = CheckBalancedMarkers(CodeString)
        if not IsBalancedMarkers:
            logger.warning("The number of nesting markers does not match. When manually correcting, try not to use nesting markers")
        OperatorIndexesList  = FindSpecialOperatorIndexes(CodeString, language, IsBalancedMarkers)
        if OperatorIndexesList is None:
            raise ValueError("Error in tokenization of nesting markers")
        return TokenizeWithSpecialOperators(CodeString, language, OperatorIndexesList)
    except ValueError as e:
        logger.error(f"Logic error: {e}")
        return 0



