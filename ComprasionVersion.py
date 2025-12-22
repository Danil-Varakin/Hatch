import os
import tempfile
from ComprasionInput import handle_match_conflict
from Insert import RunInsert
from tree_sitter import Point
from TokenizeCode import CheckAndRunTokenize
from Logging import setup_logger, log_function
from tree_sitter_language_pack import get_parser
from Utilities import ReadFile, LoadLanguageModule
from typing import Any, Optional, Dict, Union
from constants import OPEN_NESTING_MARKERS, OPEN_TO_CLOSE_NESTING_MARKERS, CLOSE_NESTING_MARKERS, CLOSE_TO_OPEN_NESTING_MARKERS
from gitUtils import GetDiffOutput, ReadLastGitCommit
from getChange import CompareFilesFromPoint, UpdateChange, GetChange, GetChangeIndexes

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
                if child.start_point <= CurrentPoint < child.end_point or not IsStart and child.start_point <= CurrentPoint <= child.end_point:
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
        RightFromFirst = CollectRightSiblingsAndUncles(node1, lca)
        LeftFromSecond = CollectLeftSiblingsAndUncles(node2, lca)
        MiddleUnderLca = NodesBetweenAncestors(lca, node1, node2)
        AllNodes = RightFromFirst + LeftFromSecond + MiddleUnderLca
        AllNodes.extend([node1, node2])
        seen = set()
        UniqueNodes = []
        for node in AllNodes:
            NodeId = id(node)
            if NodeId not in seen:
                seen.add(NodeId)
                UniqueNodes.append(node)

        UniqueNodes.sort(key=lambda n: n.start_point)

        return UniqueNodes
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
def FindNearestStructure(node: Any, NodeTypes: list[str], IsControlStructure: bool) -> Union[list[Dict[str, Any]], Dict]:
    try:
        NearestStructure = []
        CounterNesting = 0
        node = node.parent
        IsNotFirst = False
        while node is not None:
            CounterNesting += 1
            if node.type in NodeTypes:
                NearestStructure.append({"CounterNesting": CounterNesting, "NearestStructure": node})
                if IsNotFirst or IsControlStructure:
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
        IsControlStructure = False
        for i, GroupStruct in enumerate([LanguageModule.FUNCTION_NODE_TYPES, LanguageModule.BRACKET_STRUCTURE_TYPES, LanguageModule.CONTROL_STRUCTURE_TYPES]):
            if i == 2:
                IsControlStructure = True
            NearestStructureDictionary = FindNearestStructure(NodesWithChange, GroupStruct, IsControlStructure)
            for item in NearestStructureDictionary:
                ParentStructuresWithLevels.append({"NestingLevel": item["CounterNesting"], "Structure": item["NearestStructure"]})

        ParentStructuresWithLevels = [struct for struct in ParentStructuresWithLevels if not (struct["NestingLevel"] == float('inf') and struct["Structure"] is None)]
        ParentStructuresWithLevels.sort(key=lambda x: x["NestingLevel"])
        return [struct["Structure"] for struct in ParentStructuresWithLevels]

    except Exception as e:
        logger.error(f"Logic error: {str(e)}")
        return []

@log_function(args=False, result=False)
def AddInstruction(FilePath: str, MainBranch: str, language: str) ->tuple[list[str], list[str]]:
    try:
        Match = []
        Patch =[]
        NumberInsert = 0
        NewSourceCode = ReadFile(FilePath)
        SourceCode = ReadLastGitCommit(FilePath, MainBranch)
        while  CompareFilesFromPoint(SourceCode, ReadFile(FilePath)):
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
            if match in Match:
                Match, Patch = handle_match_conflict(Match, Patch)

            SourceCode = VerificationInstruction(patch, match, SourceCode, language, NumberInsert)

            if not SourceCode:
                raise ValueError('The match did`t work correctly')
            NumberInsert += 1
            Match.append(match)

        return  Match, Patch
    except Exception as e:
        logger.error(f"Logic error: {str(e)}")
        return [], []

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
    MatchList = CollectingMatchList(NodesWithChanges, NearestStructs, siblings, language)

    MatchString = "..."
    ISAction = True if action == "add" else False

    for i, (node, NodeType) in enumerate(MatchList):
        IsEllipsisTail =  MatchString[-3:len(MatchString)] == "..." or MatchString[-4:-1]  == "..."
        NextNode, NextType = 0, 0
        if i + 1 < len(MatchList):
            NextNode, NextType = MatchList[i + 1]

        if NodeType == 'ParentNode':
            ParentBracketType = BracketToNodeTypes(node, LanguageModule.BRACKET_TO_NODE_TYPES)
            if not IsEllipsisTail:
                MatchString += "\n ... "
            MatchString += GetParentText (node, MatchList, i, SourceCode, ParentBracketType)

        elif NodeType == 'NodeWithChange':
            if i == 0:
                MatchString += "\n>>>"
            MatchString += f"\n {GetNodeText(node, SourceCode)} "
            IsNextExist = len(MatchList) > i + 1
            if IsNextExist and NextType in ["ParentNode", 'SiblingNode']  or not NextType:
                if not ISAction:
                    MatchString += " <<< ... "
                else:
                    MatchString += "\n >>> "
                    if not NextType or  NextType != 'SiblingNode':
                        MatchString += "\n ... "

        elif NodeType == 'SiblingNode':
            if not IsEllipsisTail and i > 0 and MatchList[i-1][1] != "NodeWithChange":
                MatchString += " \n... "
            MatchString += f"\n{GetNodeText(node, SourceCode)}"
            if NextNode and not NextType == "NodeWithChange" or not NextNode:
                MatchString +=  "\n ... "

        if NextNode and NextType == "NodeWithChange" and NodeType != "NodeWithChange" and not ISAction:
            if not IsEllipsisTail and NodeType != "SiblingNode":
                MatchString += f' ... >>> '
            else:
                MatchString += f"  >>> "

    IsEllipsisTail = MatchString[-3:len(MatchString)] == "..." or MatchString[-4:-1]  == "..."
    if not IsEllipsisTail:
        MatchString += " ..."
    MatchString = autoCloseBrackets(MatchString)
    return MatchString

@log_function(args=False, result=False)
def BracketToNodeTypes(node: Any, typesSet: Dict[str, str]) -> Optional[str]:
    node_type = node.type
    for bracket, node_types in typesSet.items():
        if node_type in node_types:

            return bracket
    return None

@log_function(args=False, result=False)
def GetParentText (CurrentNode, MatchList, MatchListIndex, SourceCode, ParentBracketType):
    node = MatchList[MatchListIndex + 1][0]
    ParentText = f"\n {GetNodeText(CurrentNode, SourceCode).split(ParentBracketType)[0].strip()}"
    if GetNodeText(node, SourceCode) in ParentText:
        for bracket in OPEN_NESTING_MARKERS:
            ParentText = f"\n {GetNodeText(CurrentNode, SourceCode).split(bracket)[0].strip()}"
            if GetNodeText(node, SourceCode) not in ParentText:
                ParentText +=  f" {bracket} ... "
                return ParentText
    return f"\n {GetNodeText(CurrentNode, SourceCode).split(ParentBracketType)[0].strip()}" + (f" {ParentBracketType} ... " if ParentBracketType else "")


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
def CollectingMatchList(NodesWithChanges: list[Any], NearestStructs: list[list[Any]], siblings: Dict[str, Optional[Any]], language: str) -> list[Any]:
    try:
        NodePositions = {}
        BlockParent = []
        for i, node in enumerate(NodesWithChanges):
            NodePositions[node] = ((node.start_point[0], node.start_point[1]), 'NodeWithChange')
            if len(NearestStructs) >= i + 1:
                for ParentNode in NearestStructs[i]:
                    if not IsNodeWholeConstruction(ParentNode, node, language):
                        BlockParent.append(ParentNode)
                    if ParentNode not in NodePositions and ParentNode not in BlockParent:
                        NodePositions[ParentNode] = ((ParentNode.start_point[0], ParentNode.start_point[1]), 'ParentNode')
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

        return FilteredNodes
    except Exception as e:
        logger.error(f"Logic error: {str(e)}")
        return []

@log_function(args=False, result=False)
def autoCloseBrackets(MatchString):
    if MatchString:
        NestingMarkerStack = []
        for symbol in MatchString:
            if symbol in OPEN_NESTING_MARKERS:
                NestingMarkerStack.append(symbol)
            if symbol in CLOSE_NESTING_MARKERS and NestingMarkerStack and NestingMarkerStack[-1] == CLOSE_TO_OPEN_NESTING_MARKERS[symbol]:
                NestingMarkerStack.pop()
        for NestingMarker in reversed(NestingMarkerStack):
            MatchString += OPEN_TO_CLOSE_NESTING_MARKERS[NestingMarker] + " ...  "
    return MatchString

