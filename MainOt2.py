from CompressionVersion import   RunAddInstruction
from CompressionInput  import CreateMarkdownInstructions
FilePath = r"test/PassedTests/unique15.cpp"
OutPath = "unique13res.md"
OldPath = r"test/PassedTests/unique14.cpp"
Match, Patch =  RunAddInstruction(FilePath, "cpp", OldFilePath=OldPath)
CreateMarkdownInstructions(OutPath, Match, Patch)
