from ComprasionVersion import CompareFileVersions

FilePath = r"C:\Users\droby\Hatch\test\PassedTests\unique10.cpp"
ComparisonResult = CompareFileVersions(FilePath, MainBranch="main")
print(ComparisonResult)
