from CompressionVersion import  AddInstruction
from CompressionInput  import CreateMarkdownInstructions
from Utilities import  ReadFile
from gitUtils import ReadLastGitCommit
FilePath = r"test/PassedTests/unique16.cpp"
OutPath = "unique13res.md"
SourceCode = ReadLastGitCommit(FilePath, "origin/development")
print(repr(SourceCode[4043:4080]))
S2 = ReadFile(FilePath)
Match, Patch = AddInstruction( FilePath,"origin/development", "cpp")
CreateMarkdownInstructions(OutPath, Match, Patch)
