from ComprasionVersion import CompareFileVersions, CreateMarkdownInstructions
from tree_sitter_language_pack import get_language, get_parser
from Utilities import ReadLastGitCommit


CPP_LANGUAGE = get_language('cpp')
parser = get_parser('cpp')
FilePath = r"test\PassedTests\unique13.cpp"
OutPath = "unique13res.md"
SourceCode = ReadLastGitCommit(FilePath, "development")
print(SourceCode[5374:5608])
ComparisonResult = CompareFileVersions(FilePath, SourceCode)
print("Change:", ComparisonResult)

CreateMarkdownInstructions(OutPath, FilePath,"development", parser, "cpp")