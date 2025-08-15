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
        return f"Ошибка: файл {FilePath} не найден"


def ReadLine(FilePath):
    try:
        with open(FilePath, 'r', encoding='utf-8') as file:
            return file.readlines()
    except FileNotFoundError:
        return f"Ошибка: файл {FilePath} не найден"


def WriteFile(FilePath, Result):
    try:
        with open(FilePath, 'w', encoding='utf-8') as file:
            file.write(Result)
    except FileNotFoundError:
        print( f"Ошибка: файл {FilePath} не найден")


def MatchLoadFromString(StringOfMarkdownContent):
    try:
        matches = re.findall(r'### match:\s*```(.*?)```', StringOfMarkdownContent, re.DOTALL)
        if matches:
            return [match.strip() for match in matches]
        else:
            raise ValueError("Match не найден")
    except ValueError as e:
        print(f"Логическая ошибка: {e}")
        return []

def PatchLoadFromString(StringOfMarkdownContent):
    try:
        patches = re.findall(r'### patch\s*```(.*?)```', StringOfMarkdownContent, re.DOTALL)
        if patches:
            return [patch[1:-1] if patch.startswith('\n') and patch.endswith('\n') else patch.strip() for patch in patches]
        else:
            raise ValueError("Patch не найден")
    except ValueError as e:
        print(f"Логическая ошибка: {e}")
        return []

def DetectProgrammingLanguage(FileNameSourceCode):
    ext = os.path.splitext(FileNameSourceCode)[1].lower()
    return EXTENSIONS_FILE.get(ext, 'Неизвестный язык')

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
            raise ValueError("Количество Match и Patch секций не совпадает")
        return True
    except ValueError as e:
        print(f"Логическая ошибка: {e}")
        return False

def FindNthNOperators(string, StartIndex):
    result = ""
    if StartIndex >= len(string):
        return result
    EndIndex = StartIndex
    if EndIndex < len(string) and string[EndIndex] == '_':
        EndIndex += 1
        Numbers = ""
        while EndIndex < len(string) and string[EndIndex].isdigit():
            Numbers += string[EndIndex]
            EndIndex += 1
        if EndIndex < len(string) and string[EndIndex] == '.' and Numbers:
            result = string[StartIndex: EndIndex + 1]
    return result

def IsPassToN(Token):
    return re.fullmatch(r"_\d+\.", Token)

def IsOnlyOneInsert(MatchTokenList):
    matches = [MatchToken for MatchToken in MatchTokenList if ">>>" in MatchToken]
    print(matches)
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
            raise ValueError(f"Ошибка: Файл {FilePath} не найден на диске.")

        CurrentVersion = ReadFile(FilePath)

        if not OldVersion:
            raise ValueError("Файл не найден при последнем commit")

        return {"OldVersion":OldVersion, "CurrentVersion": CurrentVersion}

    except subprocess.CalledProcessError as e:
        print (f"Ошибка запуска git diff: {e.stderr}")
    except FileNotFoundError as e:
        if str(e).lower().find('git') != -1:
            print("Ошибка: git не установлен или не найден под данному пути файла")
        print(f"Ошибка чтения файла: {str(e)}")
    except ValueError as e:
        print(f"Логическая ошибка: {str(e)}")
    except Exception as e:
        print(f"Не известная ошибка: {str(e)}")