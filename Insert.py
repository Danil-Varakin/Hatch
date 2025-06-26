from SearchCode import SearchInsertIndexInSourseCode
from ParsingCodeAndInstruction import ReadFile, WriteFile


def Insert(Match, Patch, SourceCode, SourcePath, OutPath, add_newline=True):
    search_result = SearchInsertIndexInSourseCode(Match, SourceCode)
    if not search_result:
        return 0
    position, count, search_string = search_result
    source_content = ReadFile(SourcePath)

    occurrence_count = 0
    char_position = -1

    for i in range(len(source_content)):
        if source_content.startswith(search_string, i):
            occurrence_count += 1
            if occurrence_count == count:
                char_position = i
                break

    if char_position == -1:
        return 0
    patch_text = f"\n{Patch}" if add_newline else Patch

    if position == 'Next':
        modified_content = source_content[:char_position] + patch_text + source_content[char_position:]
    elif position == 'Prev':
        modified_content = source_content[:char_position + len(search_string)] + patch_text + source_content[char_position + len(search_string):]
    else:
        return 0
    WriteFile(modified_content)
    return 1
