from ComprasionVersion import CompareFileVersions

FilePath = r"test/PassedTests/unique13.cpp"
ComparisonResult = CompareFileVersions(FilePath, MainBranch="development")
print(ComparisonResult)
