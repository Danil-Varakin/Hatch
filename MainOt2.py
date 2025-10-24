from ComprasionVersion import CompareFileVersions, AddInstruction, CreateMarkdownInstructions
from tree_sitter_language_pack import get_language, get_parser
from Utilities import ReadFile, ReadLastGitCommit

CPP_LANGUAGE = get_language('cpp')
parser = get_parser('cpp')
FilePath = r"test\PassedTests\unique13.cpp"
fff = ReadFile(FilePath)
SourceCode = ReadLastGitCommit(FilePath, "development")
ComparisonResult = CompareFileVersions(FilePath, SourceCode)
Match = AddInstruction(FilePath, "development", parser, "cpp")
print("Change:", ComparisonResult)
print("Result:", Match)

# Вызов функции для создания Markdown файла
CreateMarkdownInstructions(FilePath, Match, ComparisonResult)