import os
import re
import tempfile
import importlib
from tree_sitter import Point
from Insert import RunInsert
from SearchCode import UpdateUnpairedMarkers
from TokenizeCode import CheckAndRunTokenize
from Utilities import ReadFile, GetDiffOutput, ReadLastGitCommit
from constants import OPEN_NESTING_MARKERS
from Logging import setup_logger, log_function


logger = setup_logger()

@log_function(args=False, result=False)
def LoadLanguageModule(language):
    ModuleName = f'CompressionConstants_{language}'
    try:
        return importlib.import_module(ModuleName)
    except ModuleNotFoundError:
        raise ValueError(f'The module for the {language} language was not found. Check the {ModuleName}.py file')
    except Exception as e:
        raise RuntimeError(f'Error loading the module for {language}: {e}')

@log_function(args=False, result=False)
def CompareFileVersions(PathFile, OldCode):
    try:
        DiffOutput = GetDiffOutput(OldCode, PathFile)
        if not DiffOutput:
            raise ValueError('No changes in the file')
        Change = ParseDiffToTuples(DiffOutput, OldCode)
        if Change:
            return Change
        else:
            raise ValueError('No changes in the file')
    except Exception as e:
        logger.error(f"Error in CompareFileVersions: {str(e)}")
        return 0

@log_function(args=False, result=False)
def ParseDiffToTuples(DiffOutput, OldCode):
    try:
        result = []
        lines = DiffOutput.splitlines()
        LineNumberNewFile = 0
        LineNumberOldFile = 0
        InDiffBlock = False
        FirstBlockProcessed = False
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
                    if line.startswith('{+') and line.endswith("+}"):
                        added = "\n" + added
                    if change and change[-1]['type'] == "add":
                        change.append({'line': LineNumberNewFile, 'type': 'add', 'start': change[-1]['start'], 'end': change[-1]['end'], 'added': added + "\n", 'deleted': '', "indexLineInDiff": indexLineInDiff})
                    else:
                        if not change and result and result[-1]["indexLineInDiff"] == indexLineInDiff - 1 and result[-1]["type"] == "add":
                            change.append({'line': LineNumberNewFile, 'type': 'add', 'start': result[-1]['start'], 'end': result[-1]['end'], 'added': added + "\n", 'deleted': '', "indexLineInDiff": indexLineInDiff})
                        else:
                            IndexStartChange = line.find(ChangeStr) - 1
                            LineBeforeChangeIndexDict = FindInsertStartIndexInOldCode(OldCode, LineNumberOldFile - 1, IndexStartChange)
                            StartIndex = LineBeforeChangeIndexDict["LineBeforeChangeStartIndex"]
                            EndIndex = LineBeforeChangeIndexDict["LineBeforeChangeEndIndex"]
                            change.append({'line': LineNumberNewFile, 'type': 'add', 'start': StartIndex, 'end': EndIndex, 'added': added + "\n", 'deleted': '', "indexLineInDiff": indexLineInDiff})
            result.extend(change)
        if result:
            result = MakeReplace(MergesActionsSameType(result, lines))
            Change = result[0]
            return Change
        else:
            return []
    except Exception as e:
        logger.error(f"Logic error: {str(e)}")
        return []


@log_function(args=False, result=False)
def FindInsertStartIndexInOldCode(OldCode, LineNumberOldFile, IndexStartChangeInDiff):
    try:
        OldCodeLines = OldCode.splitlines()
        StartIndexOldLine = 0
        for OldCodeLine in  OldCodeLines[:LineNumberOldFile]:
            StartIndexOldLine += len(OldCodeLine) + 1
        if IndexStartChangeInDiff <= 0:
            LineBeforeChangeEndIndex = StartIndexOldLine + len(OldCodeLines[LineNumberOldFile])
        else:
            LineBeforeChangeEndIndex = StartIndexOldLine + IndexStartChangeInDiff + 1

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
def MergesActionsSameType(Change,CodeLines):
    try:
        result = []
        i = 0
        while i < len(Change):
            current = Change[i]
            j =  1
            Ratio = 0
            while i+j < len(Change) and Change[i+j]['type'] == current['type'] and Change[i+j]['line'] == current['line'] + j + Ratio:
                if current['type'] == 'add':
                    current['added'] += Change[i+j]['added']
                else:
                    current['deleted'] += Change[i+j]['deleted']
                current['end'] = Change[i+j]['end']
                current['indexLineInDiff'] = Change[i+j]['indexLineInDiff']
                if i+j < len(Change) and Change[i+j]['indexLineInDiff'] + Ratio + 1 < len(CodeLines):
                    line = CodeLines[Change[i+j]['indexLineInDiff']  + Ratio + 1]
                    while (line.isspace() or len(line) == 0) and Change[i+j]['indexLineInDiff'] + Ratio + 1 < len(CodeLines):
                        Ratio += 1
                        if i+j >= len(Change) or Change[i+j]['indexLineInDiff'] + Ratio + 1 >= len(CodeLines):
                            break
                        line = CodeLines[Change[i+j]['indexLineInDiff'] + Ratio + 1]
                j += 1
            result.append(current)
            i = j + i
        return result
    except Exception as e:
        logger.error(f"Logic error: {str(e)}")
        return 0

@log_function(args=False, result=False)
def MakeReplace(Change):
    try:
        result = []
        i = 0
        while i < len(Change):
            if i + 1 < len(Change) and Change[i]['type'] == 'delete' and Change[i + 1]['type'] == 'add'   and 0 <= Change[i]['indexLineInDiff'] -  Change[i + 1]['indexLineInDiff'] <=1:
                result.append({'line': Change[i + 1]['line'], 'type': 'replace', 'start': Change[i]['start'], 'end': Change[i]['end'], 'added': Change[i + 1]['added'], 'deleted': Change[i]['deleted']})
                i += 2
            else:
                result.append(Change[i])
                i += 1
        return result
    except Exception as e:
        logger.error(f"Logic error: {str(e)}")
        return 0

@log_function(args=False, result=False)
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

@log_function(args=False, result=False)
def FindStartEndPositionSubStringInStr(CodeString, SubString, LineNumber):
    try:
        if not SubString:
            raise ValueError("A substring cannot be empty")

        CodeLines = CodeString.splitlines()
        if LineNumber < 1 or LineNumber > len(CodeLines):
            raise ValueError("The row number is out of the allowed range")

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
            raise ValueError("The substring was not found in the string")

    except Exception as e:
        logger.error(f"Logic error: {str(e)}")
        return None

@log_function(args=False, result=False)
def SearchNodesWithChange(CodeAnalyze, change, parser):
    try:
        ChangeStart = change['start']
        ChangeEnd = change["end"]
        tree = GetASTTree(parser, CodeAnalyze)
        if not tree:
            raise ValueError(f"Syntax error in the file")

        NodesWithChangeList = []
        result = []
        CurrentPositionStart = ChangeStart
        while CurrentPositionStart < ChangeEnd and CodeAnalyze[CurrentPositionStart].isspace():
            CurrentPositionStart += 1
        PrefixStart = CodeAnalyze[:CurrentPositionStart+1]
        LinesStartList = PrefixStart.splitlines(keepends=True)
        StartLine = len(LinesStartList) - 1
        StartCol = len(LinesStartList[-1])-1 if LinesStartList else 0

        CurrentPositionEnd = ChangeEnd
        while CurrentPositionEnd >= ChangeStart and CodeAnalyze[CurrentPositionEnd].isspace():
            CurrentPositionEnd -= 1
        PrefixEnd = CodeAnalyze[:CurrentPositionEnd+1]
        LinesEnd = PrefixEnd.splitlines(keepends=True)
        EndLine = len(LinesEnd) - 1
        EndCol = len(LinesEnd[-1]) if LinesEnd else 0

        StartPoint = Point(row=StartLine, column=StartCol)
        EndPoint = Point(row=EndLine, column=EndCol)

        @log_function(args=False, result=False)
        def FindNodeWithAllChange(node, depth=0):
            candidate = node
            best_child = None
            for child in node.children:
                if FullyContainsRange(child, StartPoint, EndPoint):
                    best_child = child
                    break

            if best_child is not None:
                FindNodeWithAllChange(best_child, depth + 1)
            else:
                FindStartEndNode(candidate, True)
                if not NodesWithChangeList[0] == candidate:
                    FindStartEndNode(candidate, False)
                    if not NodesWithChangeList[-1] == candidate:
                        result.extend(GetNodesBetween(NodesWithChangeList[0], NodesWithChangeList[1], candidate))
                    else:
                        result.append(NodesWithChangeList[-1])
                else:
                    result.extend(NodesWithChangeList)

        @log_function(args=False, result=False)
        def FindStartEndNode(node, IsStart):
            CurrentPoint = StartPoint if IsStart else EndPoint
            IsChildrenIncludesStartChange = False
            for child in node.children:
                if child.start_point <= CurrentPoint <= child.end_point:
                    IsChildrenIncludesStartChange = True
                    FindStartEndNode(child, IsStart)
            NodesWithChangeList.append(node) if not IsChildrenIncludesStartChange else None

        FindNodeWithAllChange(tree.root_node)
        CoalesceEnclosingNodes(result, tree.root_node)
        if result:
            return result
        else:
            raise ValueError("There are no enclosing constructs for changes")

    except Exception as e:
        logger.error(f"Logic error: {str(e)}")
        return []

@log_function(args=False, result=False)
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

@log_function(args=False, result=False)
def FullyContainsRange(node, StartPoint, EndPoint):
    try:
        NodeStartPoint = node.start_point
        NodeEndPoint = node.end_point
        NodeStart = (NodeStartPoint.row, NodeStartPoint.column)
        NodeEnd = (NodeEndPoint.row, NodeEndPoint.column)
        ChangeStart = (StartPoint.row, StartPoint.column)
        ChangeEnd = (EndPoint.row, EndPoint.column)
        return NodeStart <= ChangeStart and NodeEnd >= ChangeEnd
    except Exception as e:
        logger.error(f"Logic error in FullyContainsRange: {str(e)}")
        return False

@log_function(args=False, result=False)
def CollectRightSiblingsAndUncles(node, StopAt):
    try:
        result = []
        cur = node
        while cur.parent != StopAt and cur is not None:
            parent = cur.parent
            if parent is not None:
                started = False
                for sibling in parent.children:
                    if started and sibling != StopAt:
                        result.append(sibling)
                    if sibling == cur:
                        started = True
            cur = parent
        return result
    except Exception as e:
        logger.error(f"Logic error: {str(e)}")

@log_function(args=False, result=False)
def CollectLeftSiblingsAndUncles(node, StopAt):
    try:
        result = []
        cur = node
        while cur.parent != StopAt and cur is not None:
            parent = cur.parent
            if parent is not None:
                for sibling in parent.children:
                    if sibling == cur:
                        break
                    if sibling != StopAt:
                        result.append(sibling)
            cur = parent
        return result
    except Exception as e:
        logger.error(f"Logic error: {str(e)}")

@log_function(args=False, result=False)
def nodes_between_ancestors(lca, FirstNode, SecondNode):
    try:
        between = []
        FirstChild = FirstNode
        SecondChild = SecondNode

        while FirstChild.parent != lca:
            FirstChild = FirstChild.parent
        while SecondChild.parent != lca:
            SecondChild = SecondChild.parent

        if FirstChild and SecondChild and FirstChild != SecondChild:
            started = False
            for child in lca.children:
                if child == FirstChild or child == SecondChild:
                    started = not started
                    continue
                if started:
                    between.append(child)
        return between
    except Exception as e:
        logger.error(f"Logic error: {str(e)}")

@log_function(args=False, result=False)
def GetNodesBetween(node1, node2, lca):
    try:
        right_from_first = CollectRightSiblingsAndUncles(node1, lca)
        left_from_second = CollectLeftSiblingsAndUncles(node2, lca)
        middle_under_lca = nodes_between_ancestors(lca, node1, node2)
        all_nodes = right_from_first + left_from_second + middle_under_lca
        all_nodes.extend([node1, node2])
        seen = set()
        unique_nodes = []
        for node in all_nodes:
            node_id = id(node)
            if node_id not in seen:
                seen.add(node_id)
                unique_nodes.append(node)

        unique_nodes.sort(key=lambda n: n.start_point)

        return unique_nodes
    except Exception as e:
        logger.error(f"Logic error: {str(e)}")

@log_function(args=False, result=False)
def GetASTTree(parser, CodeString):
    try:
        tree = parser.parse(CodeString.encode('utf-8'))
        if tree.root_node.type == 'ERROR':
            raise ValueError(f"A syntax error in the . AST file contains an ERROR node.")
        return tree
    except Exception as e:
        logger.error(f"Logic error: {str(e)}")
        return None

@log_function(args=False, result=False)
def FindSiblingNodes(Nodes, IsInsertInBegin, language):
    try:
        if not Nodes:
            raise ValueError("The Nodes list is empty. No nodes to analyze.")
        FistNode = Nodes[0]
        LastNode = Nodes[-1]
        PrevForFirst = FistNode.prev_sibling
        NextForLast = LastNode.next_sibling
        FilteredSiblingsDict = {
            'PrevForFirst': PrevForFirst if IsIndependentNode(PrevForFirst, language) and not IsInsertInBegin and  PrevForFirst.is_named else None,
            'NextForLast': NextForLast if IsIndependentNode(NextForLast, language) and not IsInsertInBegin and  NextForLast.is_named else None}
        return FilteredSiblingsDict
    except Exception as e:
        logger.error(f"Logic error: {str(e)}")
        return 0

@log_function(args=False, result=False)
def IsIndependentNode(node, language):
    try:
        LanguageModule = LoadLanguageModule(language)
        if node is None:
            return False
        if node.type not in LanguageModule.EXCLUDED_TYPES:
            return True
        return False
    except Exception as e:
        logger.error(f"Logic error: {str(e)}")
        return 0

@log_function(args=False, result=False)
def FindNearestStructure(node, NodeTypes):
    try:
        NearestStructure = []
        CounterNesting = 0
        node = node.parent
        IsNotFirst = False
        while node is not None:
            CounterNesting += 1
            if node.type in NodeTypes:
                NearestStructure.append({"CounterNesting": CounterNesting, "NearestStructure": node})
                if IsNotFirst:
                    break
                IsNotFirst = True
            node = node.parent
        return NearestStructure
    except Exception as e:
        logger.error(f"Logic error: {str(e)}")
        return {}

@log_function(args=False, result=False)
def AddInstruction(FilePath, MainBranch, parser, language):
    try:
        Match = []
        NumberInsert = 0
        SourceCode = ReadLastGitCommit(FilePath, MainBranch)
        Patch =[]
        while GetDiffOutput(SourceCode, FilePath):
            Change = CompareFileVersions(FilePath, SourceCode)
            if not Change:
                raise ValueError("no changes found")
            NodesWithChanges = SearchNodesWithChange(SourceCode, Change, parser)
            UpdateChangeDict = UpdateChange(Change, NodesWithChanges, SourceCode, language)
            Change = UpdateChangeDict["Change"]
            IsInsertInBegin = UpdateChangeDict["IsInsertInBegin"]
            action = Change['type']
            CommonParentStructure = []
            for NodesWithChange in NodesWithChanges:
                NearestStructs = FindOldParentConstruction(NodesWithChange, language)
                ParentStructure = []
                for NearestStruct in NearestStructs:
                    if NearestStruct["Structure"] is not None:
                        ParentStructure.append(NearestStruct["Structure"])
                if ParentStructure:
                    CommonParentStructure.append(ParentStructure)
            SiblingNodesDict = FindSiblingNodes(NodesWithChanges, IsInsertInBegin, language)
            match = GenerateMatch(NodesWithChanges, SiblingNodesDict, CommonParentStructure, SourceCode, action, language)
            if action == 'delete':
                patch = ''
            else:
                patch = Change["added"]
            Patch.append(patch)
            print(match, "\n Patch: ", patch)
            SourceCode = VerificationInstruction(patch, match, SourceCode, language, NumberInsert)
            if not SourceCode:
                raise ValueError('The match did`t work correctly')
            NumberInsert += 1
            Match.append(match)
        return {"Match": Match, "Patch": Patch}
    except Exception as e:
        logger.error(f"Logic error: {str(e)}")
        return 0

@log_function(args=False, result=False)
def UpdateChange(Change, NodesWithChanges, SourceCode, language):
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
            Change["added"] = NodeText[:ChangeTextIndex ]  + NodeText[ChangeTextIndex + len(ChangeText):]
            if ChangeType == "delete":
                Change["type"] = "replace"
    return {"Change": Change, "IsInsertInBegin": IsInsertInBegin}




@log_function(args=False, result=False)
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
                raise ValueError(f"Match № {NumberInsert}  not created")
    except ValueError as e:
        logger.error(f"Logic error: {str(e)}")
        return 0
    except OSError as e:
        logger.error(f"Input/Output error: {str(e)}")
        return 0
    finally:
        if TempFilePath:
            try:
                os.unlink(TempFilePath)
                logger.debug(f"The file has been deleted: {TempFilePath}")
            except OSError as e:
                logger.error(f"Error when deleting a file {TempFilePath}: {str(e)}")


@log_function(args=False, result=False)
def FindOldParentConstruction(NodesWithChange, language):
    try:
        LanguageModule = LoadLanguageModule(language)
        NearestStructureDictionary = FindNearestStructure(NodesWithChange, LanguageModule.FUNCTION_NODE_TYPES)
        NestingLevelStruct = [d["CounterNesting"] for d in NearestStructureDictionary]
        NearestStructNode = [d["NearestStructure"] for d in NearestStructureDictionary]

        NearestStructureDictionary = FindNearestStructure(NodesWithChange, LanguageModule.FUNCTION_NODE_TYPES)
        NearestStructNode.extend([d["NearestStructure"] for d in NearestStructureDictionary])
        NestingLevelStruct.extend([d["CounterNesting"] for d in NearestStructureDictionary])

        NearestStructureDictionary = FindNearestStructure(NodesWithChange, LanguageModule.BRACKET_STRUCTURE_TYPES)
        NearestStructNode.extend([d["NearestStructure"] for d in NearestStructureDictionary])
        NestingLevelStruct.extend([d["CounterNesting"] for d in NearestStructureDictionary])

        NearestStructs = [{"NestingLevel": level, "Structure": node}for level, node in zip(NestingLevelStruct, NearestStructNode)]
        NearestStructs = sorted(NearestStructs, key=lambda x: x["NestingLevel"])
        NearestStructs = [ struct for struct in NearestStructs if not (struct["NestingLevel"] == float('inf') and struct["Structure"] is None)]
        return NearestStructs
    except Exception as e:
        logger.error(f"Logic error: {str(e)}")
        return 0

@log_function(args=False, result=False)
def GenerateMatch(NodesWithChanges, siblings, NearestStructs, SourceCode, action, language):
    LanguageModule = LoadLanguageModule(language)
    CollectingMatchListDict = CollectingMatchList(NodesWithChanges, NearestStructs, siblings, language)
    MatchList = CollectingMatchListDict["SortedNodes"]
    ParentNodeList = CollectingMatchListDict["ParentNodeList"]
    ParentCloseIndexes = FindLastNodeInParent(MatchList, ParentNodeList, SourceCode, language)
    MatchString = ""
    ISAction = True if action == "add" else False
    ParentOpenIndex = {GetNodeText(ParentCloseIndex[2], SourceCode).split(BracketToNodeTypes(ParentCloseIndex[2], LanguageModule.BRACKET_TO_NODE_TYPES))[0].strip(): -1 for ParentCloseIndex in ParentCloseIndexes}
    for i, (node, NodeType) in enumerate(MatchList):

        NextNode, NextType = 0, 0
        if i + 1 < len(MatchList):
            NextNode, NextType = MatchList[i + 1]

        if NodeType == 'ParentNode':
            ParentBracketType = BracketToNodeTypes(node, LanguageModule.BRACKET_TO_NODE_TYPES)

            if len(MatchString) > 3 and  MatchString[-4: -1] != "..." or len(MatchString) < 3:
                MatchString += "\n ... "
            MatchString += f"\n { GetNodeText(node, SourceCode).split(ParentBracketType)[0].strip()} "
            MatchString += f" \n {ParentBracketType} ... "

        elif NodeType == 'NodeWithChange':
            if i == 0:
                MatchString += ' \n ... '
                if not ISAction:
                    MatchString += "\n >>> "
            MatchString += f"\n {GetNodeText(node, SourceCode)} "
            IsNextExist = len(MatchList) > i + 1
            if IsNextExist and NextType in ["ParentNode", 'SiblingNode']  or not NextType:
                if not ISAction:
                    MatchString += " \n <<< ... "
                else:
                    MatchString += "\n >>> "
                    if not NextType or  NextType != 'SiblingNode':
                        MatchString += "\n ... "

        elif NodeType == 'SiblingNode':
            if len(MatchString) > 3 and  MatchString[-4: -1] != "..."  and i > 0 and  MatchList[i-1][1] != "NodeWithChange" or len(MatchString) < 3:
                MatchString += " \n... "
            MatchString += f"\n{GetNodeText(node, SourceCode)}"
            if NextNode and not NextType == "NodeWithChange" or not NextNode:
                MatchString +=  "\n ... "

        if NextNode and NextType == "NodeWithChange" and NodeType != "NodeWithChange":
            if not ISAction:
                if len(MatchString) > 3 and  MatchString[-4: -1] != "..." and NodeType != "SiblingNode" or len(MatchString) < 3:
                    MatchString += f'\n ... >>> '
                else:
                    MatchString += f"\n  >>> "

        for ParentCloseIndex in ParentCloseIndexes:
            if ParentCloseIndex[0] == i:
                MatchStringTokenList = CheckAndRunTokenize(MatchString, language)
                for j in range(len(MatchStringTokenList) - 1, -1, -1):
                    if MatchStringTokenList[j] in OPEN_NESTING_MARKERS:
                        ParentOpenIndex[GetNodeText(ParentCloseIndex[2], SourceCode).split(MatchStringTokenList[j])[0].strip()] = j
                        break
    if ParentOpenIndex:
        MatchStringTokenList = CheckAndRunTokenize(MatchString, language)
        IsNestingMarkerPairsDictionary = UpdateUnpairedMarkers(MatchStringTokenList)
        ParentOpenIndexList = list(ParentOpenIndex.items())
        for i in range(len(ParentOpenIndexList)):
            if ParentOpenIndexList[i][1] != -1 and not IsNestingMarkerPairsDictionary[ParentOpenIndexList[i][1]][0]:
                if MatchStringTokenList[ParentOpenIndexList[i][1]] == "{":
                    MatchString += " } ..."
                elif MatchStringTokenList[ParentOpenIndexList[i][1]] == "(":
                    MatchString += " ) ..."
                elif MatchStringTokenList[ParentOpenIndexList[i][1]] == "[":
                    MatchString += " ] ..."
                elif MatchStringTokenList[ParentOpenIndexList[i][1]] == "<":
                    MatchString += " > ..."
    if len(MatchString) > 3 and MatchString[-4:-1] != "...":
        MatchString += " ..."
    return MatchString

def BracketToNodeTypes(node, typesSet):
    if node.type in typesSet["{"]:
        return "{"
    elif node.type in typesSet["("]:
        return "("
    elif node.type in typesSet["["]:
        return "["
    elif node.type in typesSet["<"]:
        return "<"

@log_function(args=False, result=False)
def GetNodeText(node, SourceCode):
    try:
        return SourceCode[node.start_byte:node.end_byte]
    except Exception as expt:
        raise ValueError(f"Could`nt extract the node text at the positions {node.start_byte}:{node.end_byte}: {expt}")

@log_function(args=False, result=False)
def IsNodeWholeConstruction(ParentNode, ChildNode, language):
    LanguageModule = LoadLanguageModule(language)
    if ParentNode.type not in LanguageModule.DICTIONARY_SOLID_STRUCTURES:
        return True
    return ChildNode.type not in LanguageModule.DICTIONARY_SOLID_STRUCTURES[ParentNode.type]

@log_function(args=False, result=False)
def CollectingMatchList(NodesWithChanges, NearestStructs, siblings, language):
    try:
        NodePositions = {}
        BlockParent = []
        ParentNodeList = []
        for i, node in enumerate(NodesWithChanges):
            NodePositions[node] = ((node.start_point[0], node.start_point[1]), 'NodeWithChange')
            if len(NearestStructs) >= i + 1:
                for ParentNode in NearestStructs[i]:
                    if not IsNodeWholeConstruction(ParentNode, node, language):
                        BlockParent.append(ParentNode)
                    if ParentNode not in NodePositions and ParentNode not in BlockParent:
                        NodePositions[ParentNode] = ((ParentNode.start_point[0], ParentNode.start_point[1]), 'ParentNode')
                    if ParentNode not in ParentNodeList:
                        ParentNodeList.append(ParentNode)
        PrevForFirst = siblings.get('PrevForFirst')
        NextForLast = siblings.get('NextForLast')
        if PrevForFirst:
            NodePositions[PrevForFirst] = ((PrevForFirst.start_point[0], PrevForFirst.start_point[1]), 'SiblingNode')
        if NextForLast:
            NodePositions[NextForLast] = ((NextForLast.start_point[0], NextForLast.start_point[1]), 'SiblingNode')

        SortedNodes = sorted(
            [(node, NodeType) for node, (pos, NodeType) in NodePositions.items()],
            key=lambda x: NodePositions[x[0]][0]
        )
        return {"SortedNodes": SortedNodes, "ParentNodeList": ParentNodeList}
    except Exception as e:
        logger.error(f"Logic error: {str(e)}")
        return 0

@log_function(args=False, result=False)
def FindLastNodeInParent(MatchNodeList, ParentList, SourceCode, language):
    try:
        LanguageModule = LoadLanguageModule(language)
        ParentCloseIndex = {ParentNode: None for ParentNode in ParentList}
        IsFirstForNode = {ParentNode: True for ParentNode in ParentList}
        for i in range(len(MatchNodeList)):
            node, _ = MatchNodeList[i]
            for ParentNode in ParentList:
                if ParentNode.start_point[0] <= node.start_point[0] <= ParentNode.end_point[0]:
                    BracketType = BracketToNodeTypes(ParentNode, LanguageModule.BRACKET_TO_NODE_TYPES)
                    if IsFirstForNode[ParentNode] or GetNodeText(node, SourceCode) in GetNodeText(ParentNode, SourceCode).split(BracketType)[0].strip():
                        if len(MatchNodeList) > i + 1:
                            NextNode, _= MatchNodeList[i+1]
                        else:
                            NextNode = 0
                        ParentCloseIndex[ParentNode] = (i, i)
                        IsFirstForNode[ParentNode] = False
                        if NextNode and GetNodeText(NextNode, SourceCode) == BracketType:
                            ParentCloseIndex[ParentNode] = (i+1, i)
                    else:
                        ParentCloseIndex[ParentNode] = (ParentCloseIndex[ParentNode][0], i)
        ParentCloseIndex = [(v1, v2, k) for k, (v1, v2) in ParentCloseIndex.items()]
        ParentCloseIndex = sorted(ParentCloseIndex, key=lambda x: x[2].start_point, reverse=True)
        return ParentCloseIndex
    except Exception as e:
        logger.error(f"Logic error: {str(e)}")
        return 0



@log_function(args=False, result=False)
def CreateMarkdownInstructions(OutPath, FilePath, MainBranch, parser, language):
    try:
        AddInstructionDict = AddInstruction(FilePath, MainBranch, parser, language)
        if not AddInstructionDict:
            raise ValueError("There are no instructions ")
        Match = AddInstructionDict["Match"]
        patch = AddInstructionDict["Patch"]
        with open(OutPath, 'w', encoding='utf-8') as MdFile:
            if not Match:
                raise ValueError("The list of instructions is empty")

            for idx  in range(len(Match)):
                MdFile.write(f"### match\n")
                MdFile.write(f"```\n{Match[idx]}\n```\n")

                MdFile.write(f"### patch\n")

                MdFile.write(f"```\n{patch[idx]}\n```\n\n")

        logger.info(f"Markdown file has been created successfully: {OutPath}")
        return True

    except Exception as e:
        logger.error(f"Error when creating a Markdown file: {str(e)}")
        return False
