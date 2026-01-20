import re
import tree_sitter
from Utilities import LoadLanguageModule
from Logging import setup_logger, log_function
from typing import Any, Optional, Dict, Tuple

logger = setup_logger()

@log_function(args=False, result=False)
def GetNextChar(row: int, col: int, lines: list) -> Tuple[Optional[str], int, int]:
    if row >= len(lines):
        return None, row, col
    line = lines[row]
    if col < len(line):
        return line[col], row, col + 1
    else:
        return '\n', row + 1, 0

@log_function(args=False, result=False)
def SkipWWhitespace(row: int, col: int, lines: list) -> Tuple[Optional[str], int, int]:
    while True:
        char, NextRow, NextCol = GetNextChar(row, col, lines)
        if char is None:
            return None, NextRow, NextCol
        if not char.isspace():
            return char, NextRow, NextCol
        row, col = NextRow, NextCol

@log_function(args=False, result=False)
def CompareFilesFromPoint(old_content: str, new_content: str, start_point: tree_sitter.Point = tree_sitter.Point(row=0, column=0)) -> Optional[tree_sitter.Point]:
    OldLines = old_content.split('\n')
    NewLines = new_content.split('\n')
    OldRow = start_point.row
    OldCol = start_point.column
    NewRow = start_point.row
    NewCol = start_point.column

    while True:
        OldChar, OldRow, OldCol = SkipWWhitespace(OldRow, OldCol, OldLines)
        NewChar, NewRow, NewCol = SkipWWhitespace(NewRow, NewCol, NewLines)
        if OldChar is None and NewChar is None:
            return None
        if OldChar != NewChar:
            if OldChar is not None:
                return tree_sitter.Point(row=OldRow, column=OldCol - 1)
            else:
                return tree_sitter.Point(row=OldRow, column=OldCol)

@log_function(args=False, result=False)
def GetChangeIndexes(DiffOutput: str) -> list[tuple[Any]]:
    ChangeLinesIndex = []
    try:
        changesBlockStarted = False
        lines = DiffOutput.splitlines()
        InDiffBlock = False
        OldLineNum = 0
        NewLineNum = 0
        for  line in lines:
            if line.startswith("@@"):
                if InDiffBlock and ChangeLinesIndex:
                    break
                InDiffBlock = True
                match = re.search(r'@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@', line)
                if match:
                    OldLineNum = int(match.group(1)) - 1
                    NewLineNum = int(match.group(3)) - 1
                continue

            if not InDiffBlock:
                continue
            if any(line.startswith(prefix) for prefix in ['diff --git', 'index ', '---', '+++', 'Binary files', '\\']):
                continue

            if line.startswith("-"):
                ChangeLinesIndex.append(({"OldLineIndex":OldLineNum, "NewLineIndex":NewLineNum-1},'del'))
                changesBlockStarted = True
                OldLineNum += 1
            elif line.startswith("+"):
                ChangeLinesIndex.append(({"OldLineIndex":OldLineNum-1, "NewLineIndex":NewLineNum},'add'))
                changesBlockStarted = True
                NewLineNum += 1
            else:
                if changesBlockStarted and ChangeLinesIndex:
                    break
                OldLineNum += 1
                NewLineNum += 1
        return ChangeLinesIndex
    except Exception as e:
        logger.error(f"Logic error: {str(e)}")
        return ChangeLinesIndex
@log_function(args=False, result=False)
def GetChange(ChangeLinesIndex: list[tuple[Any]], OldCode: str, NewCode: str) -> dict[str,Any]:
    try:
        Changes = []
        for (ChangeLineIndex, ChangeType) in ChangeLinesIndex:
            if ChangeType == 'del':
                NewLineIndex = ChangeLineIndex["NewLineIndex"]
                OldLineIndex = ChangeLineIndex["OldLineIndex"]
                ChangeLine = OldCode.splitlines(keepends=True)[OldLineIndex]
                if not ChangeLine.isspace():
                    ChangeLine = ChangeLine.replace('\n','')
                IndexDict = FindStartEndPositionSubStringInStr(OldCode, ChangeLine, OldLineIndex)
                Changes.append({ 'type': 'delete', 'start': IndexDict["StartIndex"], 'end': IndexDict["EndIndex"], 'added': '', 'deleted': ChangeLine, "NewLineIndex": NewLineIndex})
            else:
                NewLineIndex = ChangeLineIndex["NewLineIndex"]
                ChangeLine = NewCode.splitlines(keepends=True)[NewLineIndex]
                if Changes and Changes[-1]['type'] == "add":
                    Changes.append({ 'type': 'add', 'start': Changes[-1]['start'], 'end': Changes[-1]['end'], 'added': ChangeLine, 'deleted': '', "NewLineIndex": NewLineIndex})
                else:
                    OldLineIndex = ChangeLineIndex["OldLineIndex"]
                    LineBeforeChangeIndexDict = FindInsertStartIndexInOldCode(OldCode, OldLineIndex)
                    StartIndex = LineBeforeChangeIndexDict["LineBeforeChangeStartIndex"]
                    EndIndex = LineBeforeChangeIndexDict["LineBeforeChangeEndIndex"]
                    Changes.append({'type': 'add', 'start': StartIndex, 'end': EndIndex, 'added': ChangeLine,'deleted': '', "NewLineIndex": NewLineIndex})
        Changes = (MakeReplace(MergesActionsSameType(Changes)))
        if Changes:
            Change = Changes[0]
            return Change
        else:
            raise ValueError("Changes not found.")
    except Exception as e:
        logger.error(f"Logic error: {str(e)}")
        return {}

@log_function(args=False, result=False)
def FindInsertStartIndexInOldCode(OldCode: str, LineNumberOldFile: int) -> Dict[str, int]:
    try:
        OldCodeLines = OldCode.splitlines()
        StartIndexOldLine = 0
        for OldCodeLine in  OldCodeLines[:LineNumberOldFile]:
            StartIndexOldLine += len(OldCodeLine) + 1

        LineBeforeChangeEndIndex = StartIndexOldLine + len(OldCodeLines[LineNumberOldFile])
        i = 0
        while OldCode[StartIndexOldLine: LineBeforeChangeEndIndex + 1].isspace() or OldCode[StartIndexOldLine: LineBeforeChangeEndIndex + 1] =="":
            LineBeforeChangeEndIndex = StartIndexOldLine - len(OldCodeLines[LineNumberOldFile - i]) - 1
            StartIndexOldLine = LineBeforeChangeEndIndex -  len(OldCodeLines[LineNumberOldFile - i - 1])
            i += 1
        return {"LineBeforeChangeStartIndex": StartIndexOldLine, "LineBeforeChangeEndIndex":LineBeforeChangeEndIndex}

    except Exception as e:
        logger.error(f"Logic error: {str(e)}")
        return {}

@log_function(args=False, result=False)
def FindStartEndPositionSubStringInStr(CodeString: str, SubString: str, LineNumber: int) -> Optional[Dict[str, int]]:
    try:
        if not SubString:
            raise ValueError("A substring cannot be empty")

        CodeLines = CodeString.splitlines(keepends=True)
        if LineNumber < 0 or LineNumber > len(CodeLines):
            raise ValueError("The row number is out of the allowed range")

        StartIndex = 0
        for i in range(LineNumber):
            StartIndex += len(CodeLines[i])
        if len(CodeLines) - 1 == LineNumber:
            StartIndex -= 1

        while CodeLines[LineNumber] == "" and not SubString.isspace():
            LineNumber += 1
        StartStringIndex = CodeLines[LineNumber].find(SubString)
        if StartStringIndex != -1:
            StartIndex += StartStringIndex
            EndIndex = StartIndex + len(SubString)
            return {"StartIndex": StartIndex, "EndIndex": EndIndex}
        else:
            raise ValueError("The substring was not found in the string")
    except Exception as e:
        logger.error(f"Logic error: {str(e)}")
        return None

@log_function(args=False, result=False)
def MergesActionsSameType(Change: list[Dict[str, Any]]) -> list[dict[str,Any]]:
    try:
        result = []
        i = 0
        while i < len(Change):
            current = Change[i]
            j =  1
            while i+j < len(Change) and Change[i+j]['type'] == current['type']:
                if current['type'] == 'add':
                    current['added'] += Change[i+j]['added']
                else:
                    current['deleted'] += Change[i+j]['deleted']
                current['end'] = Change[i+j]['end']
                j += 1
            result.append(current)
            i = j + i
        return result
    except Exception as e:
        logger.error(f"Logic error: {str(e)}")
        return []

@log_function(args=False, result=False)
def MakeReplace(Change: list[Dict[str, Any]]) -> list[Dict[str, Any]]:
    try:
        result = []
        i = 0
        while i < len(Change):
            if i + 1 < len(Change) and Change[i]['type'] == 'delete' and Change[i + 1]['type'] == 'add':
                result.append({ 'type': 'replace', 'start': Change[i]['start'], 'end': Change[i]['end'], 'added': Change[i + 1]['added'], 'deleted': Change[i]['deleted'], "NewLineIndex": Change[i+1]["NewLineIndex"]})
                i += 2
            else:
                result.append(Change[i])
                i += 1
        return result
    except Exception as e:
        logger.error(f"Logic error: {str(e)}")
        return []

@log_function(args=False, result=False)
def UpdateChange(Change: Dict[str, Any], NodesWithChanges: list[Any], SourceCode: str, language: str) -> Dict[str, Any]:
    LanguageModule = LoadLanguageModule(language)
    NodeText = ""
    IsInsertInBegin = False
    ChangeType = Change["type"]
    for NodeWithChange in NodesWithChanges:
        NodeText += NodeWithChange.text.decode('utf-8')
    if ChangeType == "add":
        ChangeText = SourceCode[Change["start"]: Change["end"] + 1]
        if NodeText.find(ChangeText) == -1:
            return {"Change": Change, "IsInsertInBegin": IsInsertInBegin}
    else:
        ChangeText = Change["deleted"]
    if ''.join(NodeText.split()) != ''.join(ChangeText.split()):
        for NodeWithChange in NodesWithChanges:
            if NodeWithChange.type in LanguageModule.NESTED_STRUCTURES:
                IsInsertInBegin = True
                break
        if not IsInsertInBegin:
            ChangeTextIndex = NodeText.find(ChangeText)
            if  ChangeType == "delete":
                Change["added"] = NodeText[:ChangeTextIndex ]  + NodeText[ChangeTextIndex + len(ChangeText):]
                Change["deleted"] = NodeText
                Change["type"] = "replace"
            elif ChangeType == "add":
                Change["added"] = NodeText[:ChangeTextIndex ] + Change["added"] + NodeText[ChangeTextIndex + len(ChangeText):]
            elif ChangeType == "replace":
                Change["added"] = NodeText[:ChangeTextIndex] + Change["added"] + NodeText[ChangeTextIndex + len(ChangeText):]
                Change["deleted"] = NodeText
    return {"Change": Change, "IsInsertInBegin": IsInsertInBegin}


