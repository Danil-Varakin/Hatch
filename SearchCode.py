from constants import SPECIAL_OPERATORS, OPEN_NESTING_MARKERS, CLOSE_NESTING_MARKERS, NESTING_MARKERS, DICTIONARY_NESTING_MARKERS

def SearchInsertIndexInTokenList(MatchTokenList, SourceCodeTokenList):
    IsPassDictionaryList = [{"IndexString": "", "CurrentSourceCodeTokenIndex": 0, "SourceCodeNestingLevel": 0, "SourceCodeRelativeNestingLevel": 0,"CurrentSourceCodeTokenStringIndex": 0, 'StartSourceCodeTokenIndex': 0, 'StartSourceCodeTokenStringIndex': 0}]
    IsInsertIndexDictionaryList = []
    IsReplaceIndexDictionaryList = []
    FlagFirstCircle = True
    NestingMap = MatchNestingLevelInsertALL(MatchTokenList)
    for MatchTokenIndex in range(len(MatchTokenList)):
        if MatchTokenList[MatchTokenIndex] == '...':
            IsPassDictionaryList, FlagFirstCircle = IsPass(MatchTokenList, MatchTokenIndex, SourceCodeTokenList, IsPassDictionaryList, FlagFirstCircle, NestingMap)
        if MatchTokenList[MatchTokenIndex] == ">>>":
            IsInsertIndexDictionaryList, IsPassDictionaryList, FlagFirstCircle = IsInsert(MatchTokenList, MatchTokenIndex, SourceCodeTokenList, IsPassDictionaryList, FlagFirstCircle, NestingMap)
        if MatchTokenList[MatchTokenIndex] == "<<<":
            if IsInsertIndexDictionaryList:
                IsReplaceIndexDictionaryList, IsPassDictionaryList, FlagFirstCircle = IsInsert(MatchTokenList, MatchTokenIndex, SourceCodeTokenList, IsPassDictionaryList, FlagFirstCircle, NestingMap)
            else: return 0
        if not IsPassDictionaryList:
            return 0
    return IsInsertIndexDictionaryList, IsPassDictionaryList, IsReplaceIndexDictionaryList


def ComparisonToken(MatchTokenList, MatchTokenIndex, SourceCodeTokenList, SourceCodeTokenIndex, SourceCodeNestingLevel, FlagFirstCircle, SourceCodeRelativeNestingLevel, NestingMap, CurrentSourceCodeTokenStringIndex):
    ComparisonFlagFirstCircle = True
    SubIndex = MatchTokenIndex + 2
    MatchToken = MatchTokenList[SubIndex]
    ComparisonSourceCodeNestingLevel = 0
    ComprasionSourceCodeRelativeNestingLevel = 0
    ComparisonSourceCodeTokenIndex = SourceCodeTokenIndex
    while SubIndex < len(MatchTokenList) and MatchTokenList[SubIndex] not in SPECIAL_OPERATORS:
        if FlagFirstCircle or not ComparisonFlagFirstCircle:
            if NestingMap[SubIndex][0] == -1:
                ComprasionSourceCodeRelativeNestingLevel = SourceNestingLevelChange(ComprasionSourceCodeRelativeNestingLevel, SourceCodeTokenList, ComparisonSourceCodeTokenIndex, 0)
            ComparisonSourceCodeNestingLevel = SourceNestingLevelChange(ComparisonSourceCodeNestingLevel, SourceCodeTokenList, ComparisonSourceCodeTokenIndex, 0)
        ComparisonFlagFirstCircle = False
        SourceCodeToken = SourceCodeTokenList[ComparisonSourceCodeTokenIndex]

        if SourceCodeToken[CurrentSourceCodeTokenStringIndex:] == MatchToken:
            SubIndex += 1
            MatchToken = MatchTokenList[SubIndex] if SubIndex < len(MatchTokenList) else ""
            ComparisonSourceCodeTokenIndex += 1
            CurrentSourceCodeTokenStringIndex = 0
        elif SourceCodeToken.startswith(MatchToken, CurrentSourceCodeTokenStringIndex):
            CurrentSourceCodeTokenStringIndex += len(MatchToken)
            SubIndex += 1
            MatchToken = MatchTokenList[SubIndex] if SubIndex < len(MatchTokenList) else ""
        elif len(SourceCodeToken) == CurrentSourceCodeTokenStringIndex + 1 and( len(SourceCodeToken) > 1 or ComparisonSourceCodeTokenIndex == SourceCodeTokenIndex):
            ComparisonSourceCodeTokenIndex += 1
            CurrentSourceCodeTokenStringIndex = 0
        else:
            return False
    if MatchTokenList[MatchTokenIndex + 2] in SPECIAL_OPERATORS:
        if len(SourceCodeTokenList[SourceCodeTokenIndex]) == CurrentSourceCodeTokenStringIndex + 1:
            ComparisonSourceCodeTokenIndex += 1
            CurrentSourceCodeTokenStringIndex = 0
    return  SourceCodeNestingLevel, ComparisonSourceCodeNestingLevel, SourceCodeRelativeNestingLevel, ComprasionSourceCodeRelativeNestingLevel, CurrentSourceCodeTokenStringIndex, ComparisonSourceCodeTokenIndex, SubIndex -1


def SourceNestingLevelChange(SourceCodeNestingLevel, SourceCodeTokenList, SourceCodeTokenIndex, ComparisonIndex):

    if SourceCodeTokenList[SourceCodeTokenIndex + ComparisonIndex] in OPEN_NESTING_MARKERS:
        SourceCodeNestingLevel = SourceCodeNestingLevel + 1

    if SourceCodeTokenList[SourceCodeTokenIndex + ComparisonIndex] in CLOSE_NESTING_MARKERS:
        SourceCodeNestingLevel = SourceCodeNestingLevel - 1

    return SourceCodeNestingLevel


def IsPass(MatchTokenList, MatchTokenIndex, SourceCodeTokenList, IsPassDictionary, FlagFirstCircle, NestingMap):

    IsPassOutputDictionary = []

    if IsPassDictionary:
        SkipPass = False
        if (MatchTokenIndex + 1 < len(MatchTokenList) and MatchTokenList[MatchTokenIndex + 1] in SPECIAL_OPERATORS) or MatchTokenIndex + 1 == len(MatchTokenList):
            SkipPass = True

        if not SkipPass:
            for IsPassOutput in IsPassDictionary:
                SourceCodeNestingLevel = IsPassOutput["SourceCodeNestingLevel"]
                SourceCodeRelativeNestingLevel = IsPassOutput["SourceCodeRelativeNestingLevel"]
                StartCurrentSourceCodeTokenIndex = IsPassOutput["CurrentSourceCodeTokenIndex"]
                SourceCodeTokenStringIndex = IsPassOutput["CurrentSourceCodeTokenStringIndex"]
                CounterMatches = 0
                BreakFlag = False
                for SourceCodeTokenIndex in range(StartCurrentSourceCodeTokenIndex, len(SourceCodeTokenList)):

                    if MatchTokenIndex + 1 < len(MatchTokenList):
                        if not FlagFirstCircle:
                            if NestingMap[MatchTokenIndex + 1][0] == -1:
                                SourceCodeRelativeNestingLevel = SourceNestingLevelChange(SourceCodeRelativeNestingLevel, SourceCodeTokenList, SourceCodeTokenIndex, 0)
                            SourceCodeNestingLevel = SourceNestingLevelChange(SourceCodeNestingLevel, SourceCodeTokenList, SourceCodeTokenIndex, 0)
                        MatchTokenEndsInSourceCodeTokenList = FindAllSubstringEnds(SourceCodeTokenList[SourceCodeTokenIndex], MatchTokenList[MatchTokenIndex + 1], SourceCodeTokenStringIndex)
                        SourceCodeTokenStringIndex = 0
                        if MatchTokenEndsInSourceCodeTokenList:
                            StartSourceCodeRelativeNestingLevel = SourceCodeRelativeNestingLevel
                            StartSourceCodeNestingLevel = SourceCodeNestingLevel

                            for CurrentSourceCodeTokenStringIndex in MatchTokenEndsInSourceCodeTokenList:
                                StartSourceCodeTokenStringIndex = CurrentSourceCodeTokenStringIndex
                                ComparisonTokenResults = ComparisonToken(MatchTokenList, MatchTokenIndex, SourceCodeTokenList, SourceCodeTokenIndex, SourceCodeNestingLevel, FlagFirstCircle, SourceCodeRelativeNestingLevel, NestingMap,CurrentSourceCodeTokenStringIndex)
                                if ComparisonTokenResults:
                                    SourceCodeNestingLevel, ComparisonSourceCodeNestingLevel, SourceCodeRelativeNestingLevel, ComprasionSourceCodeRelativeNestingLevel, CurrentSourceCodeTokenStringIndex, ComparisonSourceCodeTokenIndex, SubIndex = ComparisonTokenResults
                                    IndexString = IsPassOutput["IndexString"] + str(CounterMatches) + '/'

                                    if NestingMap[SubIndex][0] != -1:
                                        if NestingMap[SubIndex][0] == SourceCodeNestingLevel + ComparisonSourceCodeNestingLevel:
                                            CurrentSourceCodeTokenIndex = ComparisonSourceCodeTokenIndex
                                            SourceCodeRelativeNestingLevel = SourceCodeRelativeNestingLevel + ComprasionSourceCodeRelativeNestingLevel
                                            SourceCodeNestingLevel = SourceCodeNestingLevel + ComparisonSourceCodeNestingLevel
                                            CounterMatches += 1
                                            IsPassOutputDictionary.append({"IndexString": IndexString, "CurrentSourceCodeTokenIndex": CurrentSourceCodeTokenIndex, "SourceCodeNestingLevel": SourceCodeNestingLevel, "SourceCodeRelativeNestingLevel": SourceCodeRelativeNestingLevel, "CurrentSourceCodeTokenStringIndex": CurrentSourceCodeTokenStringIndex, 'StartSourceCodeTokenIndex': SourceCodeTokenIndex, 'StartSourceCodeTokenStringIndex': StartSourceCodeTokenStringIndex})

                                            if (PassInNestingMarkers(MatchTokenIndex, MatchTokenList) != 0 and PassInNestingMarkers(MatchTokenIndex, MatchTokenList)[1] < SubIndex + 1) or (PassInNestingMarkers(SubIndex, MatchTokenList) != 0 and PassInNestingMarkers(SubIndex, MatchTokenList)[0] ==  SubIndex):
                                                BreakFlag = True
                                                break
                                            SourceCodeNestingLevel = StartSourceCodeNestingLevel
                                            SourceCodeRelativeNestingLevel = StartSourceCodeRelativeNestingLevel
                                    else:
                                        if NestingMap[SubIndex][1] == ComprasionSourceCodeRelativeNestingLevel + SourceCodeRelativeNestingLevel or NestingMap[SubIndex][1] == 0:
                                            CurrentSourceCodeTokenIndex = ComparisonSourceCodeTokenIndex
                                            SourceCodeRelativeNestingLevel = SourceCodeRelativeNestingLevel + ComprasionSourceCodeRelativeNestingLevel
                                            SourceCodeNestingLevel = SourceCodeNestingLevel + ComparisonSourceCodeNestingLevel
                                            IsPassOutputDictionary.append({"IndexString": IndexString, "CurrentSourceCodeTokenIndex": CurrentSourceCodeTokenIndex, "SourceCodeNestingLevel": SourceCodeNestingLevel, "SourceCodeRelativeNestingLevel": SourceCodeRelativeNestingLevel,"CurrentSourceCodeTokenStringIndex": CurrentSourceCodeTokenStringIndex, 'StartSourceCodeTokenIndex': SourceCodeTokenIndex, 'StartSourceCodeTokenStringIndex': StartSourceCodeTokenStringIndex})
                                            CounterMatches += 1

                                            if (PassInNestingMarkers(MatchTokenIndex, MatchTokenList) != 0 and PassInNestingMarkers(MatchTokenIndex, MatchTokenList)[1] < SubIndex + 1) or (PassInNestingMarkers(SubIndex, MatchTokenList) != 0 and PassInNestingMarkers(SubIndex, MatchTokenList)[0] ==  SubIndex):
                                                BreakFlag = True
                                                break
                                            SourceCodeNestingLevel = StartSourceCodeNestingLevel
                                            SourceCodeRelativeNestingLevel = StartSourceCodeRelativeNestingLevel
                                        if NestingMap[SubIndex + 1][0] != -1:
                                            SourceCodeRelativeNestingLevel = 0
                            if BreakFlag:
                                break
        else:
            return IsPassDictionary, FlagFirstCircle

    if FlagFirstCircle:
        FlagFirstCircle = False

    return IsPassOutputDictionary, FlagFirstCircle


def IsInsert(MatchTokenList, MatchTokenIndex, SourceCodeTokenList, IsPassDictionaryList, FlagFirstCircle, NestingMap):
    IsInsertIndexDictionaryList = []
    IsInsertOutputDictionaryList = []
    for IsPassDictionary in IsPassDictionaryList:
        CurrentSourceCodeTokenIndex = IsPassDictionary["CurrentSourceCodeTokenIndex"]
        CurrentSourceCodeTokenStringIndex = IsPassDictionary["CurrentSourceCodeTokenStringIndex"]
        IndexString =IsPassDictionary["IndexString"]
        IsPassDictionary = [IsPassDictionary]

        if MatchTokenList[MatchTokenIndex - 1] != '...' and (MatchTokenIndex + 1 == len(MatchTokenList) or MatchTokenList[MatchTokenIndex + 1] == '...'):
            IsInsertIndexDictionaryList.append(FindIsInsertIndex(MatchTokenList, MatchTokenIndex, CurrentSourceCodeTokenStringIndex, CurrentSourceCodeTokenIndex, IndexString, SourceCodeTokenList,  'Prev'))
            IsInsertOutputDictionaryList.extend(IsPassDictionary)

        elif MatchTokenIndex + 1 < len(MatchTokenList) and MatchTokenList[MatchTokenIndex + 1] != '...':
            IsPassOutputDictionaryList, FlagFirstCircle = IsPass(MatchTokenList, MatchTokenIndex, SourceCodeTokenList, IsPassDictionary, FlagFirstCircle, NestingMap)
            if  IsPassOutputDictionaryList:
                IsInsertOutputDictionaryList.extend(IsPassOutputDictionaryList)
                for IsPassOutput in IsPassOutputDictionaryList:
                    StartSourceCodeTokenIndex = IsPassOutput["StartSourceCodeTokenIndex"]
                    StartSourceCodeTokenStringIndex = IsPassOutput["StartSourceCodeTokenStringIndex"]
                    IndexString = IsPassOutput["IndexString"]
                    IsInsertIndexDictionaryList.append(FindIsInsertIndex(MatchTokenList, MatchTokenIndex, StartSourceCodeTokenStringIndex, StartSourceCodeTokenIndex, IndexString, SourceCodeTokenList, 'Next'))

    return IsInsertIndexDictionaryList, IsInsertOutputDictionaryList, FlagFirstCircle

def FindIsInsertIndex(MatchTokenList, MatchTokenIndex, CurrentSourceCodeTokenStringIndex, CurrentSourceCodeTokenIndex, IndexString, SourceCodeTokenList, InsertPosition):
    if len(SourceCodeTokenList[CurrentSourceCodeTokenIndex]) == 1 or InsertPosition == 'Prev':
        InsertIndex ={'IndexString': IndexString, 'CurrentSourceCodeTokenIndex': CurrentSourceCodeTokenIndex, 'CurrentSourceCodeTokenStringIndex': CurrentSourceCodeTokenStringIndex, 'InsertPosition': InsertPosition}
    else:
        InsertIndex = {'IndexString': IndexString, 'CurrentSourceCodeTokenIndex': CurrentSourceCodeTokenIndex, 'CurrentSourceCodeTokenStringIndex': CurrentSourceCodeTokenStringIndex - len(MatchTokenList[MatchTokenIndex + 1]) + 1, 'InsertPosition': InsertPosition}
    return InsertIndex


def GetBracketIndicesForEllipsis(MatchTokenList):
    result = []
    IsNestingMarkerPairsDictionary = CheckMatchNestingMarkerPairs(MatchTokenList)
    for i, MatchToken in enumerate(MatchTokenList):
        if MatchToken == '...' and i > 0:
            CurrentEllipsis = 0
            for BracketIndex, (IsValid, ClosingIndex) in IsNestingMarkerPairsDictionary.items():
                if IsValid and ClosingIndex != -1:
                    if BracketIndex < i < ClosingIndex:
                        CurrentEllipsis = ({"EllipsisIndex": i, "BracketIndex": BracketIndex})
                        break
            if  CurrentEllipsis:
                result.append(CurrentEllipsis)
            else:
                result.append({"EllipsisIndex": i, "BracketIndex": -1})
    return result


def MatchNestingLevelInsertALL(MatchTokenList):
    NestingMap = []
    CounterNesting = 0
    CounterRelativeNesting = 0
    IsNestingDefined = True
    BracketIndicesForEllipsis = GetBracketIndicesForEllipsis(MatchTokenList)
    BetweenEllipsis = set()

    for i, CurentBracket in enumerate(BracketIndicesForEllipsis):
        for NextBracket in BracketIndicesForEllipsis[i + 1:]:
            if CurentBracket['BracketIndex'] == NextBracket['BracketIndex']:
                BetweenEllipsis.update(range(CurentBracket['EllipsisIndex'] + 1, NextBracket['EllipsisIndex']))
    for i, MatchToken in enumerate(MatchTokenList):
        if i in BetweenEllipsis:
            IsNestingDefined, CounterRelativeNesting = CheckCounterNesting( MatchToken, CounterRelativeNesting, IsNestingDefined, i)
            NestingMap.append((-1,CounterRelativeNesting))
        else:
            IsNestingDefined, CounterNesting = CheckCounterNesting( MatchToken, CounterNesting, IsNestingDefined, i)
            NestingMap.append((CounterNesting if IsNestingDefined else -1,0))
    return NestingMap

def CheckCounterNesting( MatchToken,CounterNesting, IsNestingDefined, index):
    if MatchToken == '...' and index > 0:
        if CounterNesting == 0:
            IsNestingDefined = False
    elif MatchToken in OPEN_NESTING_MARKERS:
        CounterNesting += 1
        IsNestingDefined = True
    elif MatchToken in CLOSE_NESTING_MARKERS:
        CounterNesting -= 1
    return IsNestingDefined, CounterNesting

def SearchInsertIndexInSourceCode(MatchTokenList, SourceCodeTokenList):
    InsertIndexInTokenList = SearchInsertIndexInTokenList(MatchTokenList, SourceCodeTokenList)
    if InsertIndexInTokenList == 0:
        return 0
    TokenDirection, [TokenPosition, TokenStringIndex] = list(InsertIndexInTokenList.items())[0]
    TokenValue = SourceCodeTokenList[TokenPosition][TokenStringIndex]
    count = 0

    for i in range(TokenPosition):
        count += SourceCodeTokenList[i].count(TokenValue)

    count += SourceCodeTokenList[TokenPosition][:TokenStringIndex].count(TokenValue)
    return [TokenDirection, count + 1, TokenValue]


def CheckMatchNestingMarkerPairs(MatchTokenList):
    IsNestingMarkerPairsDictionary = {}
    stack = []
    NestingMarkerList = [(i, MatchToken) for i, MatchToken in enumerate(MatchTokenList) if MatchToken in NESTING_MARKERS]
    for index, _ in NestingMarkerList:
        IsNestingMarkerPairsDictionary[index] = [False, -1]
    for i, (IndexOnMatch, NestingMarker) in enumerate(NestingMarkerList):
        if NestingMarker in OPEN_NESTING_MARKERS:
            stack.append((IndexOnMatch, NestingMarker, i))
        elif NestingMarker in CLOSE_NESTING_MARKERS:
            for j in range(len(stack) - 1, -1, -1):
                if stack[j][1] == DICTIONARY_NESTING_MARKERS[NestingMarker]:
                    OpenNestingMarkerIndexOnMatch, _, _ = stack.pop(j)
                    IsNestingMarkerPairsDictionary[OpenNestingMarkerIndexOnMatch] = [True, IndexOnMatch]
                    IsNestingMarkerPairsDictionary[IndexOnMatch] = [True, OpenNestingMarkerIndexOnMatch]
                    break
    return IsNestingMarkerPairsDictionary


def PassInNestingMarkers(IndexPassInMatch, MatchTokenList):
    IsNestingMarkerPairsDictionary = CheckMatchNestingMarkerPairs(MatchTokenList)
    MarkerList = [[index, IsPaired, PairedIndex] for index, [IsPaired, PairedIndex] in IsNestingMarkerPairsDictionary.items()]
    ClosestPair = None
    for index, IsPaired, PairedIndex in MarkerList:
        if IsPaired and index <= IndexPassInMatch <= PairedIndex:
            ClosestPair = [index, PairedIndex]
    if ClosestPair:
        return ClosestPair
    else:
        return 0

def FindAllSubstringEnds(string, substring, substringindex):
    result = []
    while True:
        index = string.find(substring, substringindex)
        if index == -1:
            break
        if index + len(substring) == len(string):
            result.append(index + len(substring) - 1)
        else:
            result.append(index + len(substring))
        substringindex = index + 1
    return result