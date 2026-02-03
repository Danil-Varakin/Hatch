import os
import re
import importlib
import subprocess
from typing import Literal
from constants import EXTENSIONS_FILE
from Logging import setup_logger, log_function

logger = setup_logger()

@log_function(args=False, result=False)
def ReadFile(FilePath, encoding='utf-8'):
    try:
        with open(FilePath, 'r', encoding = encoding) as file:
            return file.read()
    except FileNotFoundError:
        logger.error(f"Error: file {FilePath} not found")


@log_function(args=False, result=False)
def ReadLine(FilePath):
    try:
        with open(FilePath, 'r', encoding='utf-8') as file:
            return file.readlines()
    except FileNotFoundError:
        logger.error(f"Error: file {FilePath} not found")

@log_function(args=False, result=False)
def WriteFile(FilePath, Result):
    try:
        with open(FilePath, 'w', encoding='utf-8') as file:
            file.write(Result)
    except FileNotFoundError:
        logger.error(f"Error: file {FilePath} not found")

@log_function(args=False, result=False)
def WriteResultToMarkdown(output_file, match_result, change_dict):

    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('### match\n')
            f.write('```\n')
            f.write(f'{match_result}\n')
            f.write('```\n')
            f.write('### patch\n')
            f.write('```\n')
            f.write(f"\n{change_dict['added']}\n")
            f.write('```\n')
        logger.info(f"Result successfully written to {output_file}")
    except Exception as e:
        logger.error(f"Error writing to Markdown file: {str(e)}")
        raise

@log_function(args=False, result=False)
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

@log_function(args=False, result=False)
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
            logger.warning(f"File {PathFile} is missing in branch {MainBranch}. Treating the old version as empty.")
            return {"NewLines": ReadLine(PathFile), "OldLines": []}
        else:
            logger.error(f"Error retrieving the old version of the file from the branch {MainBranch}: {str(e)}")
            raise

@log_function(args=False, result=False)
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

@log_function(args=False, result=False)
def DetectProgrammingLanguage(FileNameSourceCode):
    try:
        ext = os.path.splitext(FileNameSourceCode)[1].lower()
        Language = EXTENSIONS_FILE.get(ext, None)
        if not Language:
            raise ValueError ("Unknown language")
        return Language
    except ValueError as e:
        logger.error(f"Logic error: {e}")

@log_function(args=False, result=False)
def LoadLanguageModule(language: str):
    ModuleName = f'CompressionConstants.CompressionConstants_{language}'
    try:
        return importlib.import_module(ModuleName)
    except ModuleNotFoundError:
        raise ValueError(f'The module for the {language} language was not found. Check the {ModuleName}.py file')
    except Exception as e:
        raise RuntimeError(f'Error loading the module for {language}: {e}')

@log_function(args=False, result=False)
def ReceivingMatchOrPatchOrSourceCodeFromList(FilePath, TypeContent: Literal['Match', 'Patch', 'SourceCode']):
    if TypeContent == 'Match':
        return MatchLoadFromString(ReadFile(FilePath))
    elif TypeContent == 'Patch':
        return PatchLoadFromString(ReadFile(FilePath))
    else:
        return ReadFile(FilePath)

@log_function(args=False, result=False)
def ComparingListsLength(matches, patches):
    try:
        if len(matches) != len(patches):
            raise ValueError("The number of Match and Patch sections does not match")
        return True
    except ValueError as e:
        logger.error(f"Logic error: {e}")
        return False

@log_function(args=False, result=False)
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

@log_function(args=False, result=False)
def IsPassToN(Token):
    return re.fullmatch(r'\^[1-9]\d*\.\.', Token)

@log_function(args=False, result=False)
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

@log_function(args=False, result=False)
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

@log_function(args=False, result=False)
def GetTokenIndexBeforePosition(NodeStart: int, tokens: list[str]) -> int:
    pos = 0
    TokenIndex = 0
    while TokenIndex < len(tokens):
        token = tokens[TokenIndex]
        if pos + len(token) > NodeStart:
            break
        pos += len(token)
        TokenIndex += 1
    return TokenIndex

@log_function(args=False, result=False)
def TokenIndexToStringIndex(TargetTokenIndex, SourceCode, TokenList):
    RepetitionCount = 1
    for Token in TokenList[:TargetTokenIndex]:
        if Token == TokenList[TargetTokenIndex]:
            RepetitionCount += 1
    pos = -1
    for _ in range(RepetitionCount):
        pos = SourceCode.find(TokenList[TargetTokenIndex], pos + 1)
        if pos == -1:
            return -1

    return pos+1