from SearchCode import SearchInsertIndexInSourceCode
from Utilities import ReadFile, WriteFile, AddingTabs
from Logging import setup_logger, log_function

logger = setup_logger()

@log_function(args=False, result=False)
def RunInsert(Match, Patch, SourceCode, SourcePath, OutPath, returnChangeEndIndex=False):
    SearchResult = SearchInsertIndexInSourceCode(Match, SourceCode)
    if not SearchResult:
        return 0
    if "Replace" in SearchResult:
        CompletionStatus = Replace(Patch, SourcePath, OutPath, SearchResult, returnChangeEndIndex)
    else:
        CompletionStatus = Insert(Patch, SourcePath, OutPath, SearchResult, returnChangeEndIndex)
    return CompletionStatus

@log_function(args=False, result=False)
def Replace(Patch, SourcePath, OutPath, SearchResult, returnChangeEndIndex=False):
    try:
        ReplacePosition, ReplaceCount, ReplaceSearchString = SearchResult['Replace']
        InsertPosition, InsertCount, InsertSearchString, CodeNestingLevel = SearchResult['Insert']
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

        while len(SourceContent) > ReplaceIndex + 1 and SourceContent[ReplaceIndex + 1].isspace():
            ReplaceIndex += 1
        while len(SourceContent) > InsertIndex + 1 and SourceContent[InsertIndex + 1].isspace():
            InsertIndex += 1

        Patch = AddingTabs(Patch, CodeNestingLevel)
        if InsertPosition == 'Prev' and ReplacePosition == 'Next':
            ModifiedContent = SourceContent[:InsertIndex + len(InsertSearchString)] + Patch + SourceContent[ReplaceIndex:]
            ChangeEndIndex = InsertIndex + len(InsertSearchString) + len(Patch)
        elif InsertPosition == 'Next' and ReplacePosition == 'Next':
            ModifiedContent = SourceContent[:InsertIndex] + Patch + SourceContent[ReplaceIndex:]
            ChangeEndIndex = InsertIndex  + len(Patch)
        else:
            ModifiedContent = SourceContent[:InsertIndex] + Patch + SourceContent[ReplaceIndex + len(ReplaceSearchString):]
            ChangeEndIndex = InsertIndex + len(Patch)
        WriteFile(OutPath, ModifiedContent)
        if returnChangeEndIndex:
            return 1, ChangeEndIndex
        else:
            return 1
    except ValueError as e:
        logger.error(f'Logic error: {e}')
        return 0

@log_function(args=False, result=False)
def Insert(Patch, SourcePath, OutPath, SearchResult, returnChangeEndIndex=False):
    try:
        position, count, SearchString, CodeNestingLevel = SearchResult['Insert']
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

        while len(SourceContent) > CharPosition + 1 and SourceContent[CharPosition + 1].isspace():
            CharPosition += 1

        Patch = AddingTabs(Patch, CodeNestingLevel)
        ChangeEndIndex = 0
        if position == 'Next':
            ModifiedContent = SourceContent[:CharPosition] + Patch + SourceContent[CharPosition:]
            ChangeEndIndex = CharPosition + len(Patch)
        elif position == 'Prev':
            ModifiedContent = SourceContent[:CharPosition + len(SearchString)] + Patch + SourceContent[CharPosition + len(SearchString):]
            ChangeEndIndex = CharPosition + len(SearchString) + len(Patch)
        WriteFile(OutPath, ModifiedContent)
        if returnChangeEndIndex:
            return 1, ChangeEndIndex
        else:
            return 1
    except ValueError as e:
        logger.error(f'Logic error: {e}')
        return 0