
import webview
from ParsingCodeAndInstruction import ReceivingMatchOrPatchOrSourceCodeFromListUI, MatchLoadFromString, PatchLoadFromString
from TokenizeCode import CheckAndRunTokenize, detect_programming_language
from SearchCode import SearchInsertIndexInTokenList, MatchNestingLevelInsertALL, SearchInsertIndexInSourseCode, CheckMatchNestingMarkerPairs, PassInNestingMarkers
from Insert import Insert
ListOfCodeAndInstructionAndLanguage = ['test/PassedTests/unique13.md','file','test/PassedTests/unique13.cpp', 'file', 'cpp']
# ListOfCodeAndInstructionAndLanguage - List of [matchContent, matchType, sourceContent, sourceType, sourceLanguage]
Language = ListOfCodeAndInstructionAndLanguage[4]
Match = ReceivingMatchOrPatchOrSourceCodeFromListUI(ListOfCodeAndInstructionAndLanguage, True, MatchLoadFromString)
Patch = ReceivingMatchOrPatchOrSourceCodeFromListUI(ListOfCodeAndInstructionAndLanguage, True, PatchLoadFromString)
SourceCode = ReceivingMatchOrPatchOrSourceCodeFromListUI(ListOfCodeAndInstructionAndLanguage, False)
Match = CheckAndRunTokenize(Match, Language)
SourceCode = CheckAndRunTokenize(SourceCode, Language)
SearchDictionary = SearchInsertIndexInSourseCode(Match, SourceCode)
dddd = detect_programming_language( 'def CheckMatchNestingMarkerPairs(MatchTokenList: list[tuple]):=')
AAA = PassInNestingMarkers(4,Match)
NestingMap = MatchNestingLevelInsertALL(Match)
print(f"Source code TokenList: {SourceCode}")
print(f"Match nesting map: {NestingMap}")
print(f'AAAA{dddd}')
print(f"Insert index in sourcecode TokenList: {SearchDictionary}")
print(f"Source code TokenList len: {len(SourceCode) - 1}")

#Insert(Match, Patch, SourceCode, ListOfCodeAndInstructionAndLanguage[2], F'C:/Users/droby/Documents/GitHub/Hatch/test/result1.cpp')
