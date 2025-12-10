from constants import SPECIAL_OPERATORS, OPEN_NESTING_MARKERS, CLOSE_NESTING_MARKERS, NESTING_MARKERS, DICTIONARY_NESTING_MARKERS, PASS_OPERATORS
from  Utilities import IsPassToN
import copy
import re
from Logging import setup_logger, log_function

logger = setup_logger()

@log_function(args=False, result=False)
def SearchInsertIndexInTokenList(MatchTokenList, SourceCodeTokenList):
    try:
        SourceCodeRelativeNestingLevel = {i: [0, False] for i in range(1, len(TokenInBetweenEllipsis(MatchTokenList)) + 1)}
        IsPassDictionaryList = [{"IndexString": "", "CurrentSourceCodeTokenIndex": 0, "SourceCodeNestingLevel": 0, "SourceCodeRelativeNestingLevel": SourceCodeRelativeNestingLevel,"CurrentSourceCodeTokenStringIndex": 0, 'StartSourceCodeTokenIndex': 0, 'StartSourceCodeTokenStringIndex': 0, "CodeNestingLevel": 0}]
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
                raise ValueError(f"Part of the pattern was not found {MatchTokenIndex}")
        result = CollectingResultsIndexInTokenList(IsInsertIndexDictionaryList, IsPassDictionaryList, IsReplaceIndexDictionaryList)
        if result:
            return result
        else:
            raise ValueError("Pattern is not unique")
    except ValueError as e:
        logger.error(f"Pattern matching error: {e}")
        return  None


@log_function(args=False, result=False)
def CollectingResultsIndexInTokenList( IsInsertIndexDictionaryList, IsPassDictionaryList, IsReplaceIndexDictionaryList):
    try:
        if not IsInsertIndexDictionaryList:
            raise ValueError("The insertion location was not found.")
        result = {}
        ValidInserts = ValidatePoint(IsPassDictionaryList, IsInsertIndexDictionaryList, "Insert")
        result.update({"InsertSourceCodeTokenStringIndex": ValidInserts["CurrentSourceCodeTokenStringIndex"], "InsertSourceCodeTokenIndex": ValidInserts["CurrentSourceCodeTokenIndex"], "InsertPosition": ValidInserts["InsertPosition"], 'CodeNestingLevel': ValidInserts["CodeNestingLevel"]})
        if IsReplaceIndexDictionaryList:
            ValidReplaces = ValidatePoint(IsPassDictionaryList, IsReplaceIndexDictionaryList, "Replace")
            result.update({"ReplaceSourceCodeTokenStringIndex": ValidReplaces["CurrentSourceCodeTokenStringIndex"], "ReplaceSourceCodeTokenIndex": ValidReplaces["CurrentSourceCodeTokenIndex"], "ReplacePosition": ValidReplaces["InsertPosition"]})
        return result
    except ValueError as e:
        logger.error(f"Pattern matching error: {e}")
        return None

@log_function(args=False, result=False)
def ValidatePoint(IsPassDictionaryList, CandidateDictionaryList, TypeAction):
    ValidPoints = []
    for IsInsertIndexDictionary in CandidateDictionaryList:
        CandidatePath = IsInsertIndexDictionary["IndexString"]
        HasMatchingLeaf = any(pass_dict["IndexString"].startswith(CandidatePath) for pass_dict in IsPassDictionaryList)
        if HasMatchingLeaf:
            ValidPoints.append(IsInsertIndexDictionary)

    if not ValidPoints:
        raise ValueError(f"The {TypeAction} location was not found")
    multipleAction = len(ValidPoints) > 1
    if multipleAction:
        raise ValueError(f"Pattern is not unique - multiple {TypeAction} regions found")

    ValidPoint = ValidPoints[0]
    return ValidPoint

@log_function(args=False, result=False)
def FindAllSubstringEnds(string, SubString, SubStringIndex):
    result = []
    while True:
        index = string.find(SubString, SubStringIndex)
        if (SubString in NESTING_MARKERS and len(string) > 1 or index == -1) and len(SubString) > 0:
            break
        result.append(index + len(SubString) - 1)
        SubStringIndex = index + 1
    return result

@log_function(args=False, result=False)
def ComparisonToken(MatchTokenList, MatchTokenIndex, SourceCodeTokenList, SourceCodeTokenIndex, NestingMap, CurrentSourceCodeTokenStringIndex, SourceCodeNestingLevel, IndexString):
    BracketIndexInSourceCodeList = []
    CompressionSourceCodeRelativeNestingLevel = 0
    ComparisonSourceCodeNestingLevel = 0
    CurrentSourceCodeTokenStringIndex += 1
    FirstCircleFlag = True
    ComparisonSourceCodeTokenIndex = SourceCodeTokenIndex
    SubIndex = MatchTokenIndex + 2
    if SubIndex < len(MatchTokenList):
        MatchToken = MatchTokenList[SubIndex]
        while SubIndex < len(MatchTokenList)  and ComparisonSourceCodeTokenIndex < len(SourceCodeTokenList) and MatchTokenList[SubIndex] not in SPECIAL_OPERATORS and not IsPassToN(MatchTokenList[SubIndex]):
            if CurrentSourceCodeTokenStringIndex == len(SourceCodeTokenList[SourceCodeTokenIndex]) and FirstCircleFlag:
                ComparisonSourceCodeTokenIndex = SourceCodeTokenIndex + 1 if SourceCodeTokenIndex + 1 < len(SourceCodeTokenList) else SourceCodeTokenIndex
                CurrentSourceCodeTokenStringIndex = 0
                FirstCircleFlag = False
            SourceCodeToken = SourceCodeTokenList[ComparisonSourceCodeTokenIndex]

            if NestingMap[SubIndex][0] <= -1:
                CompressionSourceCodeRelativeNestingLevel = NestingLevelChange(CompressionSourceCodeRelativeNestingLevel, SourceCodeTokenList, ComparisonSourceCodeTokenIndex)
            ComparisonSourceCodeNestingLevel = NestingLevelChange(ComparisonSourceCodeNestingLevel, SourceCodeTokenList, ComparisonSourceCodeTokenIndex)
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

@log_function(args=False, result=False)
def NestingLevelChange(NestingLevel, TokenList, TokenIndex):

    if TokenList[TokenIndex] in OPEN_NESTING_MARKERS:
        NestingLevel = NestingLevel + 1

    if TokenList[TokenIndex] in CLOSE_NESTING_MARKERS:
        NestingLevel = NestingLevel - 1

    return NestingLevel

@log_function(args=False, result=False)
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
                SourceCodeRelativeNestingLevel = copy.deepcopy(IsPassOutput["SourceCodeRelativeNestingLevel"])
                StartCurrentSourceCodeTokenIndex = IsPassOutput["CurrentSourceCodeTokenIndex"]
                SourceCodeTokenStringIndex = IsPassOutput["CurrentSourceCodeTokenStringIndex"]
                CodeNestingLevel = IsPassOutput["CodeNestingLevel"]
                CounterMatches = 0
                BreakFlag = False
                BreakFlagCompression = False
                IsThisNestingLevelExistFurther = False

                if NestingMap[MatchTokenIndex + 1][0] <= -1:
                    IsEllipsisEnd = False
                    for NestingLevel,RelativeNestingLevel in NestingMap[MatchTokenIndex + 2:]:
                        if NestingMap[MatchTokenIndex + 1][0] != NestingLevel:
                            IsEllipsisEnd = True
                        if IsEllipsisEnd and NestingMap[MatchTokenIndex + 1][0] == NestingLevel:
                            IsThisNestingLevelExistFurther = True
                            break
                for SourceCodeTokenIndex in range(StartCurrentSourceCodeTokenIndex, len(SourceCodeTokenList)):

                    if MatchTokenIndex + 1 < len(MatchTokenList):
                        for key in SourceCodeRelativeNestingLevel:
                            if SourceCodeRelativeNestingLevel[key][1]:
                                SourceCodeRelativeNestingLevel[key][0] = NestingLevelChange(SourceCodeRelativeNestingLevel[key][0], SourceCodeTokenList, SourceCodeTokenIndex)

                        if not FlagFirstCircle:
                            SourceCodeNestingLevel = NestingLevelChange(SourceCodeNestingLevel, SourceCodeTokenList, SourceCodeTokenIndex)
                        CodeNestingLevel = NestingLevelChange(CodeNestingLevel, SourceCodeTokenList, SourceCodeTokenIndex)

                        CompressionIndexString = IsPassOutput["IndexString"] + str(CounterMatches) + '/'
                        for (MatchBracketIndex, SourceCodeBracketIndex, SourceCodeBracketNestingLevel, IndexString) in BracketIndexInSourceCodeList:
                            for SearchToken in range(MatchTokenIndex + 1, LastSearchToken + 1):
                                if NestingMarkersIndexesForTokenList[SearchToken][0] == MatchBracketIndex and SourceCodeBracketNestingLevel > SourceCodeNestingLevel and  CompressionIndexString[0:len(IndexString)] == IndexString:
                                    if SourceCodeTokenList[SourceCodeTokenIndex] in CLOSE_NESTING_MARKERS:
                                        BreakFlagCompression = True
                                    else:
                                        BreakFlag = True
                                    break
                        if BreakFlag:
                            break
                        MatchTokenEndsInSourceCodeTokenList = FindAllSubstringEnds(SourceCodeTokenList[SourceCodeTokenIndex], MatchTokenList[MatchTokenIndex + 1], SourceCodeTokenStringIndex)
                        SourceCodeTokenStringIndex = 0

                        if MatchTokenEndsInSourceCodeTokenList:
                            StartSourceCodeRelativeNestingLevel = copy.deepcopy(SourceCodeRelativeNestingLevel)
                            StartSourceCodeNestingLevel = SourceCodeNestingLevel
                            StartCodeNestingLevel = CodeNestingLevel
                            if NestingMap[MatchTokenIndex + 1][0] <= -1 and SourceCodeRelativeNestingLevel[-(NestingMap[MatchTokenIndex + 1][0])][1] == False:
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
                                            CodeNestingLevel = CodeNestingLevel + ComparisonSourceCodeNestingLevel
                                            BreakFlagCompression, IsPassOutputDictionary, CounterMatches = AddToIsPassDictionary(MatchTokenList, MatchTokenIndex, SourceCodeTokenIndex, CurrentSourceCodeTokenIndex, CurrentSourceCodeTokenStringIndex, StartSourceCodeTokenStringIndex, SourceCodeNestingLevel, SourceCodeRelativeNestingLevel, IsPassOutputDictionary, IndexString, CounterMatches, CodeNestingLevel)
                                            if BreakFlagCompression:
                                                break

                                        SourceCodeNestingLevel = StartSourceCodeNestingLevel
                                    else:
                                        if NestingMap[SubIndex][1] == CompressionSourceCodeRelativeNestingLevel + SourceCodeRelativeNestingLevel[-(NestingMap[SubIndex][0])][0]:
                                            SourceCodeRelativeNestingLevel[-(NestingMap[SubIndex][0])][0] = SourceCodeRelativeNestingLevel[-(NestingMap[SubIndex][0])][0] + CompressionSourceCodeRelativeNestingLevel

                                            for key in SourceCodeRelativeNestingLevel:
                                                if SourceCodeRelativeNestingLevel[key][1] and key != -(NestingMap[SubIndex][0]):
                                                    SourceCodeRelativeNestingLevel[key][0] = SourceCodeRelativeNestingLevel[key][0] + CompressionSourceCodeRelativeNestingLevel

                                            CurrentSourceCodeTokenIndex = ComparisonSourceCodeTokenIndex
                                            SourceCodeNestingLevel = SourceCodeNestingLevel + ComparisonSourceCodeNestingLevel
                                            BracketIndexInSourceCodeList.extend(ComparisonBracketIndexInSourceCodeList)
                                            CodeNestingLevel = CodeNestingLevel + ComparisonSourceCodeNestingLevel
                                            if IsThisNestingLevelExistFurther:
                                                SourceCodeRelativeNestingLevel[-(NestingMap[MatchTokenIndex + 1][0])][1] = True
                                            else:
                                                SourceCodeRelativeNestingLevel[-(NestingMap[MatchTokenIndex + 1][0])][1] = False
                                            BreakFlagCompression, IsPassOutputDictionary, CounterMatches = AddToIsPassDictionary(MatchTokenList, MatchTokenIndex, SourceCodeTokenIndex, CurrentSourceCodeTokenIndex, CurrentSourceCodeTokenStringIndex, StartSourceCodeTokenStringIndex, SourceCodeNestingLevel, SourceCodeRelativeNestingLevel, IsPassOutputDictionary, IndexString, CounterMatches, CodeNestingLevel)
                                            if BreakFlagCompression:
                                                break
                                        SourceCodeNestingLevel = StartSourceCodeNestingLevel
                                        SourceCodeRelativeNestingLevel = copy.deepcopy(StartSourceCodeRelativeNestingLevel)
                                        CodeNestingLevel = StartCodeNestingLevel

                            if BreakFlagCompression:
                                break
        else:
            return IsPassDictionary, FlagFirstCircle, BracketIndexInSourceCodeList

    if FlagFirstCircle:
        FlagFirstCircle = False
    return IsPassOutputDictionary, FlagFirstCircle, BracketIndexInSourceCodeList

@log_function(args=False, result=False)
def AddToIsPassDictionary(MatchTokenList, MatchTokenIndex, SourceCodeTokenIndex, CurrentSourceCodeTokenIndex, CurrentSourceCodeTokenStringIndex, StartSourceCodeTokenStringIndex, SourceCodeNestingLevel, SourceCodeRelativeNestingLevel, IsPassOutputDictionary, IndexString, CounterMatches, CodeNestingLevel):
    NumberOccurrences = 0
    BreakFlagCompression = False
    if IsPassToN(MatchTokenList[MatchTokenIndex]):
        NumberOccurrences =  re.search(r"\d+", MatchTokenList[MatchTokenIndex]).group()
        NumberOccurrences = int(NumberOccurrences)
    elif MatchTokenIndex > 0 and IsPassToN(MatchTokenList[MatchTokenIndex - 1]):
        NumberOccurrences =  re.search(r"\d+", MatchTokenList[MatchTokenIndex - 1]).group()
        NumberOccurrences = int(NumberOccurrences)

    if MatchTokenList[MatchTokenIndex] == "..^" or MatchTokenIndex > 0 and MatchTokenList[MatchTokenIndex - 1] == "..^" :
        if IsPassOutputDictionary:
            IsPassOutputDictionary.clear()
        IsPassOutputDictionary.append(
            {"IndexString": IndexString, "CurrentSourceCodeTokenIndex": CurrentSourceCodeTokenIndex,
             "SourceCodeNestingLevel": SourceCodeNestingLevel,
             "SourceCodeRelativeNestingLevel": SourceCodeRelativeNestingLevel,
             "CurrentSourceCodeTokenStringIndex": CurrentSourceCodeTokenStringIndex,
             'StartSourceCodeTokenIndex': SourceCodeTokenIndex,
             'StartSourceCodeTokenStringIndex': StartSourceCodeTokenStringIndex,
             'CodeNestingLevel': CodeNestingLevel})
    else:
        CounterMatches += 1
    if NumberOccurrences and NumberOccurrences == CounterMatches:
        IsPassOutputDictionary.append(
            {"IndexString": IndexString, "CurrentSourceCodeTokenIndex": CurrentSourceCodeTokenIndex,
             "SourceCodeNestingLevel": SourceCodeNestingLevel,
             "SourceCodeRelativeNestingLevel": SourceCodeRelativeNestingLevel,
             "CurrentSourceCodeTokenStringIndex": CurrentSourceCodeTokenStringIndex,
             'StartSourceCodeTokenIndex': SourceCodeTokenIndex,
             'StartSourceCodeTokenStringIndex': StartSourceCodeTokenStringIndex,
             'CodeNestingLevel': CodeNestingLevel})
        BreakFlagCompression = True

    elif not NumberOccurrences:
        IsPassOutputDictionary.append(
            {"IndexString": IndexString, "CurrentSourceCodeTokenIndex": CurrentSourceCodeTokenIndex,
             "SourceCodeNestingLevel": SourceCodeNestingLevel,
             "SourceCodeRelativeNestingLevel": SourceCodeRelativeNestingLevel,
             "CurrentSourceCodeTokenStringIndex": CurrentSourceCodeTokenStringIndex,
             'StartSourceCodeTokenIndex': SourceCodeTokenIndex,
             'StartSourceCodeTokenStringIndex': StartSourceCodeTokenStringIndex,
             'CodeNestingLevel': CodeNestingLevel})
    if MatchTokenList[MatchTokenIndex] == "^.." or MatchTokenIndex > 0 and MatchTokenList[MatchTokenIndex - 1] == "^..":
        BreakFlagCompression = True

    return BreakFlagCompression, IsPassOutputDictionary, CounterMatches

@log_function(args=False, result=False)
def IsInsert(MatchTokenList, MatchTokenIndex, SourceCodeTokenList, IsPassDictionaryList, FlagFirstCircle, NestingMap, BracketIndexInSourceCodeList):
    IsInsertIndexDictionaryList = []
    IsInsertOutputDictionaryList = []
    for IsPassDictionary in IsPassDictionaryList:
        CurrentSourceCodeTokenIndex = IsPassDictionary["CurrentSourceCodeTokenIndex"]
        CurrentSourceCodeTokenStringIndex = IsPassDictionary["CurrentSourceCodeTokenStringIndex"]
        StartSourceCodeTokenStringIndex = IsPassDictionary["CurrentSourceCodeTokenStringIndex"]
        SourceCodeNestingLevel = IsPassDictionary["SourceCodeNestingLevel"]
        SourceCodeRelativeNestingLevel = IsPassDictionary["SourceCodeRelativeNestingLevel"]
        IndexString =IsPassDictionary["IndexString"]
        CodeNestingLevel = IsPassDictionary["CodeNestingLevel"]
        IsPassDictionary = [IsPassDictionary]

        if  MatchTokenIndex > 0 and MatchTokenIndex + 1 < len(MatchTokenList) and MatchTokenList[MatchTokenIndex + 1] not in SPECIAL_OPERATORS  and not IsPassToN(MatchTokenList[MatchTokenIndex + 1]) and MatchTokenList[MatchTokenIndex - 1] not in SPECIAL_OPERATORS  and not IsPassToN(MatchTokenList[MatchTokenIndex - 1]):
            IsThisNestingLevelExistFurther = False

            if NestingMap[MatchTokenIndex + 1][0] <= -1:
                IsEllipsisEnd = False
                for NestingLevel, RelativeNestingLevel in NestingMap[MatchTokenIndex + 2:]:
                    if NestingMap[MatchTokenIndex + 1][0] != NestingLevel:
                        IsEllipsisEnd = True
                    if IsEllipsisEnd and NestingMap[MatchTokenIndex + 1][0] == NestingLevel:
                        IsThisNestingLevelExistFurther = True
                        break

            MatchTokenEndsInSourceCodeTokenList = FindAllSubstringEnds(SourceCodeTokenList[CurrentSourceCodeTokenIndex], MatchTokenList[MatchTokenIndex + 1], CurrentSourceCodeTokenStringIndex)
            if NestingMap[MatchTokenIndex + 1][0] <= -1 and SourceCodeRelativeNestingLevel[-(NestingMap[MatchTokenIndex + 1][0])][1] == False:
                SourceCodeRelativeNestingLevel[-(NestingMap[MatchTokenIndex + 1][0])][0] = NestingLevelChange(SourceCodeRelativeNestingLevel[-(NestingMap[MatchTokenIndex + 1][0])][0], SourceCodeTokenList, CurrentSourceCodeTokenIndex)

            for key in SourceCodeRelativeNestingLevel:
                if SourceCodeRelativeNestingLevel[key][1]:
                    SourceCodeRelativeNestingLevel[key][0] = NestingLevelChange(SourceCodeRelativeNestingLevel[key][0], SourceCodeTokenList, CurrentSourceCodeTokenIndex)

            SourceCodeNestingLevel = NestingLevelChange(SourceCodeNestingLevel, SourceCodeTokenList, CurrentSourceCodeTokenIndex)
            if MatchTokenEndsInSourceCodeTokenList:
                StartSourceCodeTokenIndex = CurrentSourceCodeTokenIndex
                for CurrentSourceCodeTokenStringIndex in MatchTokenEndsInSourceCodeTokenList:

                    if CurrentSourceCodeTokenStringIndex != StartSourceCodeTokenStringIndex + len(MatchTokenList[MatchTokenIndex + 1]) - 1:
                        continue
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
                                IsInsertOutputDictionaryList.append({"IndexString": IndexString, "CurrentSourceCodeTokenIndex": CurrentSourceCodeTokenIndex, "SourceCodeNestingLevel": SourceCodeNestingLevel, "SourceCodeRelativeNestingLevel": SourceCodeRelativeNestingLevel, "CurrentSourceCodeTokenStringIndex": CurrentSourceCodeTokenStringIndex, 'StartSourceCodeTokenIndex': StartSourceCodeTokenIndex, 'StartSourceCodeTokenStringIndex': StartSourceCodeTokenStringIndex, "CodeNestingLevel": CodeNestingLevel})
                                IsInsertIndexDictionaryList.append(FindIsInsertIndex(MatchTokenList, MatchTokenIndex, StartSourceCodeTokenStringIndex, StartSourceCodeTokenIndex, IndexString, SourceCodeTokenList, 'Next', CodeNestingLevel))
                        else:
                            if NestingMap[SubIndex][1] == CompressionSourceCodeRelativeNestingLevel + SourceCodeRelativeNestingLevel[-(NestingMap[SubIndex][0])][0]:
                                CurrentSourceCodeTokenIndex = ComparisonSourceCodeTokenIndex
                                SourceCodeRelativeNestingLevel[-(NestingMap[SubIndex][0])][0] = SourceCodeRelativeNestingLevel[-(NestingMap[SubIndex][0])][0] + CompressionSourceCodeRelativeNestingLevel

                                for key in SourceCodeRelativeNestingLevel:
                                    if SourceCodeRelativeNestingLevel[key][1] and key != -(NestingMap[SubIndex][0]):
                                        SourceCodeRelativeNestingLevel[key][0] = SourceCodeRelativeNestingLevel[key][0] + CompressionSourceCodeRelativeNestingLevel

                                SourceCodeNestingLevel = SourceCodeNestingLevel + ComparisonSourceCodeNestingLevel
                                BracketIndexInSourceCodeList.extend(ComparisonBracketIndexInSourceCodeList)
                                if IsThisNestingLevelExistFurther:
                                    SourceCodeRelativeNestingLevel[-(NestingMap[MatchTokenIndex + 1][0])][1] = True
                                else:
                                    SourceCodeRelativeNestingLevel[-(NestingMap[MatchTokenIndex + 1][0])][1] = False
                                IsInsertOutputDictionaryList.append({"IndexString": IndexString, "CurrentSourceCodeTokenIndex": CurrentSourceCodeTokenIndex, "SourceCodeNestingLevel": SourceCodeNestingLevel, "SourceCodeRelativeNestingLevel": SourceCodeRelativeNestingLevel, "CurrentSourceCodeTokenStringIndex": CurrentSourceCodeTokenStringIndex, 'StartSourceCodeTokenIndex': StartSourceCodeTokenIndex, 'StartSourceCodeTokenStringIndex': StartSourceCodeTokenStringIndex, "CodeNestingLevel": CodeNestingLevel})
                                IsInsertIndexDictionaryList.append(FindIsInsertIndex(MatchTokenList, MatchTokenIndex, StartSourceCodeTokenStringIndex, StartSourceCodeTokenIndex, IndexString, SourceCodeTokenList, 'Next', CodeNestingLevel))


        elif MatchTokenIndex + 1 < len(MatchTokenList) and MatchTokenList[MatchTokenIndex + 1] not in SPECIAL_OPERATORS  and not IsPassToN(MatchTokenList[MatchTokenIndex + 1]) or MatchTokenIndex + 2 < len(MatchTokenList) and MatchTokenList[MatchTokenIndex + 1] not in PASS_OPERATORS and not IsPassToN(MatchTokenList[MatchTokenIndex + 1]) and MatchTokenList[MatchTokenIndex + 2] not in SPECIAL_OPERATORS and not IsPassToN(MatchTokenList[MatchTokenIndex + 2]):
            IsPassOutputDictionaryList, FlagFirstCircle, BracketIndexInSourceCodeList = IsPass(MatchTokenList, MatchTokenIndex, SourceCodeTokenList, IsPassDictionary, FlagFirstCircle, NestingMap, BracketIndexInSourceCodeList)
            if IsPassOutputDictionaryList:
                IsInsertOutputDictionaryList.extend(IsPassOutputDictionaryList)
                for IsPassOutput in IsPassOutputDictionaryList:
                    StartSourceCodeTokenIndex = IsPassOutput["StartSourceCodeTokenIndex"]
                    StartSourceCodeTokenStringIndex = IsPassOutput["StartSourceCodeTokenStringIndex"]
                    IndexString = IsPassOutput["IndexString"]
                    IsInsertIndexDictionaryList.append(FindIsInsertIndex(MatchTokenList, MatchTokenIndex, StartSourceCodeTokenStringIndex, StartSourceCodeTokenIndex, IndexString, SourceCodeTokenList, 'Next', CodeNestingLevel))

        elif MatchTokenIndex == 0 and (len(MatchTokenList) == 1 or MatchTokenList[MatchTokenIndex + 1] in SPECIAL_OPERATORS or IsPassToN(MatchTokenList[MatchTokenIndex + 1])):
            IsInsertIndexDictionaryList.append({'IndexString': IndexString, 'CurrentSourceCodeTokenIndex': 0, 'CurrentSourceCodeTokenStringIndex': 0, 'InsertPosition': 'Next', "CodeNestingLevel": 0})
            IsInsertOutputDictionaryList.extend(IsPassDictionary)

        elif MatchTokenIndex > 0 and MatchTokenList[MatchTokenIndex - 1] not in SPECIAL_OPERATORS and not IsPassToN(MatchTokenList[MatchTokenIndex - 1]):
            IsInsertIndexDictionaryList.append(FindIsInsertIndex(MatchTokenList, MatchTokenIndex, CurrentSourceCodeTokenStringIndex, CurrentSourceCodeTokenIndex, IndexString, SourceCodeTokenList, 'Prev', CodeNestingLevel))
            IsInsertOutputDictionaryList.extend(IsPassDictionary)

        elif MatchTokenIndex + 1 == len(MatchTokenList) and (MatchTokenList[MatchTokenIndex - 1] in PASS_OPERATORS or IsPassToN(MatchTokenList[MatchTokenIndex - 1])):
            IsInsertIndexDictionaryList.append({'IndexString': IndexString, 'CurrentSourceCodeTokenIndex': len(SourceCodeTokenList) - 1, 'CurrentSourceCodeTokenStringIndex': len(SourceCodeTokenList[-1]) - 1, 'InsertPosition': 'Prev', "CodeNestingLevel": 0})
            IsInsertOutputDictionaryList.extend(IsPassDictionary)

        elif MatchTokenList[MatchTokenIndex] == "<<<" and MatchTokenList[MatchTokenIndex - 1] == ">>>":
            IsInsertOutputDictionaryList.append(IsPassDictionary[0])

    return IsInsertIndexDictionaryList, IsInsertOutputDictionaryList, FlagFirstCircle, BracketIndexInSourceCodeList

@log_function(args=False, result=False)
def FindIsInsertIndex(MatchTokenList, MatchTokenIndex, CurrentSourceCodeTokenStringIndex, CurrentSourceCodeTokenIndex, IndexString, SourceCodeTokenList, InsertPosition, CodeNestingLevel):
    if  InsertPosition == 'Prev':
        if CurrentSourceCodeTokenStringIndex == 0:
            InsertIndex ={'IndexString': IndexString, 'CurrentSourceCodeTokenIndex': CurrentSourceCodeTokenIndex - 1, 'CurrentSourceCodeTokenStringIndex':  len(SourceCodeTokenList[CurrentSourceCodeTokenIndex - 1]) - 1, 'InsertPosition': InsertPosition, "CodeNestingLevel": CodeNestingLevel}
        else:
            InsertIndex ={'IndexString': IndexString, 'CurrentSourceCodeTokenIndex': CurrentSourceCodeTokenIndex, 'CurrentSourceCodeTokenStringIndex':  CurrentSourceCodeTokenStringIndex - 1, 'InsertPosition': InsertPosition, "CodeNestingLevel": CodeNestingLevel}
    else:
        InsertIndex = {'IndexString': IndexString, 'CurrentSourceCodeTokenIndex': CurrentSourceCodeTokenIndex, 'CurrentSourceCodeTokenStringIndex': CurrentSourceCodeTokenStringIndex - len(MatchTokenList[MatchTokenIndex + 1]) + 1, 'InsertPosition': InsertPosition, "CodeNestingLevel": CodeNestingLevel}
    return InsertIndex

@log_function(args=False, result=False)
def SearchInsertIndexInSourceCode(MatchTokenList, SourceCodeTokenList):
    InsertIndexInTokenDictionary = SearchInsertIndexInTokenList(MatchTokenList, SourceCodeTokenList)
    if not InsertIndexInTokenDictionary:
        return None
    Result = {}
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
    CodeNestingLevel = InsertIndexInTokenDictionary["CodeNestingLevel"]
    CountInsert = 0
    for i in range(TokenInsertPosition):
        CountInsert += SourceCodeTokenList[i].count(TokenInsertValue)
    CountInsert += SourceCodeTokenList[TokenInsertPosition][:TokenInsertStringIndex].count(TokenInsertValue)
    Result['Insert'] = [TokenInsertDirection, CountInsert + 1, TokenInsertValue, CodeNestingLevel]
    print(Result)
    return Result


@log_function(args=False, result=False)
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

@log_function(args=False, result=False)
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

@log_function(args=False, result=False)
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

@log_function(args=False, result=False)
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

@log_function(args=False, result=False)
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

@log_function(args=False, result=False)
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

@log_function(args=False, result=False)
def DictToTuples(MatchTokenList):
    result = []
    IsNestingMarkerPairsDictionary = UpdateUnpairedMarkers(MatchTokenList)
    for OpenIdx, (IsValid, CloseIdx) in IsNestingMarkerPairsDictionary.items():
        pair = tuple(sorted([OpenIdx, CloseIdx]))
        if pair not in result:
            result.append(pair)
    return result

@log_function(args=False, result=False)
def IndexNestingMarkersInSourceCode(MatchTokenList, MatchTokenIndex, StartSourceCodeTokenIndex, SubIndex, ComparisonSourceCodeNestingLevel, SourceCodeNestingLevel, IndexString):
    IndexNestingMarkersInSourceCodeList = []
    ListOfBrackets = DictToTuples(MatchTokenList)
    for (OpenBracketIndex, CloseBracketIndex) in ListOfBrackets:
        if OpenBracketIndex == SubIndex:
            ComparisonSourceCodeNestingLevel = ComparisonSourceCodeNestingLevel + SourceCodeNestingLevel
            IndexNestingMarkersInSourceCodeList.append((OpenBracketIndex, OpenBracketIndex - MatchTokenIndex  + StartSourceCodeTokenIndex - 1, ComparisonSourceCodeNestingLevel, IndexString))
    return IndexNestingMarkersInSourceCodeList