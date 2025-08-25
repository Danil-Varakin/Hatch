from SearchCode import SearchInsertIndexInSourceCode
from Utilities import ReadFile, WriteFile

def RunInsert(Match, Patch, SourceCode, SourcePath, OutPath):
    SearchResult = SearchInsertIndexInSourceCode(Match, SourceCode)
    if not SearchResult:
        return 0
    if "Replace" in SearchResult:
        CompletionStatus = Replace(Patch, SourcePath, OutPath, SearchResult)
    else:
        CompletionStatus = Insert(Patch, SourcePath, OutPath, SearchResult)
    if CompletionStatus == 0:
        return 0
    else:
        return 1


def Replace(Patch, SourcePath, OutPath, SearchResult):
    try:
        ReplacePosition, ReplaceCount, ReplaceSearchString = SearchResult['Replace']
        InsertPosition, InsertCount, InsertSearchString = SearchResult['Insert']
        SourceContent = ReadFile(SourcePath)
        InsertOccurrenceCount = 0
        ReplaceOccurrenceCount = 0
        InsertIndex = -1
        ReplaceIndex = -1
        for i in range(len(SourceContent)):
            if SourceContent.startswith(ReplaceSearchString, i) and ReplaceOccurrenceCount != ReplaceCount:
                ReplaceOccurrenceCount += 1
                if ReplaceOccurrenceCount == ReplaceCount:
                    ReplaceIndex = i
            if SourceContent.startswith(InsertSearchString, i) and InsertOccurrenceCount != InsertCount:
                InsertOccurrenceCount += 1
                if InsertOccurrenceCount == InsertCount:
                    InsertIndex = i
            if InsertOccurrenceCount == InsertCount and ReplaceOccurrenceCount == ReplaceCount:
                break
        if InsertIndex == -1 or ReplaceIndex == -1:
            raise ValueError('The insertion and/or replacement position was not found')
        if InsertPosition == 'Prev' and ReplacePosition == 'Next':
            ModifiedContent = SourceContent[:InsertIndex + len(InsertSearchString)] + Patch + SourceContent[ReplaceIndex:]
        elif InsertPosition == 'Next' and ReplacePosition == 'Next':
            ModifiedContent = SourceContent[:InsertIndex] + Patch + SourceContent[ReplaceIndex:]
        else:
            ModifiedContent = SourceContent[:InsertIndex] + Patch + SourceContent[ReplaceIndex + len(ReplaceSearchString):]

        WriteFile(OutPath, ModifiedContent)
        return 1
    except ValueError as e:
        print(f'Logic error: {e}')
        return 0


def Insert(Patch, SourcePath, OutPath, SearchResult):
    try:
        position, count, SearchString = SearchResult['Insert']
        SourceContent = ReadFile(SourcePath)
        OccurrenceCount = 0
        CharPosition = -1
        ModifiedContent = 0

        for i in range(len(SourceContent)):
            if SourceContent.startswith(SearchString, i):
                OccurrenceCount += 1
                if OccurrenceCount == count:
                    CharPosition = i
                    break

        if CharPosition == -1:
            raise ValueError('Insertion position not found')

        if position == 'Next':
            ModifiedContent = SourceContent[:CharPosition] + Patch + SourceContent[CharPosition:]
        elif position == 'Prev':
            ModifiedContent = SourceContent[:CharPosition + len(SearchString)] + Patch + SourceContent[CharPosition + len(SearchString):]

        WriteFile(OutPath, ModifiedContent)
        return 1
    except ValueError as e:
        print(f'Logic error: {e}')
        return 0