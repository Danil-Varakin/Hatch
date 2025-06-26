from SearchCode import SearchInsertIndexInSourseCode
from ParsingCodeAndInstruction import ReadLine, WriteLine


def Insert(Match, Patch, SourceCode, SourcePath, OutPath):
    if SearchInsertIndexInSourseCode(Match, SourceCode):
        position, count, SearchString = SearchInsertIndexInSourseCode(Match, SourceCode)
    else:
        return 0

    lines = ReadLine(SourcePath)
    if isinstance(lines, str):
        print(f"Ошибка чтения файла {SourcePath}: {lines}")
        return False

    occurrence = 0
    found = False
    ResultLines = []

    for i, line in enumerate(lines):
        if SearchString in line and occurrence < count:
            occurrence += 1
            if occurrence == count:
                found = True
                indent = ''
                for char in line:
                    if char in ' \t':
                        indent += char
                    else:
                        break
                before, after = line.split(SearchString, 1)
                patch_lines = Patch.splitlines()
                indented_patch_lines = [indent + pl for pl in patch_lines]

                if position == 'Next':
                    ResultLines.append(before + SearchString)
                    ResultLines.extend(indented_patch_lines)
                    if after.strip():
                        ResultLines.append(indent + after)
                elif position == 'Prev':
                    ResultLines.append(before)
                    ResultLines.extend(indented_patch_lines)
                    ResultLines.append(indent + SearchString + after)
                else:
                    ResultLines.append(line)
                    return False
            else:
                ResultLines.append(line)
        else:
            ResultLines.append(line)

    if not found:
        return False

    WriteLine(OutPath, ResultLines)
    print(f"Файл {OutPath} успешно обновлён")
    return True