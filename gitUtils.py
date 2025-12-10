import os
import re
import tempfile
import subprocess
from Logging import setup_logger, log_function

logger = setup_logger()

@log_function(args=False, result=False)
def NormalizePathToGitPath(FilePath):
    try:
        GitRoot = subprocess.check_output(['git', 'rev-parse', '--show-toplevel'], stderr=subprocess.STDOUT,
                                          text=True).strip()
        AbstractPath = os.path.abspath(FilePath)
        RelPath = os.path.relpath(AbstractPath, GitRoot)
        GitPath = RelPath.replace('\\', '/')
        return GitPath
    except subprocess.CalledProcessError as e:
        logger.error(e.output)


@log_function(args=False, result=False)
def ReadLastGitCommit(FilePath, MainBranch, splitLines=False):
    try:
        GitPath = NormalizePathToGitPath(FilePath)
        RepositoryPath = os.path.relpath(GitPath, start=os.getcwd()).replace(os.sep, "/")
        Content = subprocess.check_output(
            ["git", "show", f"{MainBranch}:{RepositoryPath}"],
            text=True,
            encoding="utf-8")
        if splitLines:
            Lines = Content.splitlines(keepends=True)
            return Lines
        else:
            return Content
    except subprocess.CalledProcessError as e:
        if "exists on disk, but not in" in str(e):
            logger.error(f"Файл {FilePath} отсутствует в ветке {MainBranch}.")
        else:
            logger.error(f"Ошибка при получении старой версии файла из ветки {MainBranch}: {str(e)}")
        return 0

@log_function(args=False, result=False)
def GetDiffOutput(FileLines, FilePath):
    try:
        GitPath = NormalizePathToGitPath(FilePath)
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", delete=False) as TemporaryFile:
            TemporaryFile.writelines(FileLines)
            OldFilePath = TemporaryFile.name
        try:
            DiffOutput = subprocess.check_output([
                "git", "diff", "--diff-algorithm=histogram",  "--ignore-all-space", "--no-index", OldFilePath, GitPath],
                text=True, encoding="utf-8")
        except subprocess.CalledProcessError as e:
            DiffOutput = e.output
        finally:
            os.unlink(OldFilePath)

        if not DiffOutput:
            raise ValueError(f"Нет различий в файле {FilePath} (или только пробелы)")
        return DiffOutput

    except Exception as e:
        logger.error(f"Ошибка при сравнении файлов {FilePath}: {str(e)}")
        return 0

@log_function(args=False, result=False)
def FilterDiffOutput(DiffOutput):
    try:
        lines = DiffOutput.splitlines()
        InDiffBlock = False
        change = []
        StartIndexDiffBlock = []
        for indexLineInDiff, line in enumerate(lines):
            if line.startswith("@@"):
                StartIndexDiffBlock.append([indexLineInDiff])
                if InDiffBlock:
                    StartIndexDiffBlock[-2].append(indexLineInDiff-1)
                    if not change:
                        StartIndexDiffBlock[-2].append(False)
                    else:
                        StartIndexDiffBlock[-2].append(True)
                change = []
                InDiffBlock = True
                continue

            if not InDiffBlock:
                continue
            pattern = re.compile(r"\[-.*?-]|\{\+.*?\+}", re.DOTALL)

            for match in pattern.finditer(line):
                ChangeStr = match.group(0)
                changed = ChangeStr[2:-2]
                changed = re.sub(r'[\s\x00-\x1F\x7F]', '', changed)
                if changed:
                    change.append(changed)
        if not StartIndexDiffBlock:
            return DiffOutput
        if len(StartIndexDiffBlock[-1]) != 3:
            StartIndexDiffBlock[-1].append(len(lines)-1)
            if change:
                StartIndexDiffBlock[-1].append(True)
            else:
                StartIndexDiffBlock[-1].append(False)
        current_pos = 0
        result = []
        ISHaveChange = False
        for start, end, keep in StartIndexDiffBlock:
            if current_pos < start:
                result.extend(lines[current_pos:start])
            if keep:
                result.extend(lines[start:end + 1])
                ISHaveChange = True
            current_pos = end + 1
        return "\n".join(result) if ISHaveChange else 0
    except Exception as e:
        logger.error(f"Ошибка при фильтрации diff: {str(e)}")
        return 0