import os
import re
from typing import Optional
from typing import Literal
from constants import EXTENSIONS_FILE

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
        match = re.search(r'### match:\s*```(.*?)```', StringOfMarkdownContent, re.DOTALL)
        if match:
            return match.group(1).strip()
        else: raise ValueError("Match не найден")
    except  ValueError as e:
        print(f"Логическая ошибка: {e}")

def PatchLoadFromString(StringOfMarkdownContent):
    try:
        patch = re.search(r'### patch\s*```(.*?)```', StringOfMarkdownContent, re.DOTALL)
        patch = patch.group(1)
        if patch:
            if patch.startswith('\n'):
                patch = patch[1:]
            return  patch[:len(patch) - 1] if patch[len(patch) -1] == '\n' else patch
        else:
            raise ValueError("Patch не найден")
    except  ValueError as e:
        print(f"Логическая ошибка: {e}")


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
