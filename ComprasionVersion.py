import os
import re
import tempfile

from tree_sitter import Point

from Insert import RunInsert
from SearchCode import UpdateUnpairedMarkers
from TokenizeCode import CheckAndRunTokenize
from Utilities import ReadFile, GetDiffOutput, ReadLastGitCommit
from constants import FUNCTION_NODE_TYPES_CPP, CONTROL_STRUCTURE_TYPES_CPP, BRACKET_STRUCTURE_TYPES_CPP, EXCLUDED_TYPES, DICTIONARY_SOLID_STRUCTURES_CPP
from Logging import setup_logger, log_function


logger = setup_logger(log_file="CodeComprasion/my_app.log")

@log_function
def CompareFileVersions(PathFile, OldCode):
    try:
        DiffOutput = GetDiffOutput(OldCode, PathFile)
        if not DiffOutput:
            raise ValueError('Нет изменений в файле')
        Change = ParseDiffToTuples(DiffOutput, PathFile, OldCode)
        if Change:
            return Change
        else:
            raise ValueError('Нет изменений в файле')
    except Exception as e:
        logger.error(f"Ошибка в CompareFileVersions: {str(e)}")
        return 0

@log_function
def ParseDiffToTuples(DiffOutput, PathFile, OldCode):
    try:
        result = []
        lines = DiffOutput.splitlines()
        LineNumberNewFile = 0
        LineNumberOldFile = 0
        InDiffBlock = False
        FirstBlockProcessed = False
        NewCode = ReadFile(PathFile)
        for indexLineInDiff, line in enumerate(lines):
            if line.startswith("@@"):
                if FirstBlockProcessed and result:
                    break
                FirstBlockProcessed = True
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

            change = []
            pattern = re.compile(r"\[-.*?-]|\{\+.*?\+}", re.DOTALL)

            for match in pattern.finditer(line):
                ChangeStr = match.group(0)
                if ChangeStr.startswith('[-'):
                    deleted = ChangeStr[2:-2]
                    IndexDict = FindStartEndPositionSubStringInStr(OldCode, deleted, LineNumberOldFile)
                    change.append({'line': LineNumberOldFile, 'type': 'delete', 'start': IndexDict["StartIndex"], 'end': IndexDict["EndIndex"], 'added': '', 'deleted': deleted + "\n", "indexLineInDiff": indexLineInDiff})
                else:
                    added = ChangeStr[2:-2]
                    IndexDict = FindStartEndPositionSubStringInStr(NewCode, added, LineNumberNewFile)
                    if change and change[-1]['type'] == 'add':
                        change.append({'line': LineNumberNewFile, 'type': 'add', 'start': change[-1]['start'], 'end': change[-1]['start'], 'added': added + "\n", 'deleted': '', "indexLineInDiff": indexLineInDiff})
                    else:
                        StartIndex = FindInsertStartIndexInOldCode(NewCode, OldCode, IndexDict['StartIndex'], LineNumberOldFile)
                        change.append({'line': LineNumberNewFile, 'type': 'add', 'start': StartIndex, 'end': StartIndex, 'added': added + "\n", 'deleted': '', "indexLineInDiff": indexLineInDiff})
            result.extend(change)
        if result:
            result = MakeReplace(MergesActionsSameType(result, lines))
            Change = result[0]
            return Change
        else:
            return 0
    except Exception as e:
        logger.error(f"Logic error: {str(e)}")
        return 0


@log_function
def FindInsertStartIndexInOldCode(NewCode, OldCode, StartIndexInNewCode, LineNumberOldFile):
    try:
        OldLines = OldCode.splitlines()

        if LineNumberOldFile < 1 or LineNumberOldFile > len(OldLines):
            raise ValueError("Номер строки выходит за пределы OldCode")

        PrefixNew = NewCode[:StartIndexInNewCode]

        StartIndexOld = 0
        for i in range(LineNumberOldFile - 1):
            StartIndexOld += len(OldLines[i]) + 1

        TargetLine = OldLines[LineNumberOldFile - 1]
        PrefixLines = PrefixNew.splitlines()
        if not PrefixLines:
            return StartIndexOld

        LastPrefixLine = PrefixLines[-1]
        if LastPrefixLine in TargetLine:
            LineOffset = TargetLine.rfind(LastPrefixLine)
            if LineOffset != -1:
                return StartIndexOld + LineOffset + len(LastPrefixLine)

        return StartIndexOld
    except Exception as e:
        logger.error(f"Logic error: {str(e)}")
        return 0


@log_function
def MergesActionsSameType(Change,CodeLines):
    try:
        result = []
        i = 0
        while i < len(Change):
            current = Change[i]
            j = i + 1
            Ratio = 0
            while j < len(Change) and Change[j]['type'] == current['type'] and Change[j]['line'] == current['line'] + j + Ratio:
                if current['type'] == 'add':
                    current['added'] += Change[j]['added']
                else:
                    current['deleted'] += Change[j]['deleted']
                current['end'] = Change[j]['end']
                if j < len(Change) and Change[j]['indexLineInDiff'] + Ratio + 1 < len(CodeLines):
                    line = CodeLines[Change[j]['indexLineInDiff']  + Ratio + 1]
                    while (line.isspace() or len(line) == 0) and Change[j]['indexLineInDiff'] + Ratio + 1 < len(CodeLines):
                        Ratio += 1
                        if j >= len(Change) or Change[j]['indexLineInDiff'] + Ratio + 1 >= len(CodeLines):
                            break
                        line = CodeLines[Change[j]['indexLineInDiff'] + Ratio + 1]
                j += 1
            result.append(current)
            i = j
        return result
    except Exception as e:
        logger.error(f"Logic error: {str(e)}")
        return 0

@log_function
def MakeReplace(Change):
    try:
        result = []
        i = 0
        while i < len(Change):
            if i + 1 < len(Change) and Change[i]['type'] == 'delete' and Change[i + 1]['type'] == 'add' and ComparisonLineIndex(i, Change):
                result.append({'line': Change[i + 1]['line'], 'type': 'replace', 'start': Change[i]['start'], 'end': Change[i]['end'], 'added': Change[i + 1]['added'], 'deleted': Change[i]['deleted']})
                i += 2
            else:
                result.append(Change[i])
                i += 1
        return result
    except Exception as e:
        logger.error(f"Logic error: {str(e)}")
        return 0

@log_function
def ComparisonLineIndex(indexInList, Changes):
    try:
        AddedLines = 0
        DeletedLines = 0
        for i in range(indexInList):
            change = Changes[i]
            AddedLines += change['added'].count('\n')
            DeletedLines += change['deleted'].count('\n')
        if  Changes[indexInList]['line'] - DeletedLines == Changes[indexInList + 1]['line'] - AddedLines:
            return True
        else:
            return False
    except Exception as e:
        logger.error(f"Logic error: {str(e)}")
        return 0

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
def SearchNodesWithChange(CodeAnalyze, change, parser):
    try:
        ChangeStart = change['start']
        ChangeEnd = change["end"]
        EnclosingNodes = []
        tree = GetASTTree(parser, CodeAnalyze)
        if not tree:
            raise ValueError(f"Синтаксическая ошибка в файле")
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
            return EnclosingNodes
        else:
            raise ValueError("Нет enclosing конструкций для изменений")

    except Exception as e:
        logger.error(f"Ошибка логики: {str(e)}")
        raise

@log_function
def CoalesceEnclosingNodes(EnclosingNodes, root):
    try:
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
    except Exception as e:
        logger.error(f"Logic error: {str(e)}")
        return 0

@log_function
def GetASTTree(parser, CodeString):
    try:
        tree = parser.parse(CodeString.encode('utf-8'))
        if tree.root_node.type == 'ERROR':
            raise ValueError(f"Синтаксическая ошибка в файле . AST содержит узел ERROR.")
        return tree
    except Exception as e:
        logger.error(f"Ошибка логики: {str(e)}")
        return 0

@log_function
def ContainsOrOverlapsRange(node, StartPoint, EndPoint):
    try:
        NodeStartPoint = node.start_point
        NodeEndPoint = node.end_point
        NodeStart = (NodeStartPoint.row, NodeStartPoint.column)
        NodeEnd = (NodeEndPoint.row, NodeEndPoint.column)
        ChangeStart = (StartPoint.row, StartPoint.column)
        ChangeEnd = (EndPoint.row, EndPoint.column)
        return NodeStart < ChangeEnd and NodeEnd > ChangeStart
    except Exception as e:
        logger.error(f"Logic error: {str(e)}")
        return 0

@log_function
def FindSiblingNodes(Nodes):
    try:
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
    except Exception as e:
        logger.error(f"Logic error: {str(e)}")
        return 0

@log_function
def IsIndependentNode(node):
    try:
        if node is None:
            return False
        if node.type not in EXCLUDED_TYPES:
            return True
        return False
    except Exception as e:
        logger.error(f"Logic error: {str(e)}")
        return 0

@log_function
def FindNearestStructure(node, NodeTypeS):
    try:
        NearestStructure = None
        CounterNesting = 0
        while node is not None:
            CounterNesting += 1
            if node.type in NodeTypeS:
                NearestStructure = node
                break
            node = node.parent
        if node is None:
            CounterNesting = float('inf')
        return {"CounterNesting": CounterNesting, "NearestStructure": NearestStructure}
    except Exception as e:
        logger.error(f"Logic error: {str(e)}")
        return 0

@log_function
def AddInstruction(FilePath, MainBranch, parser, language):
    try:
        Result = []
        NumberInsert = 0
        SourceCode = ReadLastGitCommit(FilePath, MainBranch)

        while GetDiffOutput(SourceCode, FilePath):
            Change = CompareFileVersions(FilePath, SourceCode)
            if not Change:
                raise ValueError("не найдено изменений")
            NodesWithChanges = SearchNodesWithChange(SourceCode, Change, parser)
            action = Change['type']
            CommonParentStructure = []
            for NodesWithChange in NodesWithChanges:
                NearestStructs = FindOldParentConstruction(NodesWithChange)
                ParentStructure = []
                for NearestStruct in NearestStructs:
                    if NearestStruct["Structure"] is not None:
                        ParentStructure.append(NearestStruct["Structure"])
                if ParentStructure:
                    CommonParentStructure.append(ParentStructure)
            SiblingNodesDict = FindSiblingNodes(NodesWithChanges)
            Match = GenerateMatch(NodesWithChanges, SiblingNodesDict, CommonParentStructure, SourceCode, action, language)
            if action == 'delete':
                patch = ''
            else:
                patch = Change["added"]

            SourceCode = VerificationInstruction(patch, Match, SourceCode, language, NumberInsert)
            if not SourceCode:
                raise ValueError('Match отработал не правильно')
            NumberInsert += 1
            Result.append(Match)
        return Result
    except Exception as e:
        logger.error(f"Ошибка логики: {str(e)}")
        return 0

@log_function
def VerificationInstruction(Patch, Match, SourceCode, Language, NumberInsert):
    TempFilePath = None
    try:
        with tempfile.NamedTemporaryFile(mode='w+t', delete=False) as temp_file:
            temp_file.write(SourceCode)
            temp_file.seek(0)
            TempFilePath = temp_file.name
            SourceCode = CheckAndRunTokenize(SourceCode, Language)
            Match = CheckAndRunTokenize(Match, Language)
            CompletionStatus = RunInsert(Match, Patch, SourceCode, TempFilePath, TempFilePath)
            if CompletionStatus == 1:
                logger.info(f"Match № {NumberInsert} successfully inserted")
                return ReadFile(TempFilePath)
            else:
                raise ValueError("The number of match and patch does not match")
    except ValueError as e:
        logger.error(f"Ошибка логики: {str(e)}")
        return 0
    except OSError as e:
        logger.error(f"Ошибка ввода-вывода: {str(e)}")
        return 0
    finally:
        if TempFilePath:
            try:
                os.unlink(TempFilePath)
                logger.debug(f"Файл удален: {TempFilePath}")
            except OSError as e:
                logger.error(f"Ошибка при удалении файла {TempFilePath}: {str(e)}")


@log_function
def FindOldParentConstruction(NodesWithChange):
    try:
        NearestStructureDictionary = FindNearestStructure(NodesWithChange, FUNCTION_NODE_TYPES_CPP)
        NestingLevelStruct = [NearestStructureDictionary["CounterNesting"]]
        NearestStructNode = [NearestStructureDictionary["NearestStructure"]]

        NearestStructureDictionary = FindNearestStructure(NodesWithChange, CONTROL_STRUCTURE_TYPES_CPP)
        NearestStructNode.append(NearestStructureDictionary["NearestStructure"])
        NestingLevelStruct.append(NearestStructureDictionary["CounterNesting"])

        NearestStructureDictionary = FindNearestStructure(NodesWithChange, BRACKET_STRUCTURE_TYPES_CPP)
        NearestStructNode.append(NearestStructureDictionary["NearestStructure"])
        NestingLevelStruct.append(NearestStructureDictionary["CounterNesting"])

        NearestStructs = [{"NestingLevel": level, "Structure": node}for level, node in zip(NestingLevelStruct, NearestStructNode)]
        NearestStructs = sorted(NearestStructs, key=lambda x: x["NestingLevel"])
        NearestStructs = [ struct for struct in NearestStructs if not (struct["NestingLevel"] == float('inf') and struct["Structure"] is None)]
        return NearestStructs
    except Exception as e:
        logger.error(f"Logic error: {str(e)}")
        return 0

@log_function
def GenerateMatch(NodesWithChanges, siblings, NearestStructs, SourceCode, action, language):
    try:
        CollectingMatchListDict = CollectingMatchList(NodesWithChanges, NearestStructs, siblings)
        MatchList = CollectingMatchListDict["SortedNodes"]
        ParentNodeList = CollectingMatchListDict["ParentNodeList"]
        ParentCloseIndexes = FindLastNodeInParent(MatchList, ParentNodeList, SourceCode)
        MatchString = ""
        ISAction = True if action == "add" else False
        ParentOpenIndex = {GetNodeText(ParentCloseIndex[2], SourceCode).split('{')[0].strip(): -1 for ParentCloseIndex in ParentCloseIndexes}

        for i, (node, NodeType) in enumerate(MatchList):

            NextNode, NextType = 0, 0
            if i + 1 < len(MatchList):
                NextNode, NextType = MatchList[i + 1]

            if NodeType == 'ParentNode':
                if len(MatchString) > 3 and  MatchString[-4: -1] != "..." or len(MatchString) < 3:
                    MatchString += " ... "
                MatchString += f"{ GetNodeText(node, SourceCode).split('{')[0].strip()} "
                MatchString += " { ... "

            elif NodeType == 'NodeWithChange':
                if i == 0:
                    MatchString += ' ... >>>'
                if not ISAction:
                    MatchString += f"{GetNodeText(node, SourceCode)} "
                IsNextExist = len(MatchList) > i + 1
                NextNode, NextType = MatchList[i + 1] if IsNextExist else None
                if IsNextExist and NextType in ["ParentNode", 'SiblingNode']  or not NextType:
                    if not ISAction:
                        MatchString += " <<< ... "
                    elif i > 0 and MatchList[i-1][1] != "SiblingNode":
                        MatchString += " ... "

            elif NodeType == 'SiblingNode':
                if len(MatchString) > 3 and  MatchString[-4: -1] != "..."  and i > 0 and  MatchList[i-1][1] != "NodeWithChange" or len(MatchString) < 3:
                    MatchString += " ... "
                MatchString += f"{GetNodeText(node, SourceCode)}"
                if NextNode and not NextType == "NodeWithChange" or not NextNode:
                    MatchString +=  " ... "

            if NextNode and NextType == "NodeWithChange" and NodeType != "NodeWithChange":
                if ISAction:
                    if len(MatchString) > 3 and  MatchString[-4: -1] != "..." and NodeType != "SiblingNode" or len(MatchString) < 3:
                        MatchString += f'{GetNodeText(NextNode, SourceCode)} ... >>> '
                    else:
                        MatchString += f" {GetNodeText(NextNode, SourceCode)}  >>> "
                else:
                    if len(MatchString) > 3 and  MatchString[-4: -1] != "..." and NodeType != "SiblingNode" or len(MatchString) < 3:
                        MatchString += f' ... >>> '
                    else:
                        MatchString += f"  >>> "

            for ParentCloseIndex in ParentCloseIndexes:
                if ParentCloseIndex[0] == i:
                    MatchStringTokenList = CheckAndRunTokenize(MatchString, language)
                    for j in range(len(MatchStringTokenList) - 1, -1, -1):
                        if MatchStringTokenList[j] == '{':
                            ParentOpenIndex[GetNodeText(ParentCloseIndex[2], SourceCode).split('{')[0].strip()] = j
                            break
        if ParentOpenIndex:
            MatchStringTokenList = CheckAndRunTokenize(MatchString, language)
            IsNestingMarkerPairsDictionary = UpdateUnpairedMarkers(MatchStringTokenList)
            ParentOpenIndexList = list(ParentOpenIndex.items())
            for i in range(len(ParentOpenIndexList)):
                if not IsNestingMarkerPairsDictionary[ParentOpenIndexList[i][1]][0]:
                    MatchString += " } ..."
        if len(MatchString) > 3 and MatchString[-4:-1] != "...":
            MatchString += " ..."
        return MatchString
    except Exception as e:
        logger.error(f"Logic error: {str(e)}")
        return 0


@log_function
def GetNodeText(node, SourceCode):
    try:
        return SourceCode[node.start_byte:node.end_byte]
    except Exception as expt:
        raise ValueError(f"Не удалось извлечь текст узла на позициях {node.start_byte}:{node.end_byte}: {expt}")

@log_function
def IsNodeWholeConstruction(ParentNode, ChildNode):
    if ParentNode.type not in DICTIONARY_SOLID_STRUCTURES_CPP:
        return True
    return ChildNode.type not in DICTIONARY_SOLID_STRUCTURES_CPP[ParentNode.type]

@log_function
def CollectingMatchList(NodesWithChanges, NearestStructs, siblings):
    try:
        NodePositions = {}
        BlockParent = []
        ParentNodeList = []
        for i, node in enumerate(NodesWithChanges):
            NodePositions[node] = (node.start_point[0], 'NodeWithChange')
            if len(NearestStructs) >= i + 1:
                for ParentNode in NearestStructs[i]:
                    if not IsNodeWholeConstruction(ParentNode, node):
                        BlockParent.append(ParentNode)
                    if ParentNode not in NodePositions and ParentNode not in BlockParent:
                        NodePositions[ParentNode] = (ParentNode.start_point[0], 'ParentNode')
                    if ParentNode not in ParentNodeList:
                        ParentNodeList.append(ParentNode)
        PrevForFirst = siblings.get('PrevForFirst')
        NextForLast = siblings.get('NextForLast')
        if PrevForFirst:
            NodePositions[PrevForFirst] = (PrevForFirst.start_point[0], 'SiblingNode')
        if NextForLast:
            NodePositions[NextForLast] = (NextForLast.start_point[0], 'SiblingNode')
    
        SortedNodes = sorted(
            [(node, NodeType) for node, (pos, NodeType) in NodePositions.items()],
            key=lambda x: NodePositions[x[0]][0]
        )
        return {"SortedNodes": SortedNodes,"ParentNodeList": ParentNodeList}
    except Exception as e:
        logger.error(f"Logic error: {str(e)}")
        return 0

@log_function
def FindLastNodeInParent(MatchNodeList, ParentList, SourceCode):
    try:
        ParentCloseIndex = {ParentNode: -1 for ParentNode in ParentList}
        IsFirstForNode = {ParentNode: True for ParentNode in ParentList}
        for i in range(len(MatchNodeList)):
            node, _ = MatchNodeList[i]
            for ParentNode in ParentList:
                if ParentNode.start_point[0] <= node.start_point[0] <= ParentNode.end_point[0]:
                    if IsFirstForNode[ParentNode] or GetNodeText(node, SourceCode) in GetNodeText(ParentNode, SourceCode).split('{')[0].strip():
                        if len(MatchNodeList) > i + 1:
                            NextNode, _= MatchNodeList[i+1]
                        else:
                            NextNode = 0
                        ParentCloseIndex[ParentNode] = (i, i)
                        IsFirstForNode[ParentNode] = False
                        if NextNode and GetNodeText(NextNode, SourceCode) == "{":
                            ParentCloseIndex[ParentNode] = (i+1, i)
                    else:
                        ParentCloseIndex[ParentNode] = (ParentCloseIndex[ParentNode][0], i)
        ParentCloseIndex = [(v1, v2, k) for k, (v1, v2) in ParentCloseIndex.items()]
        ParentCloseIndex = sorted(ParentCloseIndex, key=lambda x: x[2].start_point, reverse=True)
        return ParentCloseIndex
    except Exception as e:
        logger.error(f"Logic error: {str(e)}")
        return 0



@log_function
def CreateMarkdownInstructions(FilePath, Match, ComparisonResult):
    try:
        FileName = os.path.basename(FilePath)
        MdFileName = os.path.splitext(FileName)[0] + "_instructions.md"
        MdFilePath = os.path.join(os.getcwd(), MdFileName)

        with open(MdFilePath, 'w', encoding='utf-8') as MdFile:
            if isinstance(Match, str):
                Match = [Match]

            if isinstance(ComparisonResult, dict):
                ComparisonResult = [ComparisonResult]

            if not Match:
                raise ValueError("Список инструкций пуст")

            if len(Match) != len(ComparisonResult):
                while len(ComparisonResult) < len(Match):
                    ComparisonResult.append({'type': '', 'added': ''})

            for idx, (instruction, change) in enumerate(zip(Match, ComparisonResult)):
                MdFile.write(f"### match\n")
                MdFile.write(f"```\n{instruction}\n```\n")

                MdFile.write(f"### patch\n")

                action = change.get('type', '')
                if action == 'add':
                    content = change.get('added', '')
                elif action == 'delete':
                    content = ' '
                elif action == 'replace':
                    content = change.get('added', '')
                else:
                    content = ''

                MdFile.write(f"```\n{content}\n```\n\n")

        logger.info(f"Markdown файл успешно создан: {MdFilePath}")
        return True

    except Exception as e:
        logger.error(f"Ошибка при создании Markdown файла: {str(e)}")
        return False
