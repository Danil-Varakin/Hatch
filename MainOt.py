
import webview
from ParsingCodeAndInstruction import ReceivingMatchOrPatchOrSourceCodeFromListUI, MatchLoadFromString, PatchLoadFromString
from TokenizeCode import CheckAndRunTokenize
from SearchCode import SearchInsertIndexInTokenList, InsertNestingLevel, SearchInsertIndexInSourseCode, CheckMatchNestingMarkerPairs, PassInNestingMarkers
from Insert import Insert
ListOfCodeAndInstructionAndLanguage = ['test/unique7.md','file','source/unique7.cpp', 'file', 'cpp']
# ListOfCodeAndInstructionAndLanguage - List of [matchContent, matchType, sourceContent, sourceType, sourceLanguage]
Language = ListOfCodeAndInstructionAndLanguage[4]
Match = ReceivingMatchOrPatchOrSourceCodeFromListUI(ListOfCodeAndInstructionAndLanguage, True, MatchLoadFromString)
print(Match)
Patch = ReceivingMatchOrPatchOrSourceCodeFromListUI(ListOfCodeAndInstructionAndLanguage, True, PatchLoadFromString)
SourceCode = ReceivingMatchOrPatchOrSourceCodeFromListUI(ListOfCodeAndInstructionAndLanguage, False)
Match = CheckAndRunTokenize(Match, Language)
SourceCode = CheckAndRunTokenize(SourceCode, Language)
SearchDictionary = SearchInsertIndexInTokenList(Match, SourceCode)
AAA = PassInNestingMarkers(6,Match)
#InsertIndexInSourseCode = SearchInsertIndexInSourseCode(Match, SourceCode)
NestingMap = CheckMatchNestingMarkerPairs(Match)
#print(f"Match TokenList: {Match}")
print(f"Source code TokenList: {SourceCode}")
print(f"Match nesting map: {NestingMap}")
print(f'AAAA{AAA}')
print(f"Insert index in sourcecode TokenList: {SearchDictionary}")
print(f"Source code TokenList len: {len(SourceCode) - 1}")
#print(f"Insert index in source code: {InsertIndexInSourseCode}")

#Insert(Match, Patch, SourceCode, 'C:/Users/droby/Desktop/Hatch/test/aaa.cpp', True)
