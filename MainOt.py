from ParsingCodeAndInstruction import (
    ReceivingMatchOrPatchOrSourceCodeFromListUI,
    MatchLoadFromString,
    PatchLoadFromString,
)
from TokenizeCode import CheckAndRunTokenize
from SearchCode import (
    MatchNestingLevelInsertALL,
    SearchInsertIndexInSourseCode,
    PassInNestingMarkers,
    SearchInsertIndexInTokenList,
    CheckMatchNestingMarkerPairs,
    GetBracketIndicesForEllipsis, ComparisonToken
)

ListOfCodeAndInstructionAndLanguage = [ "test/PassedTests/unique8.md","file","test/PassedTests/unique8.cpp","file","cpp",]
# ListOfCodeAndInstructionAndLanguage - List of [matchContent, matchType, sourceContent, sourceType, sourceLanguage]
Language = ListOfCodeAndInstructionAndLanguage[4]
Match = ReceivingMatchOrPatchOrSourceCodeFromListUI(ListOfCodeAndInstructionAndLanguage, True, MatchLoadFromString)
Patch = ReceivingMatchOrPatchOrSourceCodeFromListUI(ListOfCodeAndInstructionAndLanguage, True, PatchLoadFromString)
SourceCode = ReceivingMatchOrPatchOrSourceCodeFromListUI(ListOfCodeAndInstructionAndLanguage, False)
Match = CheckAndRunTokenize(Match, Language)
SourceCode = CheckAndRunTokenize(SourceCode, Language)
FFFF = MatchNestingLevelInsertALL(Match)
sss = GetBracketIndicesForEllipsis(Match)
# SearchDictionary = SearchInsertIndexInSourseCode(Match, SourceCode)
# AAA = PassInNestingMarkers(4,Match)
GGG = SearchInsertIndexInTokenList(Match, SourceCode)
print(f" Match: {Match}")
print(f"Source code TokenList: {SourceCode}")
print(f"CheckMatchNestingMarkerPairs: {GGG}")

# print(f"Match nesting map: {NestingMap}")
# print(f"Insert index in sourcecode TokenList: {SearchDictionary}")
# print(f"Source code TokenList len: {len(SourceCode) - 1}")

# Insert(Match, Patch, SourceCode, ListOfCodeAndInstructionAndLanguage[2], F'/test/result1.cpp')
