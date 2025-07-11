from SearchCode import SearchInsertIndexInSourceCode
from ParsingCodeAndInstruction import ReadFile, WriteFile


def Insert(Match, Patch, SourceCode, SourcePath, OutPath):
    SearchResult = SearchInsertIndexInSourceCode(Match, SourceCode)
    if not SearchResult:
        return 0
    position, count, SearchString = SearchResult
    SourceContent = ReadFile(SourcePath)

    OccurrenceCount = 0
    CharPosition = -1

    for i in range(len(SourceContent)):
        if SourceContent.startswith(SearchString, i):
            OccurrenceCount += 1
            if OccurrenceCount == count:
                CharPosition = i
                break

    if CharPosition == -1:
        return 0

    if position == 'Next':
        ModifiedContent = SourceContent[:CharPosition] + Patch + SourceContent[CharPosition:]
    elif position == 'Prev':
        ModifiedContent = SourceContent[:CharPosition + len(SearchString)] + Patch + SourceContent[CharPosition + len(SearchString):]
    else:
        return 0
    WriteFile(OutPath, ModifiedContent)
    return 1
