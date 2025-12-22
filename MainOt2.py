from ComprasionVersion import  AddInstruction
from ComprasionInput  import CreateMarkdownInstructions
from Utilities import  ReadFile
from gitUtils import ReadLastGitCommit
FilePath = r"test/PassedTests/unique16.cpp"
OutPath = "unique13res.md"
SourceCode = ReadLastGitCommit(FilePath, "origin/development")
S2 = ReadFile(FilePath)
Match, Patch = AddInstruction( FilePath,"origin/development", "gn")
CreateMarkdownInstructions(OutPath, Match, Patch)
