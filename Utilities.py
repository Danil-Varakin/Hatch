import os
import re
from typing import Literal
from constants import EXTENSIONS_FILE
import subprocess

def ReadFile(FilePath):
    try:
        with open(FilePath, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: file {FilePath} not found")


def ReadLine(FilePath):
    try:
        with open(FilePath, 'r', encoding='utf-8') as file:
            return file.readlines()
    except FileNotFoundError:
        print(f"Error: file {FilePath} not found")


def WriteFile(FilePath, Result):
    try:
        with open(FilePath, 'w', encoding='utf-8') as file:
            file.write(Result)
    except FileNotFoundError:
        print(f"Error: file {FilePath} not found")


def MatchLoadFromString(StringOfMarkdownContent):
    try:
        matches = re.findall(r'### match:\s*```(.*?)```', StringOfMarkdownContent, re.DOTALL)
        if matches:
            return [match.strip() for match in matches]
        else:
            raise ValueError("Match not found")
    except ValueError as e:
        print(f"Logic error: {e}")
        return []

def PatchLoadFromString(StringOfMarkdownContent):
    try:
        patches = re.findall(r'### patch\s*```(.*?)```', StringOfMarkdownContent, re.DOTALL)
        if patches:
            return [patch[1:-1] if patch.startswith('\n') and patch.endswith('\n') else patch.strip() for patch in patches]
        else:
            raise ValueError("Patch not found")
    except ValueError as e:
        print(f"Logic error: {e}")
        return []

def DetectProgrammingLanguage(FileNameSourceCode):
    ext = os.path.splitext(FileNameSourceCode)[1].lower()
    return EXTENSIONS_FILE.get(ext, 'Unknown language')

def ReceivingMatchOrPatchOrSourceCodeFromList(FilePath, TypeContent: Literal['Match', 'Patch', 'SourceCode']):
    if TypeContent == 'Match':
        return MatchLoadFromString(ReadFile(FilePath))
    elif TypeContent == 'Patch':
        return PatchLoadFromString(ReadFile(FilePath))
    else:
        return ReadFile(FilePath)

def ComparingListsLength(matches, patches):
    try:
        if len(matches) != len(patches):
            raise ValueError("The number of Match and Patch sections does not match")
        return True
    except ValueError as e:
        print(f"Logic error: {e}")
        return False

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

def IsPassToN(Token):
    return re.fullmatch(r'\^[1-9]\d*\.\.', Token)

def InsertOperatorStatus(MatchTokenList):
    matches = [MatchToken for MatchToken in MatchTokenList if ">>>" in MatchToken]
    if matches:
        if len(matches) == 1:
            return 1
        else:
            return 2
    return 0

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
        print (f"Error run git diff: {e.stderr}")
    except FileNotFoundError as e:
        if str(e).lower().find('git') != -1:
            print("Error: git not installed or not found in this file path")
        print(f"File reading error: {str(e)}")
    except ValueError as e:
        print(f"Logic error: {str(e)}")
    except Exception as e:
        print(f"An unknown error: {str(e)}")

def FilteringListByOccurrence(FilterableList, FilterList):
    FilteredList = [
        (start, end) for start, end in FilterableList
        if not any(FilterTupleStart <= start < FilterTupleEnd for FilterTupleStart, FilterTupleEnd in FilterList)]
    return FilteredList


