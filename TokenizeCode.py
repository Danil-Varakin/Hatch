import re

def TokenizeCode(CodeString: str, Language: str):
    if Language not in ["python", "yaml"]:
        return ''.join(CodeString.split())
    else:
        lines = CodeString.splitlines()
        ProcessedLines = []
        for line in lines:
            LeadingSpaces = len(line) - len(line.lstrip(' '))
            StrippedLine = line.strip().replace(' ', '')
            ProcessedLine = ' ' * LeadingSpaces + StrippedLine
            ProcessedLines.append(ProcessedLine)
        return ''.join(ProcessedLines)

def FindSpecialOperatorIndixes(CodeString: str, CommentPattern: str, Language: str):
    ReComments = [
        (m.start(), m.end())
        for m in re.finditer(CommentPattern, CodeString, re.DOTALL | re.MULTILINE)
    ]
    ReStrings = [
        (m.start(), m.end())
        for m in re.finditer(
            r'"[^"\\]*(?:\\.[^"\\]*)*"|\'[^\'\\]*(?:\\.[^\'\\]*)*\'',
            CodeString,
            re.DOTALL,
        )
    ]
    patterns = r"(\.\.\.|>>>|<<<|\(|\)|\[|\]|\{|\})"
    if Language in ["python", "yaml"]:
        patterns = r"(\.\.\.|>>>|<<<|\(|\)|\[|\]|\{|\}| )"
    ReMatches = re.finditer(patterns, CodeString)
    OperatorIndexesList = []

    for ReMatch in ReMatches:
        ReOperatorStart = ReMatch.start()
        if not any(
                start <= ReOperatorStart < end for start, end in ReComments + ReStrings
        ):
            OperatorIndexesList.append(ReOperatorStart)

    return OperatorIndexesList


def FindSpecialOperatorsWithLanguage(CodeString: str, language: str):
    CStyleLanguages = ["cpp", "js", "java", "typescript", "c", "c#", "rust", "go"]
    ScriptStyleLanguages = ["python", "ruby"]
    CStyleCommentPattern = r"//.*?$|/\*.*?\*/"
    ScriptStyleCommentPattern = r"#.*?$|=begin.*?=end"

    if language in CStyleLanguages:
        return FindSpecialOperatorIndixes(CodeString, CStyleCommentPattern, language)
    elif language in ScriptStyleLanguages:
        return FindSpecialOperatorIndixes(CodeString, ScriptStyleCommentPattern, language)


def TokenizeWithSpecialOperators(CodeString: str, language: str, OperatorIndixesList: list):
    TokensList = []
    PositionInCodeString = 0

    for i in OperatorIndixesList + [len(CodeString)]:
        if i > PositionInCodeString:
            TokensList.append(TokenizeCode(CodeString[PositionInCodeString:i], language))
        if i < len(CodeString):
            if CodeString[i: i + 3] in ["...", ">>>", "<<<"]:
                TokensList.append(CodeString[i : i + 3])
                PositionInCodeString = i + 3
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



