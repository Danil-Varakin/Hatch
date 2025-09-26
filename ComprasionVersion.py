import os
import subprocess
import tempfile
from Logging import setup_logger, log_function
from Utilities import ReadLine, ReadFile
import re
import ast

logger = setup_logger(log_file="CodeComprasion/my_app.log")

@log_function
def ReadFileContents(PathFile, MainBranch):
    try:
        NewLines = ReadLine(PathFile)
        RepositoryPath = os.path.relpath(PathFile, start=os.getcwd()).replace(os.sep, "/")
        OldContent = subprocess.check_output(
            ["git", "show", f"{MainBranch}:{RepositoryPath}"],
            text=True,
            encoding="utf-8")
        OldLines = OldContent.splitlines(keepends=True)
        return {"NewLines": NewLines, "OldLines": OldLines}
    except subprocess.CalledProcessError as e:
        if "exists on disk, but not in" in str(e):
            logger.warning(f"Файл {PathFile} отсутствует в ветке {MainBranch}. Считаем старую версию пустой.")
            return {"NewLines": ReadLine(PathFile), "OldLines": []}
        else:
            logger.error(f"Ошибка при получении старой версии файла из ветки {MainBranch}: {str(e)}")
            raise


@log_function
def CompareFileContents(NewLines, OldLines, PathFile):
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", delete=False) as TemporaryFile:
            TemporaryFile.writelines(OldLines)
            OldFilePath = TemporaryFile.name

        try:
            DiffOutput = subprocess.check_output([
                    "git",
                    "diff",
                    "--word-diff",
                    "--ignore-all-space",
                    "--no-index",
                    OldFilePath,
                    PathFile],
                text=True,
                encoding="utf-8")
        except subprocess.CalledProcessError as e:
            DiffOutput = e.output
        finally:
            os.unlink(OldFilePath)

        if not DiffOutput:
            logger.info(f"Нет различий в файле {PathFile} (или только пробелы)")
            return 0

        return DiffOutput

    except Exception as e:
        logger.error(f"Ошибка при сравнении файлов {PathFile}: {str(e)}")
        raise


@log_function
def ParseDiffToTuples(DiffOutput):
    try:
        result = []
        lines = DiffOutput.splitlines()

        pattern = re.compile(r"\[-.*?-\]|\{\+.*?\+\}", re.DOTALL)

        current_line_number = 0
        in_diff_block = False

        for line in lines:
            if line.startswith("@@"):
                in_diff_block = True
                match = re.search(r"@@ -(\d+),\d+ \+(\d+),\d+ @@", line)
                if match:
                    current_line_number = int(match.group(2)) - 1
                continue

            if not in_diff_block:
                continue

            is_full_delete = line.startswith('[-') and line.endswith('-]')
            is_full_add = line.startswith('{+') and line.endswith('+}')

            if is_full_delete:
                line_num = current_line_number + 1
                deleted = line[2:-2]
                result.append((line_num, 'delete', 0, 0, '', deleted))
                continue

            if is_full_add:
                current_line_number += 1
                line_num = current_line_number
                added = line[2:-2]
                result.append((line_num, 'add', 0, len(added), added, ''))
                continue

            current_line_number += 1
            line_num = current_line_number
            changes = []
            pos = 0
            last_end = 0
            last_change = None

            for match in pattern.finditer(line):
                common = line[last_end:match.start()]
                pos += len(common)

                change_str = match.group(0)
                if change_str.startswith('[-'):
                    content = change_str[2:-2]
                    new_change = {'type': 'delete','start': pos,'end': pos,'added': '','deleted': content}
                else:
                    content = change_str[2:-2]
                    new_change = {'type': 'add','start': pos,'end': pos + len(content),'added': content,'deleted': ''}

                if last_change and last_change['type'] == 'delete' and last_change['end'] == new_change['start'] and last_end == match.start():
                    last_change['type'] = 'replace'
                    last_change['end'] = new_change['end']
                    last_change['added'] = new_change['added']
                else:
                    changes.append(new_change)
                pos = new_change['end']

                last_end = match.end()
                last_change = changes[-1] if changes else None
            pos += len(line[last_end:])

            for ch in changes:
                result.append((line_num, ch['type'], ch['start'], ch['end'], ch['added'], ch['deleted']))

        if not result:
            logger.warning("Не найдено изменений в diff-выводе")

        return result

    except Exception as e:
        logger.error(f"Ошибка при разборе diff: {str(e)}")
        raise


@log_function
def CompareFileVersions(PathFile, MainBranch="main"):
    try:
        FileLines = ReadFileContents(PathFile, MainBranch)
        DiffResult = CompareFileContents(
            FileLines["NewLines"], FileLines["OldLines"], PathFile
        )
        if DiffResult == 0:
            return 0
        Changes = ConvertDiffToIndices(ParseDiffToTuples(DiffResult), PathFile)
        return Changes
    except Exception as e:
        logger.error(f"Ошибка в CompareFileVersions: {str(e)}")
        raise


@log_function
def ConvertDiffToIndices(diff_tuples, PathFile):
    try:
        merged = []
        prev = None
        for tup in diff_tuples:
            line, action, rel_start, rel_end, added, deleted = tup
            if action == 'delete' and prev and prev[0] == line and prev[1] == action and prev[2] == rel_start:
                prev_deleted = prev[5] + '\n' + deleted if prev[5] else deleted
                prev = (line, action, rel_start, rel_end, added, prev_deleted)
            else:
                if prev:
                    merged.append(prev)
                prev = tup
        if prev:
            merged.append(prev)

        result = []
        NewContent = ReadFile(PathFile)
        lines = NewContent.splitlines(keepends=True)
        if not lines:
            logger.warning("NewContent пустой, но продолжаем обработку")

        line_starts = [0]
        current_pos = 0
        for line in lines:
            current_pos += len(line)
            line_starts.append(current_pos)

        num_lines = len(lines)

        for line_number, action, rel_start, rel_end, added, deleted in merged:
            if line_number > num_lines + 1:
                logger.warning(f"Неверный line_number {line_number} для файла с {num_lines} строками")
                continue

            base_pos = line_starts[min(line_number - 1, num_lines)]
            abs_start = base_pos + rel_start
            abs_end = base_pos + rel_end

            result.append((line_number, action, abs_start, abs_end, added, deleted))

        if not result:
            logger.warning("Не найдено изменений для преобразования в индексы")

        return result

    except Exception as e:
        logger.error(f"Ошибка при преобразовании diff в индексы: {str(e)}")
        raise

