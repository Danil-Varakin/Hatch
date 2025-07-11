def SearchInsertIndexInTokenList(MatchTokenList, SourceCodeTokenList):
    IsPassDictionary = [{"IndexString": "", "CurrentSourceCodeTokenIndex": 0, "SourceCodeNestingLevel": 0, "SourceCodeRelativeNestingLevel": 0,"CurrentSourceCodeTokenStringIndex": 0}]
    FlagFirstCircle = True
    NestingMap = MatchNestingLevelInsertALL(MatchTokenList)

    for MatchTokenIndex in range(len(MatchTokenList)):
        if MatchTokenList[MatchTokenIndex] == '...':
            IsPassDictionary, FlagFirstCircle = IsPass(MatchTokenList, MatchTokenIndex, SourceCodeTokenList, IsPassDictionary, FlagFirstCircle, NestingMap)

        if MatchTokenList[MatchTokenIndex] == ">>>":
            ResultTokenInsert = IsInsert(MatchTokenList, MatchTokenIndex, SourceCodeTokenList, IsPassDictionary, FlagFirstCircle, NestingMap)
            if ResultTokenInsert:
                return ResultTokenInsert

    return 0


def ComparisonToken(MatchTokenList, MatchTokenIndex, SourceCodeTokenList, SourceCodeTokenIndex, SourceCodeNestingLevel, FlagFirstCircle, SourceCodeRelativeNestingLevel, NestingMap, CurrentSourceCodeTokenStringIndex):
    ComparisonFlagFirstCircle = True
    SubIndex = MatchTokenIndex + 2
    MatchToken = MatchTokenList[SubIndex]
    ComparisonSourceCodeNestingLevel = 0
    ComprasionSourceCodeRelativeNestingLevel = 0
    ComparisonSourceCodeTokenIndex = SourceCodeTokenIndex
    while SubIndex < len(MatchTokenList) and MatchTokenList[SubIndex] not in ["...", ">>>"]:
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
    if MatchTokenList[MatchTokenIndex + 2] in ["...", ">>>"]:
        if len(SourceCodeTokenList[SourceCodeTokenIndex]) == CurrentSourceCodeTokenStringIndex + 1:
            ComparisonSourceCodeTokenIndex += 1
            CurrentSourceCodeTokenStringIndex = 0
    return  SourceCodeNestingLevel, ComparisonSourceCodeNestingLevel, SourceCodeRelativeNestingLevel, ComprasionSourceCodeRelativeNestingLevel, CurrentSourceCodeTokenStringIndex, ComparisonSourceCodeTokenIndex, SubIndex -1


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
                                            IsPassOutputDictionary.append({"IndexString": IndexString, "CurrentSourceCodeTokenIndex": CurrentSourceCodeTokenIndex, "SourceCodeNestingLevel": SourceCodeNestingLevel, "SourceCodeRelativeNestingLevel": SourceCodeRelativeNestingLevel, "CurrentSourceCodeTokenStringIndex": CurrentSourceCodeTokenStringIndex})

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
                                            IsPassOutputDictionary.append({"IndexString": IndexString, "CurrentSourceCodeTokenIndex": CurrentSourceCodeTokenIndex, "SourceCodeNestingLevel": SourceCodeNestingLevel, "SourceCodeRelativeNestingLevel": SourceCodeRelativeNestingLevel,"CurrentSourceCodeTokenStringIndex": CurrentSourceCodeTokenStringIndex})
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


def IsInsert(MatchTokenList, MatchTokenIndex, SourceCodeTokenList, IsPassDictionary, FlagFirstCircle, NestingMap):
    MatchNestingLevel = InsertNestingLevel(MatchTokenList)

    if MatchTokenIndex > 0 and MatchTokenIndex + 1 < len(MatchTokenList):
        if MatchTokenList[MatchTokenIndex - 1] != '...' and MatchTokenList[MatchTokenIndex + 1] == '...':
            if len(IsPassDictionary) > 1:
                return 0
            elif len(IsPassDictionary) == 1:
                if IsPassDictionary[0]["CurrentSourceCodeTokenStringIndex"] == 0:
                    CurrentSourceCodeTokenIndex = IsPassDictionary[0]["CurrentSourceCodeTokenIndex"] - 1
                    CurrentSourceCodeTokenStringIndex = len(SourceCodeTokenList[CurrentSourceCodeTokenIndex]) - 1
                else:
                    CurrentSourceCodeTokenIndex = IsPassDictionary[0]["CurrentSourceCodeTokenIndex"]
                    CurrentSourceCodeTokenStringIndex = IsPassDictionary[0]["CurrentSourceCodeTokenStringIndex"] - 1
                ResultTokenInsert = {'Prev': [CurrentSourceCodeTokenIndex,CurrentSourceCodeTokenStringIndex]}
                return ResultTokenInsert

        if (MatchTokenList[MatchTokenIndex - 1] == "..." and MatchTokenList[MatchTokenIndex + 1] != '...') or (MatchTokenList[MatchTokenIndex - 1] != "..." and MatchTokenList[MatchTokenIndex + 1] != '...'):
            IsInsertOutputList = []
            if IsPassDictionary:
                for IsPassOutput in IsPassDictionary:
                    CurrentSourceCodeTokenIndex = IsPassOutput["CurrentSourceCodeTokenIndex"]
                    SourceCodeNestingLevel = IsPassOutput["SourceCodeNestingLevel"]
                    SourceCodeRelativeNestingLevel = IsPassOutput["SourceCodeRelativeNestingLevel"]
                    SourceCodeTokenStringIndex = IsPassOutput["CurrentSourceCodeTokenStringIndex"]
                    SourceCodeTokenIndex = CurrentSourceCodeTokenIndex
                    BreakFlag = False

                    while SourceCodeTokenIndex < len(SourceCodeTokenList):
                        SourceCodeInsertIndex = SourceCodeTokenIndex
                        if not FlagFirstCircle:
                            if NestingMap[MatchTokenIndex + 1][0] == -1:
                                SourceCodeRelativeNestingLevel = SourceNestingLevelChange(SourceCodeRelativeNestingLevel, SourceCodeTokenList, SourceCodeTokenIndex, 0)
                            SourceCodeNestingLevel = SourceNestingLevelChange(SourceCodeNestingLevel, SourceCodeTokenList, SourceCodeTokenIndex, 0)

                        if MatchTokenIndex + 1 < len(MatchTokenList):
                            MatchTokenEndsInSourceCodeTokenList = FindAllSubstringEnds( SourceCodeTokenList[SourceCodeTokenIndex], MatchTokenList[MatchTokenIndex + 1],SourceCodeTokenStringIndex)
                            SourceCodeTokenStringIndex = 0
                            if MatchTokenEndsInSourceCodeTokenList:
                                StartSourceCodeRelativeNestingLevel = SourceCodeRelativeNestingLevel
                                StartSourceCodeNestingLevel = SourceCodeNestingLevel

                                for StartSourceCodeTokenStringIndex in MatchTokenEndsInSourceCodeTokenList:
                                    ComparisonTokenResults = ComparisonToken(MatchTokenList, MatchTokenIndex,SourceCodeTokenList, SourceCodeTokenIndex,SourceCodeNestingLevel, FlagFirstCircle,SourceCodeRelativeNestingLevel, NestingMap,StartSourceCodeTokenStringIndex)
                                    if ComparisonTokenResults:
                                        SourceCodeNestingLevel, ComparisonSourceCodeNestingLevel, SourceCodeRelativeNestingLevel, ComprasionSourceCodeRelativeNestingLevel, CurrentSourceCodeTokenStringIndex, ComparisonSourceCodeTokenIndex, SubIndex = ComparisonTokenResults
                                        if MatchNestingLevel[0] != -1:
                                            if NestingMap[SubIndex][0] == SourceCodeNestingLevel + ComparisonSourceCodeNestingLevel:
                                                if len(SourceCodeTokenList[SourceCodeInsertIndex]) == 1:
                                                    IsInsertOutputList.append({'Next': [SourceCodeInsertIndex, StartSourceCodeTokenStringIndex]})
                                                else:
                                                    IsInsertOutputList.append({'Next': [SourceCodeInsertIndex, StartSourceCodeTokenStringIndex - len(MatchTokenList[MatchTokenIndex + 1])]})

                                                if (PassInNestingMarkers(MatchTokenIndex, MatchTokenList) != 0 and PassInNestingMarkers(MatchTokenIndex, MatchTokenList)[1] < SubIndex + 1) or (PassInNestingMarkers(SubIndex, MatchTokenList) != 0 and PassInNestingMarkers(SubIndex, MatchTokenList)[0] ==  SubIndex):
                                                    BreakFlag = True
                                                    break
                                                SourceCodeNestingLevel = StartSourceCodeNestingLevel
                                                SourceCodeRelativeNestingLevel = StartSourceCodeRelativeNestingLevel
                                                SourceCodeTokenIndex += 1
                                            else:
                                                SourceCodeTokenIndex += 1
                                        else:
                                            if NestingMap[SubIndex][1] == SourceCodeRelativeNestingLevel + ComprasionSourceCodeRelativeNestingLevel:
                                                if len(SourceCodeTokenList[SourceCodeInsertIndex]) == 1:
                                                    IsInsertOutputList.append({'Next': [SourceCodeInsertIndex, StartSourceCodeTokenStringIndex]})
                                                else:
                                                    IsInsertOutputList.append({'Next': [SourceCodeInsertIndex, StartSourceCodeTokenStringIndex - len(MatchTokenList[MatchTokenIndex + 1])]})

                                                if (PassInNestingMarkers(MatchTokenIndex, MatchTokenList) != 0 and PassInNestingMarkers(MatchTokenIndex, MatchTokenList)[1] < SubIndex + 1) or (PassInNestingMarkers(SubIndex, MatchTokenList) != 0 and PassInNestingMarkers(SubIndex, MatchTokenList)[0] ==  SubIndex):
                                                    BreakFlag = True
                                                    break
                                                SourceCodeNestingLevel = StartSourceCodeNestingLevel
                                                SourceCodeRelativeNestingLevel = StartSourceCodeRelativeNestingLevel
                                                SourceCodeTokenIndex += 1
                                            elif NestingMap[SubIndex][1] == 0 and MatchTokenList[SubIndex][1] not in ["}", ")", "]"]:
                                                if len(SourceCodeTokenList[SourceCodeInsertIndex]) == 1:
                                                    IsInsertOutputList.append({'Next': [SourceCodeInsertIndex, StartSourceCodeTokenStringIndex]})
                                                else:
                                                    IsInsertOutputList.append({'Next': [SourceCodeInsertIndex, StartSourceCodeTokenStringIndex - len(MatchTokenList[MatchTokenIndex + 1])]})

                                                if (PassInNestingMarkers(MatchTokenIndex, MatchTokenList) != 0 and PassInNestingMarkers(MatchTokenIndex, MatchTokenList)[1] < SubIndex + 1) or (PassInNestingMarkers(SubIndex, MatchTokenList) != 0 and PassInNestingMarkers(SubIndex, MatchTokenList)[0] ==  SubIndex):
                                                    BreakFlag = True
                                                    break
                                                SourceCodeNestingLevel = StartSourceCodeNestingLevel
                                                SourceCodeRelativeNestingLevel = StartSourceCodeRelativeNestingLevel
                                                SourceCodeTokenIndex += 1
                                            else:
                                                SourceCodeTokenIndex += 1
                                    else:
                                        SourceCodeTokenIndex += 1
                                if BreakFlag:
                                    break
                            else:
                                SourceCodeTokenIndex += 1

            if len(IsInsertOutputList) > 1 or len(IsInsertOutputList) == 0:
                return 0
            else:
                return IsInsertOutputList[0] if IsInsertOutputList else 0
    elif len(MatchTokenList) == MatchTokenIndex + 1 and MatchTokenIndex > 0 and MatchTokenList[MatchTokenIndex - 1]:
        return {'Prev': [len(SourceCodeTokenList) - 1, len(SourceCodeTokenList[len(SourceCodeTokenList) - 1]) - 1]}
    elif MatchTokenIndex == 0 and len(MatchTokenList) > 1 and MatchTokenList[MatchTokenIndex + 1]:
        return {'Next': [0,0]}
    return 0


def InsertNestingLevel(MatchTokenList: list[tuple]):
    NestingMap = MatchNestingLevelInsertALL(MatchTokenList)
    for i, MatchToken in enumerate(MatchTokenList):
        if MatchToken == ">>>":
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