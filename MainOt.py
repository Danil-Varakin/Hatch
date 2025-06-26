
import webview
from ParsingCodeAndInstruction import ReceivingMatchOrPatchOrSourceCodeFromListUI, MatchLoadFromString, PatchLoadFromString
from TokenizeCode import CheckAndRunTokenize
from SearchCode import SearchInsertIndexInTokenList, InsertNestingLevel, SearchInsertIndexInSourseCode, CheckMatchNestingMarkerPairs, PassInNestingMarkers
from Insert import Insert
ListOfCodeAndInstructionAndLanguage = ['test/unique3.md','file','source/unique3.cpp', 'file', 'cpp']
# ListOfCodeAndInstructionAndLanguage - List of [matchContent, matchType, sourceContent, sourceType, sourceLanguage]
Language = ListOfCodeAndInstructionAndLanguage[4]
Match = ReceivingMatchOrPatchOrSourceCodeFromListUI(ListOfCodeAndInstructionAndLanguage, True, MatchLoadFromString)
print(Match)
Patch = ReceivingMatchOrPatchOrSourceCodeFromListUI(ListOfCodeAndInstructionAndLanguage, True, PatchLoadFromString)
SourceCode = ReceivingMatchOrPatchOrSourceCodeFromListUI(ListOfCodeAndInstructionAndLanguage, False)
Match = CheckAndRunTokenize(Match, Language)
SourceCode = CheckAndRunTokenize(SourceCode, Language)
SearchDictionary = SearchInsertIndexInSourseCode(Match, SourceCode)
AAA = PassInNestingMarkers(6,Match)
NestingMap = CheckMatchNestingMarkerPairs(Match)
print(f"Source code TokenList: {SourceCode}")
print(f"Match nesting map: {NestingMap}")
print(f'AAAA{AAA}')
print(f"Insert index in sourcecode TokenList: {SearchDictionary}")
print(f"Source code TokenList len: {len(SourceCode) - 1}")

Insert(Match, Patch, SourceCode, 'source/unique3.cpp', F'C:/Users/droby/Documents/GitHub/Hatch/source/result1.cpp')
