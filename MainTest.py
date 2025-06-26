import os
from ParsingCodeAndInstruction import ReceivingMatchOrPatchOrSourceCodeFromListUI, MatchLoadFromString, PatchLoadFromString
from TokenizeCode import  CheckAndRunTokenize
from SearchCode import SearchInsertIndexInTokenList, InsertNestingLevel, SearchInsertIndexInSourseCode, CheckMatchNestingMarkerPairs, MatchNestingLevelInsertALL
from Insert import Insert

TestFolder = "test"
SourceFolder = "source"
results = []
TestFiles = [f for f in os.listdir(TestFolder) if f.endswith(".md")]
SourceFiles = [f for f in os.listdir(SourceFolder) if f.endswith(".cpp")]
print(TestFiles,SourceFiles)
pairs = []

for TestFile in TestFiles:
    BaseName = os.path.splitext(TestFile)[0]
    SourceFile = f"{BaseName}.cpp"
    if SourceFile in SourceFiles:
        pairs.append((os.path.join(TestFolder, TestFile), os.path.join(SourceFolder, SourceFile)))
i = 0
# ListOfCodeAndInstructionAndLanguage - List of [matchContent, matchType, sourceContent, sourceType, sourceLanguage]
for TestPath, SourcePath in pairs:
    i += 1
    base_name = os.path.splitext(os.path.basename(TestPath))[0]
    print(f"\n=== Processing files: {TestPath} and {SourcePath} ===")
    ListOfCodeAndInstructionAndLanguage = [TestPath, "file", SourcePath, "file", "cpp"]
    Language = ListOfCodeAndInstructionAndLanguage[4]

    Match = ReceivingMatchOrPatchOrSourceCodeFromListUI(ListOfCodeAndInstructionAndLanguage, True, MatchLoadFromString)
    Patch = ReceivingMatchOrPatchOrSourceCodeFromListUI(ListOfCodeAndInstructionAndLanguage, True, PatchLoadFromString)
    SourceCode = ReceivingMatchOrPatchOrSourceCodeFromListUI(ListOfCodeAndInstructionAndLanguage, False)
    Match = CheckAndRunTokenize(Match, Language)
    SourceCode = CheckAndRunTokenize(SourceCode, Language)
    SearchDictionary = SearchInsertIndexInTokenList(Match, SourceCode)
    NestingLevel = InsertNestingLevel(Match)
    MatchL = InsertNestingLevel(Match)
    InsertIndexInSourseCode = SearchInsertIndexInSourseCode(Match, SourceCode)
    NestingMap = MatchNestingLevelInsertALL(Match)
    IsNestingMarkerPairsList = CheckMatchNestingMarkerPairs(Match)
    Insert(Match, Patch, SourceCode, SourcePath, F'C:/Users/droby/Documents/GitHub/Hatch/source/result{i}.cpp')

    ResultTuple = (
        Match,
        SourceCode,
        NestingMap,
        MatchL,
        SearchDictionary,
        len(SourceCode) - 1,
        InsertIndexInSourseCode,
        base_name
    )
    results.append(ResultTuple)

print("=== All Processing Results ===")
for result in results:
    Match, SourceCode, NestingMap, MatchL, SearchDictionary, source_len, InsertIndexInSourseCode, base_name = result
    print(f"\n=== Results for {base_name} ===")
    print(f"Match nesting map: {NestingMap}")
    print(f"Match nesting: {MatchL}")
    print(f"Insert index in sourcecode TokenList: {SearchDictionary}")
    print(f"Source code TokenList len: {source_len}")
    print(f"Insert index in source code: {InsertIndexInSourseCode}")
    print(f"=== End results for {base_name} ===\n")
print("=== End of All Results ===")