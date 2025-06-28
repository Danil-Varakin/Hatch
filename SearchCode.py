def SearchInsertIndexInTokenList(MatchTokenList: list[tuple], SourceCodeTokenList: list[tuple]):
    IsPassDictionary = [{"IndexString": "", "CurentSourceCodeTokenIndex": 0, "SourceCodeNestingLevel": 0, "SourceCodeRelativeNestingLevel": 0}]
    FlagFirstCircle = True
    NestingMap = MatchNestingLevelInsertALL(MatchTokenList)

    for MatchTokenIndex in range(len(MatchTokenList)):
        if MatchTokenList[MatchTokenIndex][1] == '...':
            IsPassDictionary, FlagFirstCircle = IsPass(MatchTokenList, MatchTokenIndex, SourceCodeTokenList, IsPassDictionary, FlagFirstCircle, NestingMap)

        if MatchTokenList[MatchTokenIndex][1] == ">>>":
            ResultTokenInsert = IsInsert(MatchTokenList, MatchTokenIndex, SourceCodeTokenList, IsPassDictionary, FlagFirstCircle, NestingMap)
            if ResultTokenInsert:
                return ResultTokenInsert

    return 0


def ComparisonToken(MatchTokenList, MatchTokenIndex, SourceCodeTokenList, SourceCodeTokenIndex, SourceCodeNestingLevel, FlagFirstCircle, SourceCodeRelativeNestingLevel, NestingMap):

    ComparisonIndex = 1
    NumberTokenMatch = 0
    NumberTokenSource = 0
    ComparisonSourceCodeNestingLevel = 0
    ComprasionSourceCodeRelativeNestingLevel = 0

    if FlagFirstCircle:
        if NestingMap[MatchTokenIndex + 1][0] == -1:
            SourceCodeRelativeNestingLevel = SourceNestingLevelChange(SourceCodeRelativeNestingLevel, SourceCodeTokenList, SourceCodeTokenIndex, 0)
        SourceCodeNestingLevel = SourceNestingLevelChange(SourceCodeNestingLevel, SourceCodeTokenList, SourceCodeTokenIndex, 0)

    while MatchTokenIndex + 1 + ComparisonIndex < len(MatchTokenList) and MatchTokenList[MatchTokenIndex + 1 + ComparisonIndex][1] not in ["...", ">>>"]:
        NumberTokenMatch = NumberTokenMatch + 1

        if NestingMap[MatchTokenIndex + 1][0] == -1:
            ComprasionSourceCodeRelativeNestingLevel = SourceNestingLevelChange(ComprasionSourceCodeRelativeNestingLevel, SourceCodeTokenList, SourceCodeTokenIndex, ComparisonIndex)

        ComparisonSourceCodeNestingLevel = SourceNestingLevelChange(ComparisonSourceCodeNestingLevel, SourceCodeTokenList, SourceCodeTokenIndex, ComparisonIndex)

        if MatchTokenList[MatchTokenIndex + 1 + ComparisonIndex][1] != SourceCodeTokenList[SourceCodeTokenIndex + ComparisonIndex][1]:
            ComparisonSourceCodeNestingLevel = 0
            ComprasionSourceCodeRelativeNestingLevel = 0
            break

        NumberTokenSource = NumberTokenSource + 1
        ComparisonIndex = ComparisonIndex + 1

    return ComparisonIndex, NumberTokenMatch, NumberTokenSource, SourceCodeNestingLevel, ComparisonSourceCodeNestingLevel, SourceCodeRelativeNestingLevel, ComprasionSourceCodeRelativeNestingLevel


def SourceNestingLevelChange(SourceCodeNestingLevel, SourceCodeTokenList, SourceCodeTokenIndex, ComparisonIndex):

    if SourceCodeTokenList[SourceCodeTokenIndex + ComparisonIndex][1] in ["{", "(", "["]:
        SourceCodeNestingLevel = SourceCodeNestingLevel + 1

    if SourceCodeTokenList[SourceCodeTokenIndex + ComparisonIndex][1] in ["}", ")", "]"]:
        SourceCodeNestingLevel = SourceCodeNestingLevel - 1

    return SourceCodeNestingLevel


def IsPass(MatchTokenList, MatchTokenIndex, SourceCodeTokenList, IsPassDictionary, FlagFirstCircle, NestingMap):
    
    IsPassOutputDictionary = []

    if IsPassDictionary:
        skip_rest = False
        if MatchTokenIndex + 1 < len(MatchTokenList) and MatchTokenList[MatchTokenIndex + 1][1] == '>>>':
            skip_rest = True

        if not skip_rest:
            for IsPassOutput in IsPassDictionary:
                SourceCodeNestingLevel = IsPassOutput["SourceCodeNestingLevel"]
                SourceCodeRelativeNestingLevel = IsPassOutput["SourceCodeRelativeNestingLevel"]
                StartCurentSourceCodeTokenIndex = IsPassOutput["CurentSourceCodeTokenIndex"]

                CounterMatches = 0

                for SourceCodeTokenIndex in range(StartCurentSourceCodeTokenIndex, len(SourceCodeTokenList)):

                    if MatchTokenIndex + 1 < len(MatchTokenList):
                        if not FlagFirstCircle:
                            if NestingMap[MatchTokenIndex + 1][0] == -1:
                                SourceCodeRelativeNestingLevel = SourceNestingLevelChange(SourceCodeRelativeNestingLevel, SourceCodeTokenList, SourceCodeTokenIndex, 0)
                            else:
                                SourceCodeNestingLevel = SourceNestingLevelChange(SourceCodeNestingLevel, SourceCodeTokenList, SourceCodeTokenIndex, 0)


                        if SourceCodeTokenList[SourceCodeTokenIndex] == MatchTokenList[MatchTokenIndex + 1]:
                            StartSourceCodeRelativeNestingLevel = SourceCodeRelativeNestingLevel
                            StartSourceCodeNestingLevel = SourceCodeNestingLevel

                            ComparisonIndex, NumberTokenMatch, NumberTokenSource, SourceCodeNestingLevel, ComparisonSourceCodeNestingLevel, SourceCodeRelativeNestingLevel, ComprasionSourceCodeRelativeNestingLevel = ComparisonToken(MatchTokenList, MatchTokenIndex, SourceCodeTokenList, SourceCodeTokenIndex, SourceCodeNestingLevel, FlagFirstCircle, SourceCodeRelativeNestingLevel, NestingMap)

                            if NumberTokenSource == NumberTokenMatch:
                                IndexString = IsPassOutput["IndexString"] + str(CounterMatches) + '/'

                                if NestingMap[MatchTokenIndex + ComparisonIndex][0] != -1:
                                    if NestingMap[MatchTokenIndex + ComparisonIndex][0] == SourceCodeNestingLevel + ComparisonSourceCodeNestingLevel:
                                        CurentSourceCodeTokenIndex = ComparisonIndex + SourceCodeTokenIndex
                                        SourceCodeNestingLevel = SourceCodeNestingLevel + ComparisonSourceCodeNestingLevel
                                        CounterMatches += 1
                                        IsPassOutputDictionary.append({"IndexString": IndexString, "CurentSourceCodeTokenIndex": CurentSourceCodeTokenIndex, "SourceCodeNestingLevel": SourceCodeNestingLevel, "SourceCodeRelativeNestingLevel": SourceCodeRelativeNestingLevel})

                                        if (PassInNestingMarkers(MatchTokenIndex, MatchTokenList) != 0 and PassInNestingMarkers(MatchTokenIndex, MatchTokenList)[1] < MatchTokenIndex + ComparisonIndex + 1) or (PassInNestingMarkers(MatchTokenIndex + ComparisonIndex, MatchTokenList) != 0 and PassInNestingMarkers(MatchTokenIndex + ComparisonIndex, MatchTokenList)[0] ==  MatchTokenIndex + ComparisonIndex):
                                            break
                                        SourceCodeNestingLevel = StartSourceCodeNestingLevel
                                        SourceCodeRelativeNestingLevel = StartSourceCodeRelativeNestingLevel
                                else:
                                    if NestingMap[MatchTokenIndex + ComparisonIndex][1] == ComprasionSourceCodeRelativeNestingLevel + SourceCodeRelativeNestingLevel or NestingMap[MatchTokenIndex + ComparisonIndex][1] == 0:
                                        CurentSourceCodeTokenIndex = ComparisonIndex + SourceCodeTokenIndex
                                        SourceCodeRelativeNestingLevel = SourceCodeRelativeNestingLevel + ComprasionSourceCodeRelativeNestingLevel
                                        IsPassOutputDictionary.append({"IndexString": IndexString, "CurentSourceCodeTokenIndex": CurentSourceCodeTokenIndex, "SourceCodeNestingLevel": SourceCodeNestingLevel, "SourceCodeRelativeNestingLevel": SourceCodeRelativeNestingLevel})
                                        CounterMatches += 1

                                        if (PassInNestingMarkers(MatchTokenIndex, MatchTokenList) != 0 and PassInNestingMarkers(MatchTokenIndex, MatchTokenList)[1] < MatchTokenIndex + ComparisonIndex + 1) or (PassInNestingMarkers(MatchTokenIndex + ComparisonIndex, MatchTokenList) != 0 and PassInNestingMarkers(MatchTokenIndex + ComparisonIndex, MatchTokenList)[0] ==  MatchTokenIndex + ComparisonIndex):
                                            break
                                        SourceCodeNestingLevel = StartSourceCodeNestingLevel
                                        SourceCodeRelativeNestingLevel = StartSourceCodeRelativeNestingLevel
                                    if NestingMap[MatchTokenIndex + ComparisonIndex + 1][0] != -1:
                                        SourceCodeRelativeNestingLevel = 0
        else:
            return IsPassDictionary, FlagFirstCircle

    if FlagFirstCircle:
        FlagFirstCircle = False

    return IsPassOutputDictionary, FlagFirstCircle


def IsInsert(MatchTokenList, MatchTokenIndex, SourceCodeTokenList, IsPassDictionary, FlagFirstCircle, NestingMap):
    MatchNestingLevel = InsertNestingLevel(MatchTokenList)

    if MatchTokenIndex > 0 and MatchTokenIndex + 1 < len(MatchTokenList):
        if MatchTokenList[MatchTokenIndex - 1][1] != '...' and MatchTokenList[MatchTokenIndex + 1][1] == '...':
            if len(IsPassDictionary) > 1:
                return 0
            elif len(IsPassDictionary) == 1:
                ResultTokenInsert = {'Prev': IsPassDictionary[0]["CurentSourceCodeTokenIndex"] - 1}
                return ResultTokenInsert

    IsInsertOutputList = []
    if IsPassDictionary:
        for IsPassOutput in IsPassDictionary:
            CurentSourceCodeTokenIndex = IsPassOutput["CurentSourceCodeTokenIndex"]
            SourceCodeNestingLevel = IsPassOutput["SourceCodeNestingLevel"]
            SourceCodeRelativeNestingLevel = IsPassOutput["SourceCodeRelativeNestingLevel"]

            if (MatchTokenList[MatchTokenIndex - 1][1] == "..." and MatchTokenList[MatchTokenIndex + 1][1] != '...') or (MatchTokenList[MatchTokenIndex - 1][1] != "..." and MatchTokenList[MatchTokenIndex + 1][1] != '...'):
                SourceCodeTokenIndex = CurentSourceCodeTokenIndex

                while SourceCodeTokenIndex < len(SourceCodeTokenList):
                    SourceCodeInsertIndex = SourceCodeTokenIndex
                    if MatchTokenIndex != 1:
                        if NestingMap[MatchTokenIndex + 1][0] == -1:
                            SourceCodeRelativeNestingLevel = SourceNestingLevelChange(SourceCodeRelativeNestingLevel, SourceCodeTokenList, SourceCodeTokenIndex, 0)
                        SourceCodeNestingLevel = SourceNestingLevelChange(SourceCodeNestingLevel, SourceCodeTokenList, SourceCodeTokenIndex, 0)

                    if MatchTokenIndex + 1 < len(MatchTokenList):
                        if SourceCodeTokenList[SourceCodeTokenIndex] == MatchTokenList[MatchTokenIndex + 1]:
                            StartSourceCodeRelativeNestingLevel = SourceCodeRelativeNestingLevel
                            StartSourceCodeNestingLevel = SourceCodeNestingLevel

                            ComparisonIndex, NumberTokenMatch, NumberTokenSource, SourceCodeNestingLevel, ComparisonSourceCodeNestingLevel, SourceCodeRelativeNestingLevel, ComprasionSourceCodeRelativeNestingLevel = ComparisonToken(MatchTokenList, MatchTokenIndex, SourceCodeTokenList, SourceCodeTokenIndex, SourceCodeNestingLevel, FlagFirstCircle, SourceCodeRelativeNestingLevel, NestingMap)

                            if NumberTokenSource == NumberTokenMatch:
                                if MatchNestingLevel[0] != -1:
                                    if NestingMap[MatchTokenIndex + ComparisonIndex][0] == SourceCodeNestingLevel + ComparisonSourceCodeNestingLevel:
                                        IsInsertOutputList.append({'Next': SourceCodeInsertIndex})

                                        if (PassInNestingMarkers(MatchTokenIndex, MatchTokenList) != 0 and PassInNestingMarkers(MatchTokenIndex, MatchTokenList)[1] < MatchTokenIndex + ComparisonIndex + 1) or (PassInNestingMarkers(MatchTokenIndex + ComparisonIndex, MatchTokenList) != 0 and PassInNestingMarkers(MatchTokenIndex + ComparisonIndex, MatchTokenList)[0] ==  MatchTokenIndex + ComparisonIndex):
                                            break
                                        SourceCodeNestingLevel = StartSourceCodeNestingLevel
                                        SourceCodeRelativeNestingLevel = StartSourceCodeRelativeNestingLevel
                                        SourceCodeTokenIndex += 1
                                    else:
                                        SourceCodeTokenIndex += 1
                                else:
                                    if NestingMap[MatchTokenIndex + ComparisonIndex][1] == SourceCodeRelativeNestingLevel + ComprasionSourceCodeRelativeNestingLevel:
                                        IsInsertOutputList.append({'Next': SourceCodeInsertIndex})

                                        if (PassInNestingMarkers(MatchTokenIndex, MatchTokenList) != 0 and PassInNestingMarkers(MatchTokenIndex, MatchTokenList)[1] < MatchTokenIndex + ComparisonIndex + 1) or (PassInNestingMarkers(MatchTokenIndex + ComparisonIndex, MatchTokenList) != 0 and PassInNestingMarkers(MatchTokenIndex + ComparisonIndex, MatchTokenList)[0] ==  MatchTokenIndex + ComparisonIndex):
                                            break
                                        SourceCodeNestingLevel = StartSourceCodeNestingLevel
                                        SourceCodeRelativeNestingLevel = StartSourceCodeRelativeNestingLevel
                                        SourceCodeTokenIndex += 1
                                    elif NestingMap[MatchTokenIndex + ComparisonIndex][1] == 0 and MatchTokenList[MatchTokenIndex + ComparisonIndex][1] not in ["}", ")", "]"]:
                                        IsInsertOutputList.append({'Next': SourceCodeInsertIndex})

                                        if (PassInNestingMarkers(MatchTokenIndex, MatchTokenList) != 0 and PassInNestingMarkers(MatchTokenIndex, MatchTokenList)[1] < MatchTokenIndex + ComparisonIndex + 1) or (PassInNestingMarkers(MatchTokenIndex + ComparisonIndex, MatchTokenList) != 0 and PassInNestingMarkers(MatchTokenIndex + ComparisonIndex, MatchTokenList)[0] ==  MatchTokenIndex + ComparisonIndex):
                                            break
                                        SourceCodeNestingLevel = StartSourceCodeNestingLevel
                                        SourceCodeRelativeNestingLevel = StartSourceCodeRelativeNestingLevel
                                        SourceCodeTokenIndex += 1
                                    else:
                                        SourceCodeTokenIndex += 1
                            else:
                                SourceCodeTokenIndex += 1
                        else:
                            SourceCodeTokenIndex += 1

        if len(IsInsertOutputList) > 1 or len(IsInsertOutputList) == 0:
            return 0
        else:
            return IsInsertOutputList[0] if IsInsertOutputList else 0

def InsertNestingLevel(MatchTokenList: list[tuple]):
    NestingMap = MatchNestingLevelInsertALL(MatchTokenList)
    for i, MatchToken in enumerate(MatchTokenList):
        if MatchToken[1] == ">>>":
            return NestingMap[i]
    return 0


def GetBracketIndicesForEllipsis(MatchTokenList: list[tuple]):
    stack = []
    IsNestingMarkerPairsDictionary = CheckMatchNestingMarkerPairs(MatchTokenList)
    IsNestingDefined = True
    result = []
    for i, MatchToken in enumerate(MatchTokenList):
        if MatchToken[1] == '...' and i > 0:
            bracket_index = stack[-1][0] if stack and IsNestingDefined else -1
            result.append({"EllipsisIndex": i, "BracketIndex": bracket_index})
        elif MatchToken[1] in ["{", "(", "["] and IsNestingMarkerPairsDictionary.get(i, [False])[0]:
            stack.append((i, MatchToken[1]))
            IsNestingDefined = True
        elif MatchToken[1] in ["}", ")", "]"] and IsNestingMarkerPairsDictionary.get(i, [False])[0]:
            if stack:
                stack.pop()

    return result


def MatchNestingLevelInsertALL(MatchTokenList: list[tuple]):
    NestingMap = []
    CounterNesting = 0
    CounterRelativeNesting = 0
    IsNestingDefined = True
    BracketIndicesForEllipsis = GetBracketIndicesForEllipsis(MatchTokenList)
    BetweenEllipsis = set()

    for i, CurentBracket in enumerate(BracketIndicesForEllipsis):
        for NextBracket in BracketIndicesForEllipsis[i + 1:]:
            if CurentBracket["BracketIndex"] == NextBracket["BracketIndex"] and CurentBracket["BracketIndex"]:
                BetweenEllipsis.update(range(CurentBracket["EllipsisIndex"] + 1, NextBracket["EllipsisIndex"]))
    for i, MatchToken in enumerate(MatchTokenList):
        if i in BetweenEllipsis:
            IsNestingDefined, CounterRelativeNesting = CheckCounterNesting( MatchToken, CounterRelativeNesting, IsNestingDefined, i)
            NestingMap.append((-1,CounterRelativeNesting))
        else:
            IsNestingDefined, CounterNesting = CheckCounterNesting( MatchToken, CounterNesting, IsNestingDefined, i)
            NestingMap.append((CounterNesting if IsNestingDefined else -1,0))
    return NestingMap

def CheckCounterNesting( MatchToken,CounterNesting, IsNestingDefined, index):
    if MatchToken[1] == '...' and index > 0:
        if CounterNesting == 0:
            IsNestingDefined = False
    elif MatchToken[1] in ["{", "(", "["]:
        CounterNesting += 1
        IsNestingDefined = True
    elif MatchToken[1] in ["}", ")", "]"]:
        CounterNesting -= 1
    return IsNestingDefined, CounterNesting

def SearchInsertIndexInSourseCode(MatchTokenList: list[tuple], SourceCodeTokenList: list[tuple]):
    InsertIndexInTokenList = SearchInsertIndexInTokenList(MatchTokenList, SourceCodeTokenList)
    if InsertIndexInTokenList == 0:
        return 0
    TokenDirection, TokenPosition = list(InsertIndexInTokenList.items())[0]
    TokenValue = SourceCodeTokenList[TokenPosition][1]
    CounterIdenticalToken = 0
    for SourceCodeTokenIndex in range(TokenPosition + 1):
        if SourceCodeTokenList[SourceCodeTokenIndex][1] == TokenValue:
            CounterIdenticalToken = CounterIdenticalToken + 1
    return [TokenDirection, CounterIdenticalToken, TokenValue]


def CheckMatchNestingMarkerPairs(MatchTokenList: list[tuple]):
    IsNestingMarkerPairsDictionary = {}
    stack = []
    DictionaryNestingMarker = {')': '(', '}': '{', ']': '['}
    NestingMarkerList = [(i, MatchToken[1]) for i, MatchToken in enumerate(MatchTokenList) if MatchToken[1] in ["{", "(", "[", "}", ")", "]"]]

    for index, _ in NestingMarkerList:
        IsNestingMarkerPairsDictionary[index] = [False, -1]

    for i, (IndexOnMatch, NestingMarker) in enumerate(NestingMarkerList):
        if NestingMarker in ["{", "(", "["]:
            stack.append((IndexOnMatch, NestingMarker, i))
        elif NestingMarker in ["}", ")", "]"]:
            for j in range(len(stack) - 1, -1, -1):
                if stack[j][1] == DictionaryNestingMarker[NestingMarker]:
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
