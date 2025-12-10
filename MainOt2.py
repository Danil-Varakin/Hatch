from ComprasionVersion import CreateMarkdownInstructions
from Utilities import  ReadFile
from getChange import  GetChange
from gitUtils import ReadLastGitCommit, GetDiffOutput
FilePath = r"test/PassedTests/unique13.cpp"
OutPath = "unique13res.md"
SourceCode = ReadLastGitCommit(FilePath, "origin/development")
S2 = ReadFile(FilePath)
print(SourceCode[3326:3377])
CreateMarkdownInstructions(OutPath, FilePath,"origin/development", "cpp")
