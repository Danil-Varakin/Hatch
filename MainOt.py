from Utilities import ReceivingMatchOrPatchOrSourceCodeFromList, DetectProgrammingLanguage, ComparingListsLength, WriteFile, InsertOperatorStatus
from TokenizeCode import CheckAndRunTokenize
from SearchCode import MatchNestingLevelInsertALL, SearchInsertIndexInSourceCode, TokensInNestingMarkersAll
from Insert import RunInsert

SourcePath = "test/PassedTests/unique15.cpp"
MatchPath = "test/PassedTests/unique15.md"
ResultPath = 'result1.cpp'
Language = DetectProgrammingLanguage(SourcePath)
Matches = ReceivingMatchOrPatchOrSourceCodeFromList(MatchPath, "Match")
Patches = ReceivingMatchOrPatchOrSourceCodeFromList(MatchPath, "Patch")
ResultCode = ReceivingMatchOrPatchOrSourceCodeFromList(SourcePath, "SourceCode")
WriteFile(ResultPath, ResultCode)
if ComparingListsLength(Matches, Patches):
    for Match, Patch in zip(Matches, Patches):
        SourceCode = ReceivingMatchOrPatchOrSourceCodeFromList(ResultPath, "SourceCode")
        SourceCode = CheckAndRunTokenize(SourceCode, Language)
        Match = CheckAndRunTokenize(Match, Language)
        IsOnlyOneInsert = InsertOperatorStatus(Match)
        if IsOnlyOneInsert == 1:
            FFFF = MatchNestingLevelInsertALL(Match)
            sss = TokensInNestingMarkersAll(Match)
            SearchDictionary, _ = SearchInsertIndexInSourceCode(Match, SourceCode)
            print(f"Insert index in sourcecode TokenList: {SearchDictionary}")
            RunInsert(Match, Patch, SourceCode, ResultPath, ResultPath)
        elif IsOnlyOneInsert == 2:
            print("В match больше одной вставки")
        else:
            print("В match отсутствует место вставки")