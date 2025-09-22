import os
import subprocess
import tempfile
from Logging import setup_logger, log_function
from Utilities import ReadLine
import re

logger = setup_logger(log_file="my_app.log")


@log_function
def ReadFileContents(PathFile, MainBranch):
    try:
        NewLines = ReadLine(PathFile)
        OldLines = []

        RepositoryPath = os.path.relpath(PathFile, start=os.getcwd()).replace(os.sep, "/")
        OldContent = subprocess.check_output( ["git", "show", f"{MainBranch}:{RepositoryPath}"], text=True, encoding="utf-8" )
        OldLines = OldContent.splitlines(keepends=True)
    except subprocess.CalledProcessError as e:
        if "exists on disk, but not in" in str(e):
            logger.warning(f"Файл {PathFile} отсутствует в ветке {MainBranch}. Считаем старую версию пустой.")
        else:
            logger.error(f"Ошибка при получении старой версии файла из ветки {MainBranch}: {str(e)}")
    return {"NewLines": NewLines, "OldLines": OldLines}


@log_function
def CompareFileContents(NewLines, OldLines, PathFile):
    try:
        OldFiltered = ["".join(line.split()) for line in OldLines if "".join(line.split())]
        NewFiltered = ["".join(line.split()) for line in NewLines if "".join(line.split())]

        if OldFiltered == NewFiltered:
            logger.info(f"Файлы {PathFile} и его версия в git идентичны")
            return 0

        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", delete=False) as TemporaryFile:
            TemporaryFile.writelines(OldLines)
            OldFilePath = TemporaryFile.name

        try:
            DiffOutput = subprocess.check_output(
                [
                    "git",
                    "diff",
                    "--word-diff",
                    "--ignore-all-space",
                    "--no-index",
                    OldFilePath,
                    PathFile,
                ],
                text=True,
                encoding="utf-8",
            )
        except subprocess.CalledProcessError as e:
            DiffOutput = e.output
        finally:
            os.unlink(OldFilePath)

        if not DiffOutput:
            logger.error(f"Не удалось получить diff для файла {PathFile}")
            raise RuntimeError(f"Не удалось получить diff для файла {PathFile}")
        print(DiffOutput)
        return DiffOutput

    except Exception as e:
        logger.error(f"Ошибка при сравнении файлов {PathFile}: {str(e)}")
        raise


@log_function
def ParseDiffToTuples(DiffOutput):
    try:
        Changes = []
        CurrentOldLine =  1
        CurrentNewLine =  1

        for line in DiffOutput.splitlines():
            if line.startswith("@@"):
                try:
                    parts = line.split()
                    if len(parts) >= 3:
                        old_range = parts[1].lstrip("-").split(",")
                        new_range = parts[2].lstrip("+").split(",")

                        CurrentOldLine = int(old_range[0]) if old_range[0] != "0" else 0
                        CurrentNewLine = int(new_range[0]) if new_range[0] != "0" else 0

                except (IndexError, ValueError) as e:
                    logger.error(f"Ошибка при разборе строки diff: {line}, {str(e)}")
                    continue
                continue

            if line.startswith("[-"):
                deleted_word = line[2:-2].strip()
                if deleted_word:
                    Changes.append((CurrentOldLine, "delete", deleted_word))
                CurrentOldLine += 1
                continue

            if line.startswith("{+"):
                added_word = line[3:-2].strip()
                if added_word:
                    Changes.append((CurrentNewLine, "add", added_word))
                CurrentNewLine += 1
                continue

            if line.startswith("[") and line.endswith("]"):
                CurrentOldLine += 1
                CurrentNewLine += 1
                continue

            if line.startswith("-") and not line.startswith("---"):
                content = line[1:].rstrip("\n\r")
                words = re.findall(r"\b[a-zA-Z_][a-zA-Z0-9_]*\b|\d+", content)
                for word in words:
                    if word.strip() and not word.endswith("-"):
                        Changes.append((CurrentOldLine, "delete", word))
                CurrentOldLine += 1
                continue

            if line.startswith("+") and not line.startswith("+++"):
                content = line[1:].rstrip("\n\r+")
                words = re.findall(r"\b[a-zA-Z_][a-zA-Z0-9_]*\b|\d+", content)
                for word in words:
                    if word.strip() and not word.endswith("+"):
                        Changes.append((CurrentNewLine, "add", word))
                CurrentNewLine += 1
                continue

            if line.startswith(" "):
                CurrentOldLine += 1
                CurrentNewLine += 1

        if not Changes:
            logger.error("Изменения не обнаружены в diff")
            raise ValueError("Изменения не обнаружены в diff")
        return Changes
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
        Changes = ParseDiffToTuples(DiffResult)
        return Changes
    except Exception as e:
        logger.error(f"Ошибка в CompareFileVersions: {str(e)}")
        raise
