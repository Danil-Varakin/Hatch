from ParsingCodeAndInstruction import ReceivingMatchOrPatchOrSourceCodeFromListUI,MatchLoadFromString, PatchLoadFromString, ReadFile
from TokenizeCode import CheckAndRunTokenize
from SearchCode import  MatchNestingLevelInsertALL, SearchInsertIndexInSourceCode, PassInNestingMarkers, SearchInsertIndexInTokenList, CheckMatchNestingMarkerPairs, GetBracketIndicesForEllipsis, ComparisonToken, UpdateUnpairedMarkers
from Insert import RunInsert
ListOfCodeAndInstructionAndLanguage = [ "test/PassedTests/unique3.md","file","test/PassedTests/unique3.cpp","file","cpp",]
# ListOfCodeAndInstructionAndLanguage - List of [matchContent, matchType, sourceContent, sourceType, sourceLanguage]
Language = ListOfCodeAndInstructionAndLanguage[4]
Match = ReceivingMatchOrPatchOrSourceCodeFromListUI(ListOfCodeAndInstructionAndLanguage, True, MatchLoadFromString)
Patch = ReceivingMatchOrPatchOrSourceCodeFromListUI(ListOfCodeAndInstructionAndLanguage, True, PatchLoadFromString)
SourceCode = ReceivingMatchOrPatchOrSourceCodeFromListUI(ListOfCodeAndInstructionAndLanguage, False)
Match = CheckAndRunTokenize(Match, Language)
SourceCode = CheckAndRunTokenize(SourceCode, Language)
FFFF = MatchNestingLevelInsertALL(Match)
sss = UpdateUnpairedMarkers(Match)
# AAA = PassInNestingMarkers(4,Match)
GGG = SearchInsertIndexInTokenList(Match, SourceCode)
print(f" Match: {Match}")
print(f"Source code TokenList: {SourceCode}")
print(f"CheckMatchNestingMarkerPairs: {GGG}")
SearchDictionary = SearchInsertIndexInSourceCode(Match, SourceCode)
# print(f"Match nesting map: {NestingMap}")
print(f"Insert index in sourcecode TokenList: {SearchDictionary}")

#RunInsert(Match, Patch, SourceCode, ListOfCodeAndInstructionAndLanguage[2], 'result1.cpp')
