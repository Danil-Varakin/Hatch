from constants import SPECIAL_OPERATORS, OPEN_NESTING_MARKERS, CLOSE_NESTING_MARKERS, NESTING_MARKERS, DICTIONARY_NESTING_MARKERS, PASS_OPERATORS
from  Utilities import IsPassToN
import copy
import re

def SearchInsertIndexInTokenList(MatchTokenList, SourceCodeTokenList):
    try:
        SourceCodeRelativeNestingLevel = {i: [0, True] for i in range(1, len(TokenInBetweenEllipsis(MatchTokenList)) + 1)}
        IsPassDictionaryList = [{"IndexString": "", "CurrentSourceCodeTokenIndex": 0, "SourceCodeNestingLevel": 0, "SourceCodeRelativeNestingLevel": SourceCodeRelativeNestingLevel,"CurrentSourceCodeTokenStringIndex": 0, 'StartSourceCodeTokenIndex': 0, 'StartSourceCodeTokenStringIndex': 0}]
        IsInsertIndexDictionaryList = []
        IsReplaceIndexDictionaryList = []
        FlagFirstCircle = True
        NestingMap = MatchNestingLevelInsertALL(MatchTokenList)
        BracketIndexInSourceCodeList = []
        for MatchTokenIndex in range(len(MatchTokenList)):
            if MatchTokenList[MatchTokenIndex] in PASS_OPERATORS or IsPassToN(MatchTokenList[MatchTokenIndex]):
                IsPassDictionaryList, FlagFirstCircle, BracketIndexInSourceCodeList = IsPass(MatchTokenList, MatchTokenIndex, SourceCodeTokenList, IsPassDictionaryList, FlagFirstCircle, NestingMap, BracketIndexInSourceCodeList)
            if MatchTokenList[MatchTokenIndex] == ">>>":
                IsInsertIndexDictionaryList, IsPassDictionaryList, FlagFirstCircle, BracketIndexInSourceCodeList = IsInsert(MatchTokenList, MatchTokenIndex, SourceCodeTokenList, IsPassDictionaryList, FlagFirstCircle, NestingMap, BracketIndexInSourceCodeList)
            if MatchTokenList[MatchTokenIndex] == "<<<":
                if IsInsertIndexDictionaryList:
                    IsReplaceIndexDictionaryList, IsPassDictionaryList, FlagFirstCircle, BracketIndexInSourceCodeList = IsInsert(MatchTokenList, MatchTokenIndex, SourceCodeTokenList, IsPassDictionaryList, FlagFirstCircle, NestingMap, BracketIndexInSourceCodeList)
                else: raise ValueError("The insertion location was not found")
            if not IsPassDictionaryList:
                raise ValueError("Part of the pattern was not found")
        result = CollectingResultsIndexInTokenList(IsInsertIndexDictionaryList, IsPassDictionaryList, IsReplaceIndexDictionaryList)
        if result:
            return result
        else:
            raise ValueError("Pattern is not unique")
    except ValueError as e:
        print(f"Logic error: {e}")
        return  None



def CollectingResultsIndexInTokenList( IsInsertIndexDictionaryList, IsPassDictionaryList, IsReplaceIndexDictionaryList):
    if len(IsPassDictionaryList) == 1 and IsInsertIndexDictionaryList:
        result = {}
        PassIndexString = IsPassDictionaryList[0]["IndexString"]
        if IsReplaceIndexDictionaryList:
            for IsReplaceIndexDictionary in IsReplaceIndexDictionaryList:
                ReplaceIndexString = IsReplaceIndexDictionary["IndexString"]
                if ReplaceIndexString == PassIndexString[:len(ReplaceIndexString)]:
                    result.update({"ReplaceSourceCodeTokenStringIndex": IsReplaceIndexDictionary["CurrentSourceCodeTokenStringIndex"], "ReplaceSourceCodeTokenIndex": IsReplaceIndexDictionary["CurrentSourceCodeTokenIndex"], "ReplacePosition": IsReplaceIndexDictionary["InsertPosition"]})
                    break
        for IsInsertIndexDictionary in IsInsertIndexDictionaryList:
            InsertIndexString = IsInsertIndexDictionary["IndexString"]
            if InsertIndexString == PassIndexString[:len(InsertIndexString)]:
                result.update({"InsertSourceCodeTokenStringIndex": IsInsertIndexDictionary["CurrentSourceCodeTokenStringIndex"], "InsertSourceCodeTokenIndex": IsInsertIndexDictionary["CurrentSourceCodeTokenIndex"], "InsertPosition": IsInsertIndexDictionary["InsertPosition"]})
                break
    else:
        return 0
    return result

def FindAllSubstringEnds(string, SubString, SubStringIndex):
    result = []
    while True:
        index = string.find(SubString, SubStringIndex)
        if SubString in NESTING_MARKERS and len(string) > 1 or index == -1:
            break
        result.append(index + len(SubString) - 1)
        SubStringIndex = index + 1
    return result

def ComparisonToken(MatchTokenList, MatchTokenIndex, SourceCodeTokenList, SourceCodeTokenIndex, NestingMap, CurrentSourceCodeTokenStringIndex, SourceCodeNestingLevel, IndexString):
    BracketIndexInSourceCodeList = []
    ComparisonFlagFirstCircle = True
    CompressionSourceCodeRelativeNestingLevel = 0
    ComparisonSourceCodeNestingLevel = 0
    CurrentSourceCodeTokenStringIndex += 1
    ComparisonSourceCodeTokenIndex = SourceCodeTokenIndex
    SubIndex = MatchTokenIndex + 2
    if SubIndex < len(MatchTokenList):
        MatchToken = MatchTokenList[SubIndex]
        while SubIndex < len(MatchTokenList)  and ComparisonSourceCodeTokenIndex < len(SourceCodeTokenList) and MatchTokenList[SubIndex] not in SPECIAL_OPERATORS and not IsPassToN(MatchTokenList[SubIndex]):
            SourceCodeToken = SourceCodeTokenList[ComparisonSourceCodeTokenIndex]

            if not ComparisonFlagFirstCircle:
                if NestingMap[SubIndex][0] <= -1:
                    CompressionSourceCodeRelativeNestingLevel = NestingLevelChange(CompressionSourceCodeRelativeNestingLevel, SourceCodeTokenList, ComparisonSourceCodeTokenIndex)
                ComparisonSourceCodeNestingLevel = NestingLevelChange(ComparisonSourceCodeNestingLevel, SourceCodeTokenList, ComparisonSourceCodeTokenIndex)
            ComparisonFlagFirstCircle = False
            if MatchToken in NESTING_MARKERS and SourceCodeToken == MatchToken:
                BracketIndexInSourceCodeList.extend(IndexNestingMarkersInSourceCode(MatchTokenList, MatchTokenIndex, SourceCodeTokenIndex, SubIndex, ComparisonSourceCodeNestingLevel, SourceCodeNestingLevel, IndexString))

            if SourceCodeToken[CurrentSourceCodeTokenStringIndex:] == MatchToken:
                SubIndex += 1
                MatchToken = MatchTokenList[SubIndex] if SubIndex < len(MatchTokenList) else ""
                ComparisonSourceCodeTokenIndex += 1
                CurrentSourceCodeTokenStringIndex = 0
            elif SourceCodeToken.startswith(MatchToken, CurrentSourceCodeTokenStringIndex):
                CurrentSourceCodeTokenStringIndex += len(MatchToken)
                SubIndex += 1
                MatchToken = MatchTokenList[SubIndex] if SubIndex < len(MatchTokenList) else ""
            elif len(SourceCodeToken) <= CurrentSourceCodeTokenStringIndex and( len(SourceCodeToken) > 1 or ComparisonSourceCodeTokenIndex == SourceCodeTokenIndex):
                ComparisonSourceCodeTokenIndex += 1
                CurrentSourceCodeTokenStringIndex = 0
            elif MatchToken in NESTING_MARKERS and len(SourceCodeToken) > 1:
                return False
            else:
                return False
    if (MatchTokenIndex + 2 >= len(MatchTokenList) or MatchTokenList[MatchTokenIndex + 2] in SPECIAL_OPERATORS or IsPassToN(MatchTokenList[MatchTokenIndex + 2])) and MatchTokenList[MatchTokenIndex + 1] == SourceCodeTokenList[ComparisonSourceCodeTokenIndex]:
        BracketIndexInSourceCodeList.extend(IndexNestingMarkersInSourceCode(MatchTokenList, MatchTokenIndex, SourceCodeTokenIndex, MatchTokenIndex + 1, ComparisonSourceCodeNestingLevel, SourceCodeNestingLevel, IndexString))
    if not SubIndex < len(MatchTokenList) or MatchTokenList[MatchTokenIndex + 2] in SPECIAL_OPERATORS or IsPassToN(MatchTokenList[MatchTokenIndex + 2]):
        if  len(SourceCodeTokenList[SourceCodeTokenIndex]) <= CurrentSourceCodeTokenStringIndex and ComparisonSourceCodeTokenIndex + 1 < len(SourceCodeTokenList):
            ComparisonSourceCodeTokenIndex += 1
            CurrentSourceCodeTokenStringIndex = 0
        elif len(SourceCodeTokenList) <= ComparisonSourceCodeTokenIndex and len(SourceCodeTokenList[SourceCodeTokenIndex]) <= CurrentSourceCodeTokenStringIndex:
            CurrentSourceCodeTokenStringIndex = ComparisonSourceCodeTokenIndex - 1
    return   ComparisonSourceCodeNestingLevel, CompressionSourceCodeRelativeNestingLevel, CurrentSourceCodeTokenStringIndex, ComparisonSourceCodeTokenIndex, SubIndex -1, BracketIndexInSourceCodeList


def NestingLevelChange(NestingLevel, TokenList, TokenIndex):

    if TokenList[TokenIndex] in OPEN_NESTING_MARKERS:
        NestingLevel = NestingLevel + 1

    if TokenList[TokenIndex] in CLOSE_NESTING_MARKERS:
        NestingLevel = NestingLevel - 1

    return NestingLevel

def IsPass(MatchTokenList, MatchTokenIndex, SourceCodeTokenList, IsPassDictionary, FlagFirstCircle, NestingMap, BracketIndexInSourceCodeList):
    IsPassOutputDictionary = []
    LastSearchToken = len(MatchTokenList) - 1
    NestingMarkersIndexesForTokenList = TokensInNestingMarkersAll(MatchTokenList)
    for MatchIndex in range(MatchTokenIndex + 1, len(MatchTokenList)):
        if MatchTokenList[MatchIndex] in SPECIAL_OPERATORS or IsPassToN(MatchTokenList[MatchIndex]):
            LastSearchToken = MatchIndex - 1
            break

    if IsPassDictionary:
        SkipPass = False
        if (MatchTokenIndex + 1 < len(MatchTokenList) and (MatchTokenList[MatchTokenIndex + 1] in SPECIAL_OPERATORS or IsPassToN(MatchTokenList[MatchTokenIndex + 1]))) or MatchTokenIndex + 1 == len(MatchTokenList):
            SkipPass = True

        if not SkipPass:
            for IsPassOutput in IsPassDictionary:
                SourceCodeNestingLevel = IsPassOutput["SourceCodeNestingLevel"]
                SourceCodeRelativeNestingLevel = IsPassOutput["SourceCodeRelativeNestingLevel"]
                StartCurrentSourceCodeTokenIndex = IsPassOutput["CurrentSourceCodeTokenIndex"]
                SourceCodeTokenStringIndex = IsPassOutput["CurrentSourceCodeTokenStringIndex"]
                CounterMatches = 0
                BreakFlag = False
                BreakFlagCompression = False
                for SourceCodeTokenIndex in range(StartCurrentSourceCodeTokenIndex, len(SourceCodeTokenList)):

                    if MatchTokenIndex + 1 < len(MatchTokenList):
                        if not FlagFirstCircle:
                            if NestingMap[MatchTokenIndex + 1][0] <= -1  and SourceCodeRelativeNestingLevel[-(NestingMap[MatchTokenIndex + 1][0])][1] == False:
                                SourceCodeRelativeNestingLevel[-(NestingMap[MatchTokenIndex + 1][0])][0] = NestingLevelChange(SourceCodeRelativeNestingLevel[-(NestingMap[MatchTokenIndex + 1][0])][0], SourceCodeTokenList, SourceCodeTokenIndex)
                            SourceCodeNestingLevel = NestingLevelChange(SourceCodeNestingLevel, SourceCodeTokenList, SourceCodeTokenIndex)
                        CompressionIndexString = IsPassOutput["IndexString"] + str(CounterMatches) + '/'
                        for (MatchBracketIndex, SourceCodeBracketIndex, SourceCodeBracketNestingLevel, IndexString) in BracketIndexInSourceCodeList:
                            if NestingMarkersIndexesForTokenList[LastSearchToken][0] == MatchBracketIndex and SourceCodeBracketNestingLevel > SourceCodeNestingLevel and  CompressionIndexString[0:len(IndexString)] == IndexString:
                                if SourceCodeTokenList[SourceCodeTokenIndex] in CLOSE_NESTING_MARKERS:
                                    BreakFlagCompression = True
                                else:
                                    BreakFlag = True
                                break
                        if BreakFlag:
                            break
                        MatchTokenEndsInSourceCodeTokenList = FindAllSubstringEnds(SourceCodeTokenList[SourceCodeTokenIndex], MatchTokenList[MatchTokenIndex + 1], SourceCodeTokenStringIndex)
                        SourceCodeTokenStringIndex = 0
                        StartSourceCodeRelativeNestingLevel = copy.deepcopy(SourceCodeRelativeNestingLevel)
                        StartSourceCodeNestingLevel = SourceCodeNestingLevel
                        if MatchTokenEndsInSourceCodeTokenList:

                            if NestingMap[MatchTokenIndex + 1][0] <= -1 and SourceCodeRelativeNestingLevel[-(NestingMap[MatchTokenIndex + 1][0])][1] == True:
                                SourceCodeRelativeNestingLevel[-(NestingMap[MatchTokenIndex + 1][0])][0] = NestingLevelChange(SourceCodeRelativeNestingLevel[-(NestingMap[MatchTokenIndex + 1][0])][0], SourceCodeTokenList, SourceCodeTokenIndex)
                            if FlagFirstCircle:
                                SourceCodeNestingLevel = NestingLevelChange(SourceCodeNestingLevel, SourceCodeTokenList, SourceCodeTokenIndex)

                            for CurrentSourceCodeTokenStringIndex in MatchTokenEndsInSourceCodeTokenList:
                                StartSourceCodeTokenStringIndex = CurrentSourceCodeTokenStringIndex
                                ComparisonTokenResults = ComparisonToken(MatchTokenList, MatchTokenIndex, SourceCodeTokenList, SourceCodeTokenIndex, NestingMap,CurrentSourceCodeTokenStringIndex, SourceCodeNestingLevel, IsPassOutput["IndexString"] + str(CounterMatches) + '/')
                                if ComparisonTokenResults:
                                    ComparisonSourceCodeNestingLevel, CompressionSourceCodeRelativeNestingLevel, CurrentSourceCodeTokenStringIndex, ComparisonSourceCodeTokenIndex, SubIndex, ComparisonBracketIndexInSourceCodeList = ComparisonTokenResults
                                    IndexString = IsPassOutput["IndexString"] + str(CounterMatches) + '/'

                                    if NestingMap[SubIndex][0] > -1:
                                        if NestingMap[SubIndex][0] == SourceCodeNestingLevel + ComparisonSourceCodeNestingLevel:
                                            CurrentSourceCodeTokenIndex = ComparisonSourceCodeTokenIndex
                                            SourceCodeNestingLevel = SourceCodeNestingLevel + ComparisonSourceCodeNestingLevel
                                            BracketIndexInSourceCodeList.extend(ComparisonBracketIndexInSourceCodeList)
                                            BreakFlagCompression, IsPassOutputDictionary, CounterMatches = AddToIsPassDictionary(MatchTokenList, MatchTokenIndex, SourceCodeTokenIndex, CurrentSourceCodeTokenIndex, CurrentSourceCodeTokenStringIndex, StartSourceCodeTokenStringIndex, SourceCodeNestingLevel, SourceCodeRelativeNestingLevel, IsPassOutputDictionary, IndexString, CounterMatches)
                                            if BreakFlagCompression:
                                                break

                                        SourceCodeNestingLevel = StartSourceCodeNestingLevel
                                    else:
                                        if NestingMap[SubIndex][1] == CompressionSourceCodeRelativeNestingLevel + SourceCodeRelativeNestingLevel[-(NestingMap[SubIndex + 1][0])][0] or NestingMap[SubIndex][1] == 0:
                                            SourceCodeRelativeNestingLevel[-(NestingMap[SubIndex + 1][0])][0] = SourceCodeRelativeNestingLevel[-(NestingMap[SubIndex + 1][0])][0] + CompressionSourceCodeRelativeNestingLevel
                                            CurrentSourceCodeTokenIndex = ComparisonSourceCodeTokenIndex
                                            SourceCodeNestingLevel = SourceCodeNestingLevel + ComparisonSourceCodeNestingLevel
                                            BracketIndexInSourceCodeList.extend(ComparisonBracketIndexInSourceCodeList)
                                            if LastSearchToken + 2 < len(MatchTokenList) and NestingMap[LastSearchToken + 2][0] ==  NestingMap[MatchTokenIndex + 1][0]:
                                                SourceCodeRelativeNestingLevel[-(NestingMap[MatchTokenIndex + 1][0])][1] = False
                                            BreakFlagCompression, IsPassOutputDictionary, CounterMatches = AddToIsPassDictionary(MatchTokenList, MatchTokenIndex, SourceCodeTokenIndex, CurrentSourceCodeTokenIndex, CurrentSourceCodeTokenStringIndex, StartSourceCodeTokenStringIndex, SourceCodeNestingLevel, SourceCodeRelativeNestingLevel, IsPassOutputDictionary, IndexString, CounterMatches)
                                            if BreakFlagCompression:
                                                break
                                        SourceCodeNestingLevel = StartSourceCodeNestingLevel
                                        SourceCodeRelativeNestingLevel = copy.deepcopy(StartSourceCodeRelativeNestingLevel)

                            if BreakFlagCompression:
                                break
        else:
            return IsPassDictionary, FlagFirstCircle, BracketIndexInSourceCodeList

    if FlagFirstCircle:
        FlagFirstCircle = False
    return IsPassOutputDictionary, FlagFirstCircle, BracketIndexInSourceCodeList

def AddToIsPassDictionary(MatchTokenList, MatchTokenIndex, SourceCodeTokenIndex, CurrentSourceCodeTokenIndex, CurrentSourceCodeTokenStringIndex, StartSourceCodeTokenStringIndex, SourceCodeNestingLevel, SourceCodeRelativeNestingLevel, IsPassOutputDictionary, IndexString, CounterMatches):
    NumberOccurrences = 0
    BreakFlagCompression = False
    if IsPassToN(MatchTokenList[MatchTokenIndex]):
        NumberOccurrences =  re.search(r"\d+", MatchTokenList[MatchTokenIndex]).group()
        NumberOccurrences = int(NumberOccurrences)

    if MatchTokenList[MatchTokenIndex] == "..^":
        if IsPassOutputDictionary:
            IsPassOutputDictionary.clear()
        IsPassOutputDictionary.append(
            {"IndexString": IndexString, "CurrentSourceCodeTokenIndex": CurrentSourceCodeTokenIndex,
             "SourceCodeNestingLevel": SourceCodeNestingLevel,
             "SourceCodeRelativeNestingLevel": SourceCodeRelativeNestingLevel,
             "CurrentSourceCodeTokenStringIndex": CurrentSourceCodeTokenStringIndex,
             'StartSourceCodeTokenIndex': SourceCodeTokenIndex,
             'StartSourceCodeTokenStringIndex': StartSourceCodeTokenStringIndex})
    else:
        CounterMatches += 1
    if NumberOccurrences and NumberOccurrences == CounterMatches:
        IsPassOutputDictionary.append(
            {"IndexString": IndexString, "CurrentSourceCodeTokenIndex": CurrentSourceCodeTokenIndex,
             "SourceCodeNestingLevel": SourceCodeNestingLevel,
             "SourceCodeRelativeNestingLevel": SourceCodeRelativeNestingLevel,
             "CurrentSourceCodeTokenStringIndex": CurrentSourceCodeTokenStringIndex,
             'StartSourceCodeTokenIndex': SourceCodeTokenIndex,
             'StartSourceCodeTokenStringIndex': StartSourceCodeTokenStringIndex})
        BreakFlagCompression = True

    elif not NumberOccurrences:
        IsPassOutputDictionary.append(
            {"IndexString": IndexString, "CurrentSourceCodeTokenIndex": CurrentSourceCodeTokenIndex,
             "SourceCodeNestingLevel": SourceCodeNestingLevel,
             "SourceCodeRelativeNestingLevel": SourceCodeRelativeNestingLevel,
             "CurrentSourceCodeTokenStringIndex": CurrentSourceCodeTokenStringIndex,
             'StartSourceCodeTokenIndex': SourceCodeTokenIndex,
             'StartSourceCodeTokenStringIndex': StartSourceCodeTokenStringIndex})
    if MatchTokenList[MatchTokenIndex] == "^..":
        BreakFlagCompression = True

    return BreakFlagCompression, IsPassOutputDictionary, CounterMatches

def IsInsert(MatchTokenList, MatchTokenIndex, SourceCodeTokenList, IsPassDictionaryList, FlagFirstCircle, NestingMap, BracketIndexInSourceCodeList):
    IsInsertIndexDictionaryList = []
    IsInsertOutputDictionaryList = []
    for IsPassDictionary in IsPassDictionaryList:
        CurrentSourceCodeTokenIndex = IsPassDictionary["CurrentSourceCodeTokenIndex"]
        CurrentSourceCodeTokenStringIndex = IsPassDictionary["CurrentSourceCodeTokenStringIndex"]
        SourceCodeNestingLevel = IsPassDictionary["SourceCodeNestingLevel"]
        SourceCodeRelativeNestingLevel = IsPassDictionary["SourceCodeRelativeNestingLevel"]
        IndexString =IsPassDictionary["IndexString"]
        IsPassDictionary = [IsPassDictionary]

        if  MatchTokenIndex > 0 and MatchTokenIndex + 1 < len(MatchTokenList) and MatchTokenList[MatchTokenIndex + 1] not in SPECIAL_OPERATORS  and not IsPassToN(MatchTokenList[MatchTokenIndex + 1]) and MatchTokenList[MatchTokenIndex - 1] not in SPECIAL_OPERATORS  and not IsPassToN(MatchTokenList[MatchTokenIndex - 1]):
            MatchTokenEndsInSourceCodeTokenList = FindAllSubstringEnds(SourceCodeTokenList[CurrentSourceCodeTokenIndex], MatchTokenList[MatchTokenIndex + 1], CurrentSourceCodeTokenStringIndex)
            if NestingMap[MatchTokenIndex + 1][0] <= -1:
                SourceCodeRelativeNestingLevel[-(NestingMap[MatchTokenIndex + 1][0])] = NestingLevelChange(SourceCodeRelativeNestingLevel[-(NestingMap[MatchTokenIndex + 1][0])], SourceCodeTokenList, CurrentSourceCodeTokenIndex)
            SourceCodeNestingLevel = NestingLevelChange(SourceCodeNestingLevel, SourceCodeTokenList, CurrentSourceCodeTokenIndex)
            if MatchTokenEndsInSourceCodeTokenList:
                StartSourceCodeTokenIndex = CurrentSourceCodeTokenIndex
                for CurrentSourceCodeTokenStringIndex in MatchTokenEndsInSourceCodeTokenList:
                    CounterMatches = 0
                    StartSourceCodeTokenStringIndex = CurrentSourceCodeTokenStringIndex
                    ComparisonTokenResults = ComparisonToken(MatchTokenList, MatchTokenIndex, SourceCodeTokenList, CurrentSourceCodeTokenIndex, NestingMap, CurrentSourceCodeTokenStringIndex, SourceCodeNestingLevel, IndexString + str(CounterMatches) + '/')
                    if ComparisonTokenResults:
                        ComparisonSourceCodeNestingLevel, CompressionSourceCodeRelativeNestingLevel, CurrentSourceCodeTokenStringIndex, ComparisonSourceCodeTokenIndex, SubIndex, ComparisonBracketIndexInSourceCodeList = ComparisonTokenResults
                        IndexString = IndexString + str(CounterMatches) + '/'

                        if NestingMap[SubIndex][0] > -1:
                            if NestingMap[SubIndex][0] == SourceCodeNestingLevel + ComparisonSourceCodeNestingLevel:
                                CurrentSourceCodeTokenIndex = ComparisonSourceCodeTokenIndex
                                SourceCodeNestingLevel = SourceCodeNestingLevel + ComparisonSourceCodeNestingLevel
                                BracketIndexInSourceCodeList.extend(ComparisonBracketIndexInSourceCodeList)
                                IsInsertOutputDictionaryList.append({"IndexString": IndexString, "CurrentSourceCodeTokenIndex": CurrentSourceCodeTokenIndex, "SourceCodeNestingLevel": SourceCodeNestingLevel, "SourceCodeRelativeNestingLevel": SourceCodeRelativeNestingLevel, "CurrentSourceCodeTokenStringIndex": CurrentSourceCodeTokenStringIndex, 'StartSourceCodeTokenIndex': StartSourceCodeTokenIndex, 'StartSourceCodeTokenStringIndex': StartSourceCodeTokenStringIndex})
                                IsInsertIndexDictionaryList.append(FindIsInsertIndex(MatchTokenList, MatchTokenIndex, StartSourceCodeTokenStringIndex, StartSourceCodeTokenIndex, IndexString, SourceCodeTokenList, 'Next'))
                        else:
                            if NestingMap[SubIndex][1] == CompressionSourceCodeRelativeNestingLevel + SourceCodeRelativeNestingLevel[-(NestingMap[SubIndex + 1][0])][0] or NestingMap[SubIndex][1] == 0:
                                CurrentSourceCodeTokenIndex = ComparisonSourceCodeTokenIndex
                                SourceCodeRelativeNestingLevel[-(NestingMap[SubIndex + 1][0])][0] = SourceCodeRelativeNestingLevel[-(NestingMap[SubIndex + 1][0])][0] + CompressionSourceCodeRelativeNestingLevel
                                SourceCodeNestingLevel = SourceCodeNestingLevel + ComparisonSourceCodeNestingLevel
                                BracketIndexInSourceCodeList.extend(ComparisonBracketIndexInSourceCodeList)
                                IsInsertOutputDictionaryList.append({"IndexString": IndexString, "CurrentSourceCodeTokenIndex": CurrentSourceCodeTokenIndex, "SourceCodeNestingLevel": SourceCodeNestingLevel, "SourceCodeRelativeNestingLevel": SourceCodeRelativeNestingLevel, "CurrentSourceCodeTokenStringIndex": CurrentSourceCodeTokenStringIndex, 'StartSourceCodeTokenIndex': StartSourceCodeTokenIndex, 'StartSourceCodeTokenStringIndex': StartSourceCodeTokenStringIndex})
                                IsInsertIndexDictionaryList.append(FindIsInsertIndex(MatchTokenList, MatchTokenIndex, StartSourceCodeTokenStringIndex, StartSourceCodeTokenIndex, IndexString, SourceCodeTokenList, 'Next'))


        elif MatchTokenIndex + 1 < len(MatchTokenList) and MatchTokenList[MatchTokenIndex + 1] not in SPECIAL_OPERATORS  and not IsPassToN(MatchTokenList[MatchTokenIndex + 1]) or MatchTokenIndex + 2 < len(MatchTokenList) and MatchTokenList[MatchTokenIndex + 1] not in PASS_OPERATORS and not IsPassToN(MatchTokenList[MatchTokenIndex + 1]) and MatchTokenList[MatchTokenIndex + 2] not in SPECIAL_OPERATORS and not IsPassToN(MatchTokenList[MatchTokenIndex + 2]):
            IsPassOutputDictionaryList, FlagFirstCircle, BracketIndexInSourceCodeList = IsPass(MatchTokenList, MatchTokenIndex, SourceCodeTokenList, IsPassDictionary, FlagFirstCircle, NestingMap, BracketIndexInSourceCodeList)
            if IsPassOutputDictionaryList:
                IsInsertOutputDictionaryList.extend(IsPassOutputDictionaryList)
                for IsPassOutput in IsPassOutputDictionaryList:
                    StartSourceCodeTokenIndex = IsPassOutput["StartSourceCodeTokenIndex"]
                    StartSourceCodeTokenStringIndex = IsPassOutput["StartSourceCodeTokenStringIndex"]
                    IndexString = IsPassOutput["IndexString"]
                    IsInsertIndexDictionaryList.append(FindIsInsertIndex(MatchTokenList, MatchTokenIndex, StartSourceCodeTokenStringIndex, StartSourceCodeTokenIndex, IndexString, SourceCodeTokenList, 'Next'))

        elif MatchTokenIndex == 0 and (len(MatchTokenList) == 1 or MatchTokenList[MatchTokenIndex + 1] in SPECIAL_OPERATORS or IsPassToN(MatchTokenList[MatchTokenIndex + 1])):
            IsInsertIndexDictionaryList.append({'IndexString': IndexString, 'CurrentSourceCodeTokenIndex': 0, 'CurrentSourceCodeTokenStringIndex': 0, 'InsertPosition': 'Next'})
            IsInsertOutputDictionaryList.extend(IsPassDictionary)

        elif MatchTokenIndex > 0 and MatchTokenList[MatchTokenIndex - 1] not in SPECIAL_OPERATORS and not IsPassToN(MatchTokenList[MatchTokenIndex - 1]):
            IsInsertIndexDictionaryList.append(FindIsInsertIndex(MatchTokenList, MatchTokenIndex, CurrentSourceCodeTokenStringIndex, CurrentSourceCodeTokenIndex, IndexString, SourceCodeTokenList, 'Prev'))
            IsInsertOutputDictionaryList.extend(IsPassDictionary)

        elif MatchTokenIndex + 1 == len(MatchTokenList) and (MatchTokenList[MatchTokenIndex - 1] in PASS_OPERATORS or IsPassToN(MatchTokenList[MatchTokenIndex - 1])):
            IsInsertIndexDictionaryList.append({'IndexString': IndexString, 'CurrentSourceCodeTokenIndex': len(SourceCodeTokenList) - 1, 'CurrentSourceCodeTokenStringIndex': len(SourceCodeTokenList[-1]) - 1, 'InsertPosition': 'Prev'})
            IsInsertOutputDictionaryList.extend(IsPassDictionary)

        elif MatchTokenList[MatchTokenIndex] == "<<<" and MatchTokenList[MatchTokenIndex - 1] == ">>>":
            IsInsertOutputDictionaryList.extend(IsPassDictionary)

    return IsInsertIndexDictionaryList, IsInsertOutputDictionaryList, FlagFirstCircle, BracketIndexInSourceCodeList

def FindIsInsertIndex(MatchTokenList, MatchTokenIndex, CurrentSourceCodeTokenStringIndex, CurrentSourceCodeTokenIndex, IndexString, SourceCodeTokenList, InsertPosition):
    if  InsertPosition == 'Prev':
        if CurrentSourceCodeTokenStringIndex == 0:
            InsertIndex ={'IndexString': IndexString, 'CurrentSourceCodeTokenIndex': CurrentSourceCodeTokenIndex - 1, 'CurrentSourceCodeTokenStringIndex':  len(SourceCodeTokenList[CurrentSourceCodeTokenIndex - 1]) - 1, 'InsertPosition': InsertPosition}
        else:
            InsertIndex ={'IndexString': IndexString, 'CurrentSourceCodeTokenIndex': CurrentSourceCodeTokenIndex, 'CurrentSourceCodeTokenStringIndex':  CurrentSourceCodeTokenStringIndex - 1, 'InsertPosition': InsertPosition}
    else:
        InsertIndex = {'IndexString': IndexString, 'CurrentSourceCodeTokenIndex': CurrentSourceCodeTokenIndex, 'CurrentSourceCodeTokenStringIndex': CurrentSourceCodeTokenStringIndex - len(MatchTokenList[MatchTokenIndex + 1]) + 1, 'InsertPosition': InsertPosition}
    return InsertIndex

def SearchInsertIndexInSourceCode(MatchTokenList, SourceCodeTokenList):
    Result = {}
    InsertIndexInTokenDictionary = SearchInsertIndexInTokenList(MatchTokenList, SourceCodeTokenList)
    if not InsertIndexInTokenDictionary:
        return 0
    if "ReplaceSourceCodeTokenIndex" in InsertIndexInTokenDictionary:
        TokenReplaceDirection = InsertIndexInTokenDictionary["ReplacePosition"]
        TokenReplaceStringIndex = InsertIndexInTokenDictionary["ReplaceSourceCodeTokenStringIndex"]
        TokenReplacePosition = InsertIndexInTokenDictionary["ReplaceSourceCodeTokenIndex"]
        TokenReplaceValue = SourceCodeTokenList[TokenReplacePosition][TokenReplaceStringIndex]
        CountReplace = 0
        for i in range(TokenReplacePosition):
            CountReplace += SourceCodeTokenList[i].count(TokenReplaceValue)
        CountReplace += SourceCodeTokenList[TokenReplacePosition][:TokenReplaceStringIndex].count(TokenReplaceValue)
        Result['Replace'] = [TokenReplaceDirection, CountReplace + 1, TokenReplaceValue]

    TokenInsertDirection = InsertIndexInTokenDictionary["InsertPosition"]
    TokenInsertStringIndex = InsertIndexInTokenDictionary["InsertSourceCodeTokenStringIndex"]
    TokenInsertPosition = InsertIndexInTokenDictionary["InsertSourceCodeTokenIndex"]
    TokenInsertValue = SourceCodeTokenList[TokenInsertPosition][TokenInsertStringIndex]
    CountInsert = 0
    for i in range(TokenInsertPosition):
        CountInsert += SourceCodeTokenList[i].count(TokenInsertValue)
    CountInsert += SourceCodeTokenList[TokenInsertPosition][:TokenInsertStringIndex].count(TokenInsertValue)
    Result['Insert'] = [TokenInsertDirection, CountInsert + 1, TokenInsertValue]

    return Result


def GetBracketIndicesForEllipsis(MatchTokenList):
    result = []
    IsNestingMarkerPairsDictionary =UpdateUnpairedMarkers(MatchTokenList)
    for i, MatchToken in enumerate(MatchTokenList):
        if (MatchToken in PASS_OPERATORS or  IsPassToN(MatchToken)) and i > 0:
            BracketIndexList = []
            for BracketIndex, (IsValid, ClosingIndex) in IsNestingMarkerPairsDictionary.items():
                if BracketIndex < i < ClosingIndex:
                    BracketIndexList.append((BracketIndex, ClosingIndex))
            if BracketIndexList:
                result.append({"EllipsisIndex": i, "BracketIndex": BracketIndexList})
            else:
                result.append({"EllipsisIndex": i, "BracketIndex": [(-1,-1)]})
    return result


def MatchNestingLevelInsertALL(MatchTokenList):
    result = []
    CounterNesting = 0
    BetweenEllipsis = TokenInBetweenEllipsis(MatchTokenList)
    RelativeNestingCounters = {i: 0 for i in range(1, len(BetweenEllipsis) + 1)}
    for MatchTokenIndex, MatchToken in enumerate(MatchTokenList):
        found_in_list = False
        for list_index, indices in enumerate(BetweenEllipsis):
            if MatchTokenIndex in indices:
                RelativeNestingCounters[list_index + 1] = NestingLevelChange(RelativeNestingCounters[list_index + 1], MatchTokenList, MatchTokenIndex)
                result.append((-(list_index + 1), RelativeNestingCounters[list_index + 1]))
                found_in_list = True
                break
        if not found_in_list:
            CounterNesting = NestingLevelChange(CounterNesting, MatchTokenList, MatchTokenIndex)
            result.append((CounterNesting, 0))
    return result


def TokenInBetweenEllipsis(MatchTokenList):
    BracketIndicesForEllipsis = GetBracketIndicesForEllipsis(MatchTokenList)
    BetweenEllipsis = []

    for i, CurrentBracket in enumerate(BracketIndicesForEllipsis):
        for NextBracket in BracketIndicesForEllipsis[i + 1:]:
            if CurrentBracket['BracketIndex'][-1] == NextBracket['BracketIndex'][-1]:
                BetweenEllipsis.append((list(range(CurrentBracket['EllipsisIndex'], NextBracket['EllipsisIndex'] + 1))))
                for j in range(1, len(BetweenEllipsis)):
                    if BetweenEllipsis[-1][0] == BetweenEllipsis[-(j+1)][-1]:
                        BetweenEllipsis[-(j + 1)] = [index for index in BetweenEllipsis[-(j + 1)] if index not in BetweenEllipsis[-1][1:]]
                    else:
                        BetweenEllipsis[-(j+1)] = [ index for index in BetweenEllipsis[-(j+1)] if index not in BetweenEllipsis[-1]]
                break
    return BetweenEllipsis

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


def UpdateUnpairedMarkers(MatchTokenList):
    IsNestingMarkerPairsDictionary = CheckMatchNestingMarkerPairs(MatchTokenList)
    ListLength = len(MatchTokenList)
    for index in IsNestingMarkerPairsDictionary:
        IsPaired, PairedIndex = IsNestingMarkerPairsDictionary[index]
        if not IsPaired and PairedIndex == -1 and MatchTokenList[index] in OPEN_NESTING_MARKERS:
            NearestClosingIndex = ListLength
            for OtherIndex in IsNestingMarkerPairsDictionary:
                if OtherIndex > index and IsNestingMarkerPairsDictionary[OtherIndex][0]:
                    if MatchTokenList[OtherIndex] in CLOSE_NESTING_MARKERS:
                        PairedOpeningIndex = IsNestingMarkerPairsDictionary[OtherIndex][1]
                        if PairedOpeningIndex < index:
                            NearestClosingIndex = min(NearestClosingIndex, OtherIndex)
            if MatchTokenList[NearestClosingIndex - 1] not in PASS_OPERATORS and  IsPassToN(MatchTokenList[NearestClosingIndex - 1]):
                for i in range(2, NearestClosingIndex):
                    if MatchTokenList[NearestClosingIndex - i] in PASS_OPERATORS or IsPassToN(MatchTokenList[NearestClosingIndex - i]):
                        NearestClosingIndex = NearestClosingIndex - i + 1
                        break
            IsNestingMarkerPairsDictionary[index] = [False, NearestClosingIndex]
    return IsNestingMarkerPairsDictionary


def TokensInNestingMarkersAll(MatchTokenList):
    IsNestingMarkerPairsDictionary = UpdateUnpairedMarkers(MatchTokenList)
    MarkerList = [[index, IsPaired, PairedIndex] for index, [IsPaired, PairedIndex] in IsNestingMarkerPairsDictionary.items()]
    result = []
    for TokenIndex in range(len(MatchTokenList)):
        ClosestPair = (-1, -1)
        ValidPairs = []
        for index, IsPaired, PairedIndex in sorted(MarkerList, key=lambda x: x[0]):
            if index < TokenIndex <= PairedIndex:
                ValidPairs.append([index, PairedIndex, IsPaired])
        if ValidPairs:
            ClosestPair = min(ValidPairs, key=lambda x: x[1] - x[0])
            if not ClosestPair[2]:
                for pair in sorted(ValidPairs, key=lambda x: x[1] - x[0]):
                    if pair[2]:
                        ClosestPair = (pair[0], pair[1])
                        break
                else:
                    ClosestPair = (ClosestPair[0], ClosestPair[1])
            else:
                ClosestPair = (ClosestPair[0], ClosestPair[1])
        result.append(ClosestPair)
    return result

def DictToTuples(MatchTokenList):
    result = []
    IsNestingMarkerPairsDictionary = UpdateUnpairedMarkers(MatchTokenList)
    for OpenIdx, (IsValid, CloseIdx) in IsNestingMarkerPairsDictionary.items():
        pair = tuple(sorted([OpenIdx, CloseIdx]))
        if pair not in result:
            result.append(pair)
    return result

def IndexNestingMarkersInSourceCode(MatchTokenList, MatchTokenIndex, StartSourceCodeTokenIndex, SubIndex, ComparisonSourceCodeNestingLevel, SourceCodeNestingLevel, IndexString):
    IndexNestingMarkersInSourceCodeList = []
    ListOfBrackets = DictToTuples(MatchTokenList)
    for (OpenBracketIndex, CloseBracketIndex) in ListOfBrackets:
        if OpenBracketIndex == SubIndex:
            ComparisonSourceCodeNestingLevel = ComparisonSourceCodeNestingLevel + SourceCodeNestingLevel
            IndexNestingMarkersInSourceCodeList.append((OpenBracketIndex, OpenBracketIndex - MatchTokenIndex  + StartSourceCodeTokenIndex - 1, ComparisonSourceCodeNestingLevel, IndexString))
    return IndexNestingMarkersInSourceCodeList