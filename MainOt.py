from typing import List, Any

from Utilities import ReceivingMatchOrPatchOrSourceCodeFromList, DetectProgrammingLanguage, ComparingListsLength, WriteFile, IsOnlyOneInsert
from TokenizeCode import CheckAndRunTokenize, find_nesting_brackets
from SearchCode import MatchNestingLevelInsertALL, SearchInsertIndexInSourceCode, SearchInsertIndexInTokenList, UpdateUnpairedMarkers
from Insert import RunInsert

SourcePath = "test/PassedTests/unique5.cpp"
MatchPath = "test/PassedTests/unique5.md"
ResultPath = 'result1.cpp'
Language = DetectProgrammingLanguage(SourcePath)
Matches = ReceivingMatchOrPatchOrSourceCodeFromList(MatchPath, "Match")
Patches = ReceivingMatchOrPatchOrSourceCodeFromList(MatchPath, "Patch")
ResultCode = ReceivingMatchOrPatchOrSourceCodeFromList(SourcePath, "SourceCode")
WriteFile(ResultPath, ResultCode)
if ComparingListsLength(Matches, Patches):
    for Match, Patch in zip(Matches, Patches):
        SourceCode = ReceivingMatchOrPatchOrSourceCodeFromList(ResultPath, "SourceCode")
        Fgg = find_nesting_brackets(Language, SourceCode)
        for i in Fgg:
            print(SourceCode[i - 30: i + 30])
        SourceCode = CheckAndRunTokenize(SourceCode, Language)
        Match = CheckAndRunTokenize(Match, Language)
        IsOnlyOneInsert = IsOnlyOneInsert(Match)
        if IsOnlyOneInsert == 1:
            FFFF = MatchNestingLevelInsertALL(Match)
            sss = UpdateUnpairedMarkers(Match)
            GGG = SearchInsertIndexInTokenList(Match, SourceCode)
            print(f" Match: {Match}")
            print(f"Source code TokenList: {SourceCode}")
            print(f"CheckMatchNestingMarkerPairs: {Fgg}")
            SearchDictionary = SearchInsertIndexInSourceCode(Match, SourceCode)
            print(f"Insert index in sourcecode TokenList: {SearchDictionary}")
            RunInsert(Match, Patch, SourceCode, ResultPath, ResultPath)
        elif IsOnlyOneInsert == 2:
            print("В match больше одной вставки")
        else:
            print("В match отсутствует место вставки")