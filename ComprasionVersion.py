import tempfile
import re
import os
import subprocess
from tree_sitter import Point
from Utilities import ReadLine, ReadFile, ReadFileContents
from constants import FUNCTION_NODE_TYPES, CONTROL_STRUCTURE_TYPES, BRACKET_STRUCTURE_TYPES, CLOSE_NESTING_MARKERS, EXCLUDED_TYPES
from Logging import setup_logger, log_function
from tree_sitter_language_pack import get_language, get_parser


logger = setup_logger(log_file="CodeComprasion/my_app.log")

@log_function
def CompareFileContents(FileLines, PathFile):
    try:
        OldLines = FileLines["OldLines"]
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", delete=False) as TemporaryFile:
            TemporaryFile.writelines(OldLines)
            OldFilePath = TemporaryFile.name
        try:
            DiffOutput = subprocess.check_output([
                "git", "diff", "--word-diff", "--word-diff-regex=.*", "--ignore-all-space", "--no-index",
                OldFilePath, PathFile],
                text=True, encoding="utf-8")
        except subprocess.CalledProcessError as e:
            DiffOutput = e.output
        finally:
            os.unlink(OldFilePath)

        if not DiffOutput:
            logger.info(f"Нет различий в файле {PathFile} (или только пробелы)")
            return 0
        return DiffOutput

    except Exception as e:
        logger.error(f"Ошибка при сравнении файлов {PathFile}: {str(e)}")
        raise

@log_function
def FindStartEndPositionSubStringInStr(CodeString, SubString, LineNumber):
    try:
        if not SubString:
            raise ValueError("Подстрока не может быть пустой")

        CodeLines = CodeString.splitlines()
        if LineNumber < 1 or LineNumber > len(CodeLines):
            raise ValueError("Номер строки вне допустимого диапазона")

        StartIndex = 0
        for i in range(LineNumber - 1):
            StartIndex += len(CodeLines[i]) + 1
        while CodeLines[LineNumber - 1] == "":
            LineNumber += 1
        if CodeLines[LineNumber - 1].find(SubString) != -1:
            StartIndex += CodeLines[LineNumber - 1].find(SubString)
            EndIndex = StartIndex + len(SubString)
            return {"StartIndex": StartIndex, "EndIndex": EndIndex}
        else:
            raise ValueError("Подстрока не найдена в строке")

    except Exception as e:
        logger.error(f"Логическая ошибка: {str(e)}")
        return None

@log_function
def ParseDiffToTuples(DiffOutput, PathFile, MainBranch):
    try:
        result = []
        lines = DiffOutput.splitlines()
        LineNumberNewFile = 0
        LineNumberOldFile = 0
        InDiffBlock = False
        OldCode = ReadLastGitCommit(PathFile, MainBranch)
        NewCode = ReadFile(PathFile)
        for indexLineInDiff, line in enumerate(lines):
            if line.startswith("@@"):
                InDiffBlock = True
                match = re.search(r"@@ -(\d+),\d+ \+(\d+),\d+ @@", line)
                if match:
                    LineNumberOldFile = int(match.group(1)) - 1
                    LineNumberNewFile = int(match.group(2)) - 1
                continue

            if not InDiffBlock:
                continue
            if not (line.startswith('[-') and line.endswith('-]')):
                LineNumberNewFile += 1
            if not (line.startswith('{+') and line.endswith('+}')):
                LineNumberOldFile += 1

            IsFullDelete = line.startswith('[-') and line.endswith('-]')
            IsFullAdd = line.startswith('{+') and line.endswith('+}')

            if IsFullDelete:
                deleted = line[2:-2]
                IndexDict = FindStartEndPositionSubStringInStr(OldCode, deleted, LineNumberOldFile)
                result.append({'line': LineNumberOldFile, 'type': 'delete', 'start': IndexDict["StartIndex"], 'end': IndexDict["EndIndex"], 'added': '', 'deleted': deleted + "\n", "indexLineInDiff": indexLineInDiff})
                continue
            if IsFullAdd:
                added = line[2:-2]
                IndexDict = FindStartEndPositionSubStringInStr(NewCode, added, LineNumberNewFile)
                result.append({ 'line': LineNumberNewFile, 'type': 'add', 'start': IndexDict["StartIndex"], 'end': IndexDict["EndIndex"], 'added': added + "\n", 'deleted': '', "indexLineInDiff": indexLineInDiff})
                continue

            changes = []
            pattern = re.compile(r"\[-.*?-]|\{\+.*?\+\}", re.DOTALL)

            for match in pattern.finditer(line):
                ChangeStr = match.group(0)
                if ChangeStr.startswith('[-'):
                    deleted = ChangeStr[2:-2]
                    IndexDict = FindStartEndPositionSubStringInStr(OldCode, deleted, LineNumberOldFile)
                    changes.append({'line': LineNumberOldFile, 'type': 'delete', 'start': IndexDict["StartIndex"], 'end': IndexDict["EndIndex"], 'added': '', 'deleted': deleted + "\n", "indexLineInDiff": indexLineInDiff})
                else:
                    added = ChangeStr[2:-2]
                    IndexDict = FindStartEndPositionSubStringInStr(NewCode, added, LineNumberNewFile)
                    changes.append({'line': LineNumberNewFile, 'type': 'add', 'start': IndexDict["StartIndex"], 'end': IndexDict["EndIndex"],'added': added + "\n",'deleted': '', "indexLineInDiff": indexLineInDiff})
            result.extend(changes)

        MergedResult = []
        i = 0
        while i < len(result):
            EmptyLineRatio = 0
            current = result[i]
            j = i + 1
            while j < len(result) and result[j]['type'] == current['type'] and result[j]['line'] == current['line'] + (j - i + EmptyLineRatio) or  ( not lines[result[j-i + EmptyLineRatio]["indexLineInDiff"] + 1] or lines[result[j-i + EmptyLineRatio]["indexLineInDiff"] + 1].isspace() ) :
                if not lines[result[j - i + EmptyLineRatio]["indexLineInDiff"] + 1] or lines[result[j - i + EmptyLineRatio]["indexLineInDiff"] + 1].isspace():
                    EmptyLineRatio += 1

                if current['type'] == 'add':
                    current['added'] += result[j]['added']
                else:
                    current['deleted'] += result[j]['deleted']
                current['end'] = result[j]['end']
                j += 1
            MergedResult.append(current)
            i = j
        FinalResult = []
        i = 0
        while i < len(MergedResult):
            if i + 1 < len(MergedResult) and MergedResult[i]['type'] == 'delete' and MergedResult[i + 1]['type'] == 'add' and ComparisonLineIndex(i, MergedResult):
                FinalResult.append({'line': MergedResult[i+1]['line'], 'type': 'replace','start': MergedResult[i + 1]['start'],'end': MergedResult[i + 1]['end'], 'added': MergedResult[i + 1]['added'],'deleted': MergedResult[i]['deleted']})
                i += 2
            else:
                FinalResult.append(MergedResult[i])
                i += 1

        if not FinalResult:
            logger.warning("Не найдено изменений в diff-выводе")

        return FinalResult

    except Exception as e:
        logger.error(f"Ошибка при разборе diff: {str(e)}")
        raise
@log_function
def ComparisonLineIndex(indexInList, Changes):
    added_lines = 0
    deleted_lines = 0
    for i in range(indexInList):
        change = Changes[i]
        added_lines += change['added'].count('\n')
        deleted_lines += change['deleted'].count('\n')
    if  Changes[indexInList]['line'] - deleted_lines == Changes[indexInList + 1]['line'] - added_lines:
        return True
    else:
        return False

@log_function
def CompareFileVersions(PathFile, MainBranch="main"):
    try:
        FileLines = ReadFileContents(PathFile, MainBranch)
        DiffOutput = CompareFileContents(FileLines, PathFile)
        if DiffOutput == 0:
            return 0
        Changes = ParseDiffToTuples(DiffOutput, PathFile, MainBranch)
        return Changes
    except Exception as e:
        logger.error(f"Ошибка в CompareFileVersions: {str(e)}")
        raise



CPP_LANGUAGE = get_language('cpp')
parser = get_parser('cpp')

@log_function
def ReadLastGitCommit(PathFile, MainBranch):
    try:
        RepositoryPath = os.path.relpath(PathFile, start=os.getcwd()).replace(os.sep, "/")
        OldContent = subprocess.check_output(
            ["git", "show", f"{MainBranch}:{RepositoryPath}"],
            text=True,
            encoding="utf-8")
        GitCommitFileContent = OldContent
        return GitCommitFileContent
    except subprocess.CalledProcessError as e:
        logger.error(f"Ошибка при получении старой версии файла из ветки {MainBranch}: {str(e)}")
        raise


@log_function
def CoalesceEnclosingNodes(EnclosingNodes, root):
    changed = True
    while changed:
        changed = False
        ParentCandidates = {}
        for node in EnclosingNodes:
            parent = node.parent
            if parent and parent != root:
                ParentId = id(parent)
                if ParentId not in ParentCandidates:
                    ParentCandidates[ParentId] = parent
        for parent in list(ParentCandidates.values()):
            children = parent.children
            if not children:
                continue
            AllIn = all(child in EnclosingNodes for child in children)
            if AllIn:
                for child in children:
                    EnclosingNodes.remove(child)
                EnclosingNodes.append(parent)
                changed = True
    EnclosingNodes.sort(key=lambda n: n.start_point)
    return EnclosingNodes



@log_function
def SearchNodesWithChanges(file_path, change):
    try:
        action = change['type']
        ChangeStart = change['start']
        ChangeEnd = change["end"]
        EnclosingNodes = []
        if action == 'delete':
            CodeAnalyze = ReadLastGitCommit(file_path, MainBranch="development")
        else:
            CodeAnalyze = ReadFile(file_path)
        tree = parser.parse(CodeAnalyze.encode('utf-8'))
        if tree.root_node.type == 'ERROR':
            raise ValueError(f"Синтаксическая ошибка в файле {file_path}. AST содержит узел ERROR.")

        CurrentPos = ChangeStart
        while CurrentPos < ChangeEnd and CodeAnalyze[CurrentPos].isspace():
            CurrentPos += 1
        PrefixStart = CodeAnalyze[:CurrentPos+1]
        LinesStartList = PrefixStart.splitlines(keepends=True)
        StartLine = len(LinesStartList) - 1
        StartCol = len(LinesStartList[-1])-1 if LinesStartList else 0

        CurrentPositionEnd = ChangeEnd
        while CurrentPositionEnd >= ChangeStart and CodeAnalyze[CurrentPositionEnd].isspace():
            CurrentPositionEnd -= 1
        CurrentPositionEnd += 1
        PrefixEnd = CodeAnalyze[:CurrentPositionEnd+1]
        LinesEnd = PrefixEnd.splitlines(keepends=True)
        EndLine = len(LinesEnd) - 1
        EndCol = len(LinesEnd[-1]) if LinesEnd else 0

        StartPoint = Point(row=StartLine, column=StartCol)
        EndPoint = Point(row=EndLine, column=EndCol)
        @log_function
        def FindClosestEnclosingNodes(node, depth=0):
            if ContainsOrOverlapsRange(node, StartPoint, EndPoint):
                HasChildContainingRange = False
                for child in node.children:
                    if ContainsOrOverlapsRange(child, StartPoint, EndPoint):
                        HasChildContainingRange = True
                        FindClosestEnclosingNodes(child, depth + 1)
                if not HasChildContainingRange:
                    EnclosingNodes.append(node)
            else:
                for child in node.children:
                    FindClosestEnclosingNodes(child, depth + 1)
        FindClosestEnclosingNodes(tree.root_node)
        EnclosingNodes = CoalesceEnclosingNodes(EnclosingNodes, tree.root_node)
        if EnclosingNodes:
            return {"EnclosingNodes": EnclosingNodes, "action": action}, tree
        else:
            raise ValueError("Нет enclosing конструкций для изменений")

    except Exception as e:
        logger.error(f"Ошибка логики: {str(e)}")
        raise

@log_function
def ContainsOrOverlapsRange(node, StartPoint, EndPoint):
    NodeStartPoint = node.start_point
    NodeEndPoint = node.end_point
    NodeStart = (NodeStartPoint.row, NodeStartPoint.column)
    NodeEnd = (NodeEndPoint.row, NodeEndPoint.column)
    ChangeStart = (StartPoint.row, StartPoint.column)
    ChangeEnd = (EndPoint.row, EndPoint.column)
    return NodeStart < ChangeEnd and NodeEnd > ChangeStart

@log_function
def FindSiblingNodes(Nodes):
    if not Nodes:
        raise ValueError("Список Nodes пуст. Нет узлов для анализа.")
    FistNode = Nodes[0]
    LastNode = Nodes[-1]
    PrevForFirst = FistNode.prev_sibling
    NextForLast = LastNode.next_sibling
    FilteredSiblingsDict = {
        'PrevForFirst': PrevForFirst if IsIndependentNode(PrevForFirst) else None,
        'NextForLast': NextForLast if IsIndependentNode(NextForLast) else None}
    return FilteredSiblingsDict

@log_function
def IsIndependentNode(node):
    if node is None:
        return False
    if node.type not in EXCLUDED_TYPES:
        return True
    return False

@log_function
def FindNearestStructure(node, NODE_TYPES):
    NearestStructure = None
    CounterNesting = 0
    while node is not None:
        CounterNesting += 1
        if node.type in NODE_TYPES:
            NearestStructure = node
            break
        node = node.parent
    if node is None:
        CounterNesting = float('inf')
    return {"CounterNesting": CounterNesting, "NearestStructure": NearestStructure}

@log_function
def ProcessNodes(node, CodeLines):
    NodeType = node.type
    StartLine = node.start_point[0]
    EndLine = node.end_point[0]
    StartColumn = node.start_point[1]
    EndColumn = node.end_point[1]
    if StartLine == EndLine:
        NodeText = CodeLines[StartLine][StartColumn:EndColumn].strip()
    else:
        NodeText = CodeLines[StartLine][StartColumn:].strip()
        for i in range(StartLine + 1, EndLine):
            NodeText += "\n" + CodeLines[i].strip()
        NodeText += "\n" + CodeLines[EndLine][:EndColumn].strip()
    if NodeType in FUNCTION_NODE_TYPES:
        BraceIndex = NodeText.find('{')
        if BraceIndex != -1:
            return NodeText[:BraceIndex].strip() + " {}"
        return NodeText

    elif NodeType in CONTROL_STRUCTURE_TYPES:
        BraceIndex = NodeText.find('{')
        if BraceIndex != -1:
            return NodeText[:BraceIndex].strip() + " {}"
        ColonIndex = NodeText.find(':')
        if ColonIndex != -1:
            return NodeText[:ColonIndex + 1].strip()
        return NodeText.strip()

    elif NodeType in BRACKET_STRUCTURE_TYPES:
        BraceIndex = NodeText.find('{')
        if BraceIndex != -1:
            return NodeText[:BraceIndex].strip() + " {}"
        BracketIndex = NodeText.find('(')
        if BracketIndex != -1:
            BracketCount = 1
            i = BracketIndex + 1
            while i < len(NodeText) and BracketCount > 0:
                if NodeText[i] == '(':
                    BracketCount += 1
                elif NodeText[i] == ')':
                    BracketCount -= 1
                i += 1
            if BracketCount == 0:
                return NodeText[:i].strip() + " {}" if NodeType in ['compound_statement', 'try_statement', 'namespace_definition'] else NodeText[:i].strip()
        return NodeText.strip()
    return NodeText.strip()

@log_function
def FormatStructuresForMatchList(structs):
    result = []
    for struct in structs:
        LastBrace = ''
        for brace in CLOSE_NESTING_MARKERS:
            if struct.endswith(brace):
                LastBrace = brace
                break
        if LastBrace:
            formatted = f"... {struct[:-1]} ... {LastBrace} ..."
        else:
            formatted = f"... {struct} ..."
        result.append(formatted)
    return result

@log_function
def TransformStructsForMatch(structs):
    if len(structs) < 2:
        return structs[0]
    structs.reverse()
    for i in range(len(structs) - 1):
        structs[i] = (structs[i][:-10] + structs[i + 1] + " " + structs[i] [-5:])
    return structs[0]

@log_function
def AddInstruction(FilePath, MainBranch):
    Changes = CompareFileVersions(FilePath, MainBranch=MainBranch)
    for Change in Changes:
        SearchNodesWithChangesDict, tree = SearchNodesWithChanges(FilePath, Change)
        NodesWithChanges = SearchNodesWithChangesDict["EnclosingNodes"]
        action = SearchNodesWithChangesDict['action']
        CommonMatchList = []
        for NodesWithChange in NodesWithChanges:
            NearestStructureDictionary = FindNearestStructure(NodesWithChange, FUNCTION_NODE_TYPES)
            NestingLevelStruct = [NearestStructureDictionary["CounterNesting"]]
            NearestStructNode = [NearestStructureDictionary["NearestStructure"]]

            NearestStructureDictionary = FindNearestStructure(NodesWithChange, CONTROL_STRUCTURE_TYPES)
            NearestStructNode.append(NearestStructureDictionary["NearestStructure"])
            NestingLevelStruct.append(NearestStructureDictionary["CounterNesting"])

            NearestStructureDictionary = FindNearestStructure(NodesWithChange, BRACKET_STRUCTURE_TYPES)
            NearestStructNode.append(NearestStructureDictionary["NearestStructure"])
            NestingLevelStruct.append(NearestStructureDictionary["CounterNesting"])

            NearestStructs = list(zip(NestingLevelStruct, NearestStructNode))
            NearestStructs = sorted(NearestStructs, key=lambda x: x[0])
            MatchList = []
            for NearestStruct in NearestStructs:
                if NearestStruct[1] is not None:
                    MatchList.append(NearestStruct[1])
            if MatchList:
                CommonMatchList.append(MatchList)
        SiblingNodesDict = FindSiblingNodes(NodesWithChanges)

        FileContent = ReadLastGitCommit(FilePath, MainBranch)
        Result = GenerateMatch(NodesWithChanges, SiblingNodesDict, CommonMatchList, FileContent, action)
        print("result \n \n ", Result)

@log_function
def GenerateMatch(NodesWithChanges, siblings, NearestStructs, SourceCode, action):
    @log_function
    def GetNodeText(node):
        try:
            return SourceCode[node.start_byte:node.end_byte].strip()
        except Exception as e:
            raise ValueError(f"Не удалось извлечь текст узла на позициях {node.start_byte}:{node.end_byte}: {e}")

    @log_function
    def GetCommonParentContext(NearestStructsList):
        if not NearestStructsList:
            return None
        CommonParents = set(NearestStructsList[0])
        for parents in NearestStructsList[1:]:
            CommonParents.intersection_update(parents)
        return max(CommonParents, key=lambda x: x.start_point[0], default=None) if CommonParents else None
    try:
        if action == "add":
            raise ValueError(f"Вставка не поддерживается")
        result = []
        CommonParent = GetCommonParentContext(NearestStructs)
        if CommonParent:
            ParentText = GetNodeText(CommonParent).split('{')[0].strip()
            result.append(f"... {ParentText} {{...")

        PrevForFirst = siblings.get('PrevForFirst')
        if PrevForFirst:
            result.append(GetNodeText(PrevForFirst))
        result.append(">>>")
        for i, node in enumerate(NodesWithChanges):
            NodeText = GetNodeText(node)
            result.append(NodeText)
        result.append("<<<")

        NextForLast = siblings.get('NextForLast')
        if NextForLast:
            result.append(GetNodeText(NextForLast))
        if CommonParent:
            result.append("} ...")

        return " ".join(result)
    except Exception as e:
       logger.error(f"Logic error: {e}")