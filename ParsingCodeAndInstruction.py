import os
import re
from typing import Optional
from typing import Literal

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


def WriteLine(FilePath, ResultLines):
    try:
        with open(FilePath, 'w', encoding='utf-8') as file:
            return file.writelines(ResultLines)
    except FileNotFoundError:
        return f"Ошибка: файл {FilePath} не найден"


def MatchLoadFromString(StringOfMarkdownContent):
    match = re.search(r'### match:\s*```(.*?)```', StringOfMarkdownContent, re.DOTALL)
    return match.group(1).strip() if match else None

def PatchLoadFromString(StringOfMarkdownContent):
    patch = re.search(r'### patch\s*```(.*?)```', StringOfMarkdownContent, re.DOTALL)
    return patch.group(1).strip() if patch else None

def DetectProgrammingLanguage(FileNameSourceCode):
    extensions = {
    '.py': 'python', '.java': 'java', '.cpp': 'cpp',
    '.c': 'c', '.cs': 'csharp', '.js': 'javascript',
    '.rb': 'ruby', '.ts': 'typescript', '.go': 'go',
    '.rs': ' ', '.md': 'markdown' }
    ext = os.path.splitext(FileNameSourceCode)[1].lower()
    return extensions.get(ext, 'Неизвестный язык')

def ReceivingMatchOrPatchOrSourceCodeFromListUI(ListOfCodeAndInstructionAndLanguage,IsInstruction, functionMatchOrPatch: Optional = None):
    if IsInstruction:
        if functionMatchOrPatch is None: raise ValueError("match_or_patch_function must be provided when is_instruction is True")

        elif ListOfCodeAndInstructionAndLanguage[1] == 'text': return  functionMatchOrPatch( ListOfCodeAndInstructionAndLanguage[0] )

        else: return functionMatchOrPatch(ReadFile( ListOfCodeAndInstructionAndLanguage[0]) )
    else:
        if ListOfCodeAndInstructionAndLanguage[3] != 'text': return ReadFile( ListOfCodeAndInstructionAndLanguage[2] )

        else: return ListOfCodeAndInstructionAndLanguage[2]


def ReceivingMatchOrPatchOrSourceCodeFromList(FilePath, TypeContent: Literal['Match', 'Patch', 'SourceCode']):
    if TypeContent == 'Match':
        return MatchLoadFromString(ReadFile(FilePath))
    elif TypeContent == 'Patch':
        return PatchLoadFromString(ReadFile(FilePath))
    else:
        return ReadFile(FilePath)
