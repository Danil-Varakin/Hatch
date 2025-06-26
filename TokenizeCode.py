from pygments import lex
from pygments.lexers import get_lexer_by_name
from pygments.token import Token
import re

def TokenizeCode(CodeString: str, language: str):
        lexer = get_lexer_by_name(language)
        tokens = list(lex(CodeString, lexer))
        return tokens

def FindSpecialOperatorIndixes(CodeString: str, CommentPattern: str) :
    ReComments = [(m.start(), m.end()) for m in re.finditer(CommentPattern, CodeString, re.DOTALL | re.MULTILINE)]
    ReStrings = [(m.start(), m.end()) for m in re.finditer(r'"[^"\\]*(?:\\.[^"\\]*)*"|\'[^\'\\]*(?:\\.[^\'\\]*)*\'', CodeString, re.DOTALL)]
    ReMatches = re.finditer(r'(\.\.\.|>>>|<<<)', CodeString)
    OperatorIndixesList = []

    for ReMatch in ReMatches:
        ReOperatorStart = ReMatch.start()
        if not any(start <= ReOperatorStart < end for start, end in ReComments + ReStrings):
            OperatorIndixesList.append(ReOperatorStart)

    return OperatorIndixesList

def FindSpecialOperatorsWithLanguage(CodeString: str, language: str) :

    CStyleLanguages = ['cpp', 'js', 'java', 'typescript', 'c', 'c#', 'rust', 'go']
    ScriptStyleLanguages = ['python', 'ruby']
    CStyleCommentPattern = r'//.*?$|/\*.*?\*/'
    ScriptStyleCommentPattern = r'#.*?$|=begin.*?=end'

    if language in CStyleLanguages:
        return FindSpecialOperatorIndixes(CodeString, CStyleCommentPattern)
    elif language in ScriptStyleLanguages:
        return FindSpecialOperatorIndixes(CodeString, ScriptStyleCommentPattern)


def TokenizeWithSpecialOperators(CodeString: str, language: str,OperatorIndixesList: list) :
    TokensList = []
    PositionInCodeString = 0

    for i in OperatorIndixesList + [len(CodeString)]:
        if i > PositionInCodeString:
            TokensList.extend(TokenizeCode(CodeString[PositionInCodeString:i], language))
        if i < len(CodeString):
            TokensList.append((Token.Operator, CodeString[i:i + 3]))
        PositionInCodeString = i + 3
    return TokensList

def CheckAndRunTokenize(CodeString: str,language: str):
    OperatorIndixesList = FindSpecialOperatorsWithLanguage(CodeString,language)
    if not OperatorIndixesList:
        return RemoveInsignificantTokens(TokenizeCode(CodeString, language), language)
    else:
        return RemoveInsignificantTokens(TokenizeWithSpecialOperators(CodeString, language, OperatorIndixesList), language)

def RemoveInsignificantTokens(TokensList: list[tuple], language: str):
    FilteredTokenList = []
    IsTabulation = True
    for TokenType, TokenValue in TokensList:
        IsWhitespace = bool(re.match(r'^[ \n]*$', TokenValue))

        if language in ['python', 'yaml']:
            if IsWhitespace:
                if IsTabulation:
                    FilteredTokenList.append((TokenType, TokenValue))
                elif '\n' in TokenValue:
                    IsTabulation = True
            else:
                FilteredTokenList.append((TokenType, TokenValue))
                IsTabulation = False
        else:
            if not IsWhitespace:
                FilteredTokenList.append((TokenType, TokenValue))
    return FilteredTokenList