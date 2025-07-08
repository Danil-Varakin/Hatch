def SearchInsertIndexInTokenList(MatchTokenList, SourceCodeTokenList):
    IsPassDictionary = [{"IndexString": "", "CurentSourceCodeTokenIndex": 0, "SourceCodeNestingLevel": 0, "SourceCodeRelativeNestingLevel": 0,"MatchTokenEndsInSourceCodeToken": 0}]
    FlagFirstCircle = True
    NestingMap = MatchNestingLevelInsertALL(MatchTokenList)

    for MatchTokenIndex in range(len(MatchTokenList)):
        if MatchTokenList[MatchTokenIndex] == '...':
            IsPassDictionary, FlagFirstCircle = IsPass(MatchTokenList, MatchTokenIndex, SourceCodeTokenList, IsPassDictionary, FlagFirstCircle, NestingMap)

        #if MatchTokenList[MatchTokenIndex] == ">>>":
            #ResultTokenInsert = IsInsert(MatchTokenList, MatchTokenIndex, SourceCodeTokenList, IsPassDictionary, FlagFirstCircle, NestingMap)
            #if ResultTokenInsert:
                #return ResultTokenInsert

    return 0


def ComparisonToken(MatchTokenList, MatchTokenIndex, SourceCodeTokenList, SourceCodeTokenIndex, SourceCodeNestingLevel, FlagFirstCircle, SourceCodeRelativeNestingLevel, NestingMap, MatchTokenEndsInSourceCodeToken):
    ComparisonFlagFirstCircle = True
    SubIndex = MatchTokenIndex + 2
    MatchToken = MatchTokenList[SubIndex]
    ComparisonSourceCodeNestingLevel = 0
    ComprasionSourceCodeRelativeNestingLevel = 0
    ComparisonSourceCodeTokenIndex = SourceCodeTokenIndex
    while SubIndex < len(MatchTokenList) and MatchTokenList[SubIndex] not in ["...", ">>>"]:
        if FlagFirstCircle or not ComparisonFlagFirstCircle:
            if NestingMap[MatchTokenIndex + 1][0] == -1:
                ComprasionSourceCodeRelativeNestingLevel = SourceNestingLevelChange(ComprasionSourceCodeRelativeNestingLevel, SourceCodeTokenList, ComparisonSourceCodeTokenIndex, 0)
            ComparisonSourceCodeNestingLevel = SourceNestingLevelChange(ComparisonSourceCodeNestingLevel, SourceCodeTokenList, ComparisonSourceCodeTokenIndex, 0)
        ComparisonFlagFirstCircle = False
        SourceCodeToken = SourceCodeTokenList[ComparisonSourceCodeTokenIndex]

        if SourceCodeToken[MatchTokenEndsInSourceCodeToken:] == MatchToken:
            SubIndex += 1
            MatchToken = MatchTokenList[SubIndex] if SubIndex < len(MatchTokenList) else ""
            ComparisonSourceCodeTokenIndex += 1
            MatchTokenEndsInSourceCodeToken = 0
        elif SourceCodeToken.startswith(MatchToken, MatchTokenEndsInSourceCodeToken):
            MatchTokenEndsInSourceCodeToken += len(MatchToken)
            SubIndex += 1
            MatchToken = MatchTokenList[SubIndex] if SubIndex < len(MatchTokenList) else ""
        elif len(SourceCodeToken) == MatchTokenEndsInSourceCodeToken + 1 and len(SourceCodeToken) > 1:
            ComparisonSourceCodeTokenIndex += 1
            MatchTokenEndsInSourceCodeToken = 0
        else:
            return False

    return  SourceCodeNestingLevel, ComparisonSourceCodeNestingLevel, SourceCodeRelativeNestingLevel, ComprasionSourceCodeRelativeNestingLevel, MatchTokenEndsInSourceCodeToken, ComparisonSourceCodeTokenIndex, SubIndex


def SourceNestingLevelChange(SourceCodeNestingLevel, SourceCodeTokenList, SourceCodeTokenIndex, ComparisonIndex):

    if SourceCodeTokenList[SourceCodeTokenIndex + ComparisonIndex] in ["{", "(", "["]:
        SourceCodeNestingLevel = SourceCodeNestingLevel + 1

    if SourceCodeTokenList[SourceCodeTokenIndex + ComparisonIndex] in ["}", ")", "]"]:
        SourceCodeNestingLevel = SourceCodeNestingLevel - 1

    return SourceCodeNestingLevel


def IsPass(MatchTokenList, MatchTokenIndex, SourceCodeTokenList, IsPassDictionary, FlagFirstCircle, NestingMap):

    IsPassOutputDictionary = []

    if IsPassDictionary:
        SkipPass = False
        if MatchTokenIndex + 1 < len(MatchTokenList) and MatchTokenList[MatchTokenIndex + 1] == '>>>':
            SkipPass = True

        if not SkipPass:
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
                            SourceCodeNestingLevel = SourceNestingLevelChange(SourceCodeNestingLevel, SourceCodeTokenList, SourceCodeTokenIndex, 0)
                        MatchTokenEndsInSourceCodeTokenList = FindAllSubstringEnds(SourceCodeTokenList[SourceCodeTokenIndex], MatchTokenList[MatchTokenIndex + 1])
                        if MatchTokenEndsInSourceCodeTokenList:
                            StartSourceCodeRelativeNestingLevel = SourceCodeRelativeNestingLevel
                            StartSourceCodeNestingLevel = SourceCodeNestingLevel
                            for MatchTokenEndsInSourceCodeToken in MatchTokenEndsInSourceCodeTokenList:
                                if ComparisonToken(MatchTokenList, MatchTokenIndex, SourceCodeTokenList, SourceCodeTokenIndex, SourceCodeNestingLevel, FlagFirstCircle, SourceCodeRelativeNestingLevel, NestingMap,MatchTokenEndsInSourceCodeToken):
                                    SourceCodeNestingLevel, ComparisonSourceCodeNestingLevel, SourceCodeRelativeNestingLevel, ComprasionSourceCodeRelativeNestingLevel, MatchTokenEndsInSourceCodeToken, ComparisonSourceCodeTokenIndex, SubIndex = ComparisonToken(MatchTokenList, MatchTokenIndex, SourceCodeTokenList, SourceCodeTokenIndex, SourceCodeNestingLevel, FlagFirstCircle, SourceCodeRelativeNestingLevel, NestingMap, MatchTokenEndsInSourceCodeToken)
                                    IndexString = IsPassOutput["IndexString"] + str(CounterMatches) + '/'

                                    if NestingMap[SubIndex][0] != -1:
                                        if NestingMap[SubIndex][0] == SourceCodeNestingLevel + ComparisonSourceCodeNestingLevel:
                                            CurentSourceCodeTokenIndex = ComparisonSourceCodeTokenIndex
                                            SourceCodeNestingLevel = SourceCodeNestingLevel + ComparisonSourceCodeNestingLevel
                                            CounterMatches += 1
                                            IsPassOutputDictionary.append({"IndexString": IndexString, "CurentSourceCodeTokenIndex": CurentSourceCodeTokenIndex, "SourceCodeNestingLevel": SourceCodeNestingLevel, "SourceCodeRelativeNestingLevel": SourceCodeRelativeNestingLevel, "MatchTokenEndsInSourceCodeToken": MatchTokenEndsInSourceCodeToken})

                                            if (PassInNestingMarkers(MatchTokenIndex, MatchTokenList) != 0 and PassInNestingMarkers(MatchTokenIndex, MatchTokenList)[1] < SubIndex + 1) or (PassInNestingMarkers(SubIndex, MatchTokenList) != 0 and PassInNestingMarkers(SubIndex, MatchTokenList)[0] ==  SubIndex):
                                                break
                                            SourceCodeNestingLevel = StartSourceCodeNestingLevel
                                            SourceCodeRelativeNestingLevel = StartSourceCodeRelativeNestingLevel
                                    else:
                                        if NestingMap[SubIndex][1] == ComprasionSourceCodeRelativeNestingLevel + SourceCodeRelativeNestingLevel or NestingMap[SubIndex][1] == 0:
                                            CurentSourceCodeTokenIndex = ComparisonSourceCodeTokenIndex
                                            SourceCodeRelativeNestingLevel = SourceCodeRelativeNestingLevel + ComprasionSourceCodeRelativeNestingLevel
                                            IsPassOutputDictionary.append({"IndexString": IndexString, "CurentSourceCodeTokenIndex": CurentSourceCodeTokenIndex, "SourceCodeNestingLevel": SourceCodeNestingLevel, "SourceCodeRelativeNestingLevel": SourceCodeRelativeNestingLevel,"MatchTokenEndsInSourceCodeToken": MatchTokenEndsInSourceCodeToken})
                                            CounterMatches += 1

                                            if (PassInNestingMarkers(MatchTokenIndex, MatchTokenList) != 0 and PassInNestingMarkers(MatchTokenIndex, MatchTokenList)[1] < SubIndex + 1) or (PassInNestingMarkers(SubIndex, MatchTokenList) != 0 and PassInNestingMarkers(SubIndex, MatchTokenList)[0] ==  SubIndex):
                                                break
                                            SourceCodeNestingLevel = StartSourceCodeNestingLevel
                                            SourceCodeRelativeNestingLevel = StartSourceCodeRelativeNestingLevel
                                        if NestingMap[SubIndex + 1][0] != -1:
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
    elif len(MatchTokenList) == MatchTokenIndex + 1 and MatchTokenIndex > 0 and MatchTokenList[MatchTokenIndex - 1]:
        return {'Prev': len(SourceCodeTokenList) - 1}
    elif MatchTokenIndex == 0 and len(MatchTokenList) > 1 and MatchTokenList[MatchTokenIndex + 1]:
        return {'Next': 0}
def InsertNestingLevel(MatchTokenList: list[tuple]):
    NestingMap = MatchNestingLevelInsertALL(MatchTokenList)
    for i, MatchToken in enumerate(MatchTokenList):
        if MatchToken[1] == ">>>":
            return NestingMap[i]
    return 0


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
    elif MatchToken in ["{", "(", "["]:
        CounterNesting += 1
        IsNestingDefined = True
    elif MatchToken in ["}", ")", "]"]:
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


def CheckMatchNestingMarkerPairs(MatchTokenList):
    IsNestingMarkerPairsDictionary = {}
    stack = []
    DictionaryNestingMarker = {')': '(', '}': '{', ']': '['}
    NestingMarkerList = [(i, MatchToken) for i, MatchToken in enumerate(MatchTokenList) if MatchToken in ["{", "(", "[", "}", ")", "]"]]
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

def FindAllSubstringEnds(string, substring):
    result = []
    CurrentPos = 0
    while True:
        index = string.find(substring, CurrentPos)
        if index == -1:
            break
        result.append(index + len(substring) -1)
        CurrentPos = index + 1
    return result