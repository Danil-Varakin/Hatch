from ComprasionVersion import CompareFileVersions, AddInstruction
from Utilities import ReadFile

FilePath = r"C:\Users\droby\Hatch\test\PassedTests\unique13.cpp"
ComparisonResult = CompareFileVersions(FilePath, "development")
AddInstruction(FilePath, "development")
print(ReadFile(FilePath)[2034:2039])
print(ComparisonResult)
