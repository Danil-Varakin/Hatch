import os
import tempfile
from Insert import RunInsert
from tree_sitter import Point
from constants import OPEN_NESTING_MARKERS
from TokenizeCode import CheckAndRunTokenize
from SearchCode import UpdateUnpairedMarkers
from Logging import setup_logger, log_function
from tree_sitter_language_pack import get_parser
from Utilities import ReadFile, LoadLanguageModule
from typing import Any, Optional, Dict, Tuple, Union
from gitUtils import GetDiffOutput, ReadLastGitCommit
from getChange import compare_files_from_point, UpdateChange, GetChange, GetChangeIndexes

logger = setup_logger()

@log_function(args=False, result=False)
def SearchNodesWithChange(StartPoint: Any, EndPoint: Any, tree: Any) -> list[Any]:
    try:
        NodesWithChangeList = []
        result = []
        @log_function(args=False, result=False)
        def FindNodeWithAllChange(node: Any, depth: int = 0) -> None:
            candidate = node
            BestChild = None
            for child in node.children:
                if FullyContainsRange(child, StartPoint, EndPoint):
                    BestChild = child
                    break

            if BestChild is not None:
                FindNodeWithAllChange(BestChild, depth + 1)
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
        def FindStartEndNode(node: Any, IsStart: bool) -> None:
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
def GetChangeStartEndPoint(CodeAnalyze: str, change: Dict[str, Any]) -> Any:
    ChangeStart = change['start']
    ChangeEnd = change["end"]

    while ChangeStart < ChangeEnd and CodeAnalyze[ChangeStart].isspace():
        ChangeStart += 1
    PrefixStart = CodeAnalyze[:ChangeStart + 1]
    LinesStartList = PrefixStart.splitlines(keepends=True)
    StartLine = len(LinesStartList) - 1
    StartCol = len(LinesStartList[-1]) - 1 if LinesStartList else 0

    while ChangeEnd >= ChangeStart and CodeAnalyze[ChangeEnd].isspace():
        ChangeEnd -= 1
    PrefixEnd = CodeAnalyze[:ChangeEnd + 1]
    LinesEnd = PrefixEnd.splitlines(keepends=True)
    EndLine = len(LinesEnd) - 1
    EndCol = len(LinesEnd[-1]) if LinesEnd else 0

    StartPoint = Point(row=StartLine, column=StartCol)
    EndPoint = Point(row=EndLine, column=EndCol)
    return StartPoint, EndPoint

@log_function(args=False, result=False)
def CoalesceEnclosingNodes(EnclosingNodes: list[Any], root: Any) -> Union[list[Any], int]:
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
def FullyContainsRange(node: Any, StartPoint: Point, EndPoint: Point) -> bool:
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
def CollectRightSiblingsAndUncles(node: Any, StopAt: Any) -> list[Any]:
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
        return []

@log_function(args=False, result=False)
def CollectLeftSiblingsAndUncles(node: Any, StopAt: Any) -> list[Any]:
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
        return []

@log_function(args=False, result=False)
def NodesBetweenAncestors(lca: Any, FirstNode: Any, SecondNode: Any) -> list[Any]:
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
        return  []

@log_function(args=False, result=False)
def GetNodesBetween(node1: Any, node2: Any, lca: Any) -> list[Any]:
    try:
        right_from_first = CollectRightSiblingsAndUncles(node1, lca)
        left_from_second = CollectLeftSiblingsAndUncles(node2, lca)
        middle_under_lca = NodesBetweenAncestors(lca, node1, node2)
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
        return []

@log_function(args=False, result=False)
def GetASTTree(CodeString: str, language):
    try:
        parser = get_parser(language)
        tree = parser.parse(CodeString.encode('utf-8'))
        if tree.root_node.type == 'ERROR':
            raise ValueError(f"A syntax error in the . AST file contains an ERROR node.")
        return tree
    except Exception as e:
        logger.error(f"Logic error: {str(e)}")
        return None

@log_function(args=False, result=False)
def FindSiblingNodes(Nodes: list[Any], IsInsertInBegin: bool, language: str) -> Union[Dict[str, Optional[Any]], int]:
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
def IsIndependentNode(node: Any, language: str) -> Union[bool, int]:
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
def FindNearestStructure(node: Any, NodeTypes: list[str]) -> Union[list[Dict[str, Any]], Dict]:
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
def FindParentConstructionALLType(NodesWithChange: Any, language: str) -> list[Any]:
    try:
        LanguageModule = LoadLanguageModule(language)
        ParentStructuresWithLevels = []

        for GroupStruct in [LanguageModule.FUNCTION_NODE_TYPES, LanguageModule.BRACKET_STRUCTURE_TYPES, LanguageModule.CONTROL_STRUCTURE_TYPES]:
            NearestStructureDictionary = FindNearestStructure(NodesWithChange, GroupStruct)
            for item in NearestStructureDictionary:
                ParentStructuresWithLevels.append({"NestingLevel": item["CounterNesting"], "Structure": item["NearestStructure"]})

        ParentStructuresWithLevels = [struct for struct in ParentStructuresWithLevels if not (struct["NestingLevel"] == float('inf') and struct["Structure"] is None)]
        ParentStructuresWithLevels.sort(key=lambda x: x["NestingLevel"])
        return [struct["Structure"] for struct in ParentStructuresWithLevels]

    except Exception as e:
        logger.error(f"Logic error: {str(e)}")
        return []

@log_function(args=False, result=False)
def AddInstruction(FilePath: str, MainBranch: str, language: str) -> Dict[str, list[str]]:
    try:
        Match = []
        Patch =[]
        NumberInsert = 0
        NewSourceCode = ReadFile(FilePath)
        SourceCode = ReadLastGitCommit(FilePath, MainBranch)
        while  compare_files_from_point(SourceCode, ReadFile(FilePath)):
            DiffOutput = GetDiffOutput(SourceCode, FilePath)
            ChangeLinesIndex = GetChangeIndexes(DiffOutput)
            Change = GetChange(ChangeLinesIndex, SourceCode, NewSourceCode)
            if not Change:
                raise ValueError("Changes no found")

            tree = GetASTTree(SourceCode, language)
            StartPoint, EndPoint = GetChangeStartEndPoint(SourceCode, Change)
            NodesWithChanges = SearchNodesWithChange(StartPoint, EndPoint, tree)
            
            UpdateChangeDict = UpdateChange(Change, NodesWithChanges, SourceCode, language)
            Change = UpdateChangeDict["Change"]
            IsInsertInBegin = UpdateChangeDict["IsInsertInBegin"]
            action = Change['type']
            
            ParentStructureForChangeNode = []
            for NodesWithChange in NodesWithChanges:
                ParentStructure = FindParentConstructionALLType(NodesWithChange, language)
                ParentStructureForChangeNode.append(ParentStructure)

            SiblingNodesDict = FindSiblingNodes(NodesWithChanges, IsInsertInBegin, language)
            match = GenerateMatch(NodesWithChanges, SiblingNodesDict, ParentStructureForChangeNode, SourceCode, action, language)
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
        return {}

@log_function(args=False, result=False)
def VerificationInstruction(Patch: str, Match: str, SourceCode: str, Language: str, NumberInsert: int) -> str:
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
        return ""
    except OSError as e:
        logger.error(f"Input/Output error: {str(e)}")
        return ""
    finally:
        if TempFilePath:
            os.unlink(TempFilePath)

@log_function(args=False, result=False)
def GenerateMatch(NodesWithChanges, siblings, NearestStructs, SourceCode, action, language) -> str:
    LanguageModule = LoadLanguageModule(language)
    CollectingMatchListDict = CollectingMatchList(NodesWithChanges, NearestStructs, siblings, language)
    MatchList = CollectingMatchListDict["SortedNodes"]
    ParentNodeList = CollectingMatchListDict["ParentNodeList"]
    ParentCloseIndexes = FindLastNodeInParent(MatchList, ParentNodeList, SourceCode, language)
    MatchString = "..."
    ISAction = True if action == "add" else False
    ParentOpenIndex = {GetNodeText(ParentCloseIndex[2], SourceCode).split(BracketToNodeTypes(ParentCloseIndex[2], LanguageModule.BRACKET_TO_NODE_TYPES))[0].strip(): -1 for ParentCloseIndex in ParentCloseIndexes}

    for i, (node, NodeType) in enumerate(MatchList):
        IsNonEllipsisTail = MatchString[-4:-1]  != "..." or MatchString[-3:len(MatchString)] != "..."
        NextNode, NextType = 0, 0
        if i + 1 < len(MatchList):
            NextNode, NextType = MatchList[i + 1]

        if NodeType == 'ParentNode':
            ParentBracketType = BracketToNodeTypes(node, LanguageModule.BRACKET_TO_NODE_TYPES)
            if not IsNonEllipsisTail:
                MatchString += "\n ... "
            MatchString += f"\n { GetNodeText(node, SourceCode).split(ParentBracketType)[0].strip()} "
            MatchString += f" \n {ParentBracketType} ... "

        elif NodeType == 'NodeWithChange':
            if i == 0:
                MatchString += "\n>>>"
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
            if not IsNonEllipsisTail and i > 0 and MatchList[i-1][1] != "NodeWithChange":
                MatchString += " \n... "
            MatchString += f"\n{GetNodeText(node, SourceCode)}"
            if NextNode and not NextType == "NodeWithChange" or not NextNode:
                MatchString +=  "\n ... "

        if NextNode and NextType == "NodeWithChange" and NodeType != "NodeWithChange" and not ISAction:
            if not IsNonEllipsisTail and NodeType != "SiblingNode":
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

    IsNonEllipsisTail = MatchString[-4:-1] != "..."
    if not IsNonEllipsisTail:
        MatchString += " ..."
    return MatchString

def BracketToNodeTypes(node: Any, typesSet: Dict[str, str]) -> Optional[str]:
    if node.type in typesSet["{"]:
        return "{"
    elif node.type in typesSet["("]:
        return "("
    elif node.type in typesSet["["]:
        return "["
    else:
        return "<"

@log_function(args=False, result=False)
def GetNodeText(node: Any, SourceCode: str) -> str:
    try:
        source_bytes = SourceCode.encode('utf-8')
        return source_bytes[node.start_byte:node.end_byte].decode('utf-8')
    except Exception as expt:
        raise ValueError(f"Could`nt extract the node text at the positions {node.start_byte}:{node.end_byte}: {expt}")

@log_function(args=False, result=False)
def IsNodeWholeConstruction(ParentNode: Any, ChildNode: Any, language: str) -> bool:
    LanguageModule = LoadLanguageModule(language)
    if ParentNode.type not in LanguageModule.DICTIONARY_SOLID_STRUCTURES:
        return True
    return ChildNode.type not in LanguageModule.DICTIONARY_SOLID_STRUCTURES[ParentNode.type]

@log_function(args=False, result=False)
def CollectingMatchList(NodesWithChanges: list[Any], NearestStructs: list[list[Any]], siblings: Dict[str, Optional[Any]], language: str) -> Union[Dict[str, list], int]:
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

        SortedNodes = sorted([(node, NodeType) for node, (pos, NodeType) in NodePositions.items()], key=lambda x: NodePositions[x[0]][0])

        FilteredNodes = []
        FoundImportant = False
        for node, NodeType in SortedNodes:
            if NodeType in ('SiblingNode', 'NodeWithChange'):
                FoundImportant = True
            if NodeType != 'ParentNode' or not FoundImportant:
                FilteredNodes.append((node, NodeType))

        return {"SortedNodes": FilteredNodes, "ParentNodeList": ParentNodeList}
    except Exception as e:
        logger.error(f"Logic error: {str(e)}")
        return 0

@log_function(args=False, result=False)
def FindLastNodeInParent(MatchNodeList: list[Tuple[Any, str]], ParentList: list[Any], SourceCode: str, language: str) -> list[Tuple[int, int, Any]]:
    try:
        LanguageModule = LoadLanguageModule(language)
        ParentCloseIndex = {ParentNode: (0, 0) for ParentNode in ParentList}
        IsFirstForNode = {ParentNode: True for ParentNode in ParentList}

        for i in range(len(MatchNodeList)):
            node, _ = MatchNodeList[i]
            for ParentNode in ParentList:
                if ParentNode.start_point[0] <= node.start_point[0] <= ParentNode.end_point[0]:
                    BracketType = BracketToNodeTypes(ParentNode, LanguageModule.BRACKET_TO_NODE_TYPES)
                    if IsFirstForNode[ParentNode] or GetNodeText(node, SourceCode) in \
                            GetNodeText(ParentNode, SourceCode).split(BracketType)[0].strip():
                        NextNode = None
                        if len(MatchNodeList) > i + 1:
                            NextNode, _ = MatchNodeList[i + 1]

                        ParentCloseIndex[ParentNode] = (i, i)
                        IsFirstForNode[ParentNode] = False

                        if NextNode and GetNodeText(NextNode, SourceCode) == BracketType:
                            ParentCloseIndex[ParentNode] = (i + 1, i)
                    else:
                        current_start, _ = ParentCloseIndex[ParentNode]
                        ParentCloseIndex[ParentNode] = (current_start, i)

        ParentCloseIndex = [(v1, v2, ParentNode) for ParentNode, (v1, v2) in ParentCloseIndex.items()]
        ParentCloseIndex = sorted(ParentCloseIndex, key=lambda x: x[2].start_point, reverse=True)
        return ParentCloseIndex
    except Exception as e:
        logger.error(f"Logic error: {str(e)}")
        return []



@log_function(args=False, result=False)
def CreateMarkdownInstructions(OutPath: str, FilePath: str, MainBranch: str, language: str) -> bool:
    try:
        AddInstructionDict = AddInstruction(FilePath, MainBranch, language)
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
