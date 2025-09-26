import os
import re
from typing import Literal
from constants import EXTENSIONS_FILE
import subprocess
from Logging import setup_logger, log_function

logger = setup_logger(log_file='my_app.log')

@log_function
def ReadFile(FilePath, encoding='utf-8'):
    try:
        with open(FilePath, 'r', encoding = encoding) as file:
            return file.read()
    except FileNotFoundError:
        logger.error(f"Error: file {FilePath} not found")


@log_function
def ReadLine(FilePath):
    try:
        with open(FilePath, 'r', encoding='utf-8') as file:
            return file.readlines()
    except FileNotFoundError:
        logger.error(f"Error: file {FilePath} not found")

@log_function
def WriteFile(FilePath, Result):
    try:
        with open(FilePath, 'w', encoding='utf-8') as file:
            file.write(Result)
    except FileNotFoundError:
        logger.error(f"Error: file {FilePath} not found")

@log_function
def MatchLoadFromString(StringOfMarkdownContent):
    try:
        matches = re.findall(r'### match\s*```(.*?)```', StringOfMarkdownContent, re.IGNORECASE | re.DOTALL)
        if matches:
            return [match.strip() for match in matches]
        else:
            raise ValueError("Match not found")
    except ValueError as e:
        logger.error(f"Logic error: {e}")
        return []

@log_function
def PatchLoadFromString(StringOfMarkdownContent):
    try:
        patches = re.findall(r'### patch\s*```(.*?)```', StringOfMarkdownContent, re.IGNORECASE | re.DOTALL)
        if patches:
            return [patch[1:-1] if patch.startswith('\n') and patch.endswith('\n') else patch.strip() for patch in patches]
        else:
            raise ValueError("Patch not found")
    except ValueError as e:
        logger.error(f"Logic error: {e}")
        return []

@log_function
def DetectProgrammingLanguage(FileNameSourceCode):
    try:
        ext = os.path.splitext(FileNameSourceCode)[1].lower()
        Language = EXTENSIONS_FILE.get(ext, None)
        if not Language:
            raise ValueError ("Unknown language")
        return Language
    except ValueError as e:
        logger.error(f"Logic error: {e}")

@log_function
def ReceivingMatchOrPatchOrSourceCodeFromList(FilePath, TypeContent: Literal['Match', 'Patch', 'SourceCode']):
    if TypeContent == 'Match':
        return MatchLoadFromString(ReadFile(FilePath))
    elif TypeContent == 'Patch':
        return PatchLoadFromString(ReadFile(FilePath))
    else:
        return ReadFile(FilePath)

@log_function
def ComparingListsLength(matches, patches):
    try:
        if len(matches) != len(patches):
            raise ValueError("The number of Match and Patch sections does not match")
        return True
    except ValueError as e:
        logger.error(f"Logic error: {e}")
        return False

@log_function
def FindNthNOperators(string, StartIndex):
    result = ""
    if StartIndex >= len(string):
        return result
    EndIndex = StartIndex
    if EndIndex < len(string) and string[EndIndex] == '^':
        EndIndex += 1
        Numbers = ""
        while EndIndex < len(string) and string[EndIndex].isdigit():
            Numbers += string[EndIndex]
            EndIndex += 1
        if EndIndex < len(string) and string[EndIndex:EndIndex + 2] == '..' and Numbers:
            result = string[StartIndex: EndIndex + 2]
    return result

@log_function
def IsPassToN(Token):
    return re.fullmatch(r'\^[1-9]\d*\.\.', Token)

@log_function
def InsertOperatorStatus(MatchTokenList):
    matches = [MatchToken for MatchToken in MatchTokenList if ">>>" in MatchToken]
    if matches:
        if len(matches) == 1:
            return 1
        else:
            return 2
    return 0

def AddingTabs(string, CodeNestingLevel):
    if '\n' in string:
        patch_lines = string.split('\n')
        indented_lines = []
        IsFirstLine = True
        for line in patch_lines:
            if line and not IsFirstLine:
                indented_lines.append('\t' * CodeNestingLevel + line)
            else:
                indented_lines.append(line)
            IsFirstLine = False
        string = '\n'.join(indented_lines)
        if string[len(string) - 1] == "\n":
            string = string + '\t' * CodeNestingLevel
    return string
@log_function
def GetFileOldAndNewVersion(FilePath):
    try:
        OldVersionResult = subprocess.run(
            ['git', 'show', f'HEAD:{FilePath}'],
            capture_output=True,
            text=True,
            check=True
        )
        OldVersion = OldVersionResult.stdout
        if not os.path.exists(FilePath):
            raise ValueError(f"Error: file {FilePath} not found on disk.")

        CurrentVersion = ReadFile(FilePath)

        if not OldVersion:
            raise ValueError("File not found in last commit")

        return {"OldVersion":OldVersion, "CurrentVersion": CurrentVersion}

    except subprocess.CalledProcessError as e:
        logger.critical(f"Error run git diff: {e.stderr}")
    except FileNotFoundError as e:
        if str(e).lower().find('git') != -1:
            logger.error("Error: git not installed or not found in this file path")
        logger.critical(f"File reading error: {str(e)}")
    except ValueError as e:
        logger.error(f"Logic error: {str(e)}")
    except Exception as e:
        logger.critical(f"An unknown error: {str(e)}")

@log_function
def FilteringListByOccurrence(FilterableList, FilterList):
    FilteredList = [
        (start, end) for start, end in FilterableList
        if not any(FilterTupleStart <= start < FilterTupleEnd for FilterTupleStart, FilterTupleEnd in FilterList)]
    return FilteredList


