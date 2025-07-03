from ParsingCodeAndInstruction import ReceivingMatchOrPatchOrSourceCodeFromList
from TokenizeCode import  CheckAndRunTokenize
from SearchCode import SearchInsertIndexInSourseCode
import pytest
from pathlib import Path
import glob


TEST_DIR = Path("test")
PASSED_DIR = TEST_DIR / "PassedTests"
FAILED_DIR = TEST_DIR / "FailedTests"


def GetFilePairs(directory):
    MdFiles = glob.glob(str(directory / "*.md"))
    Pairs = []
    for MdFile in MdFiles:
        BaseName = Path(MdFile).stem
        CppFile = directory / f"{BaseName}.cpp"
        if CppFile.exists():
            Pairs.append((MdFile, str(CppFile)))
    return Pairs



EXPECTED_PASSED_RESULTS = {
    "unique1": 0,
    "unique2": 0,
    "unique3": ['Prev', 2, ')'],
    "unique5": ['Prev', 1, 'register'],
    "unique6": ['Prev', 7, '}'],
    "unique7": ['Next', 7, '}'],
    "unique8": ['Next', 1, 'register'],
    "unique9": 0,
    "unique10": ['Next', 1, '}'],
    "unique11": ['Next', 52, '}'],
    "unique12": ['Prev', 18, ')'],
    "unique13": ['Next', 31, '}'],
    "unique14": ['Next', 3, '}'],
    "unique15": ['Next', 19, '}'],
    "unique16": ['Next', 1, 'kDesktopPWAsTabStripSettings'],
    "unique17": ['Prev', 17, 'endif'],


}

PassedTestFiles = GetFilePairs(PASSED_DIR)
FailedTestFiles = GetFilePairs(FAILED_DIR)


@pytest.mark.parametrize("TestPath, SourcePath", PassedTestFiles)
def testPassedCases(TestPath, SourcePath):
    language = "cpp"

    match = ReceivingMatchOrPatchOrSourceCodeFromList(TestPath, 'Match')
    patch = ReceivingMatchOrPatchOrSourceCodeFromList(TestPath, 'Patch')
    SourceCode = ReceivingMatchOrPatchOrSourceCodeFromList(SourcePath, 'SourceCode')

    match = CheckAndRunTokenize(match, language)
    SourceCode = CheckAndRunTokenize(SourceCode, language)

    result = SearchInsertIndexInSourseCode(match, SourceCode)

    BaseName = Path(TestPath).stem

    assert BaseName in EXPECTED_PASSED_RESULTS, f"Test failed for {TestPath}: No expected result defined in EXPECTED_PASSED_RESULTS"

    ExpectedResult = EXPECTED_PASSED_RESULTS[BaseName]

    assert isinstance(result, list), f"Test failed for {TestPath}: Expected a list, got {type(result)}"
    assert len(result) == 3, f"Test failed for {TestPath}: Expected list of length 3, got {len(result)}"
    assert result == ExpectedResult, f"Test failed for {TestPath}: Expected {ExpectedResult}, got {result}"


@pytest.mark.parametrize("TestPath, SourcePath", FailedTestFiles)
def testFailedCases(TestPath, SourcePath):
    language = "cpp"

    match = ReceivingMatchOrPatchOrSourceCodeFromList(TestPath, 'Match')
    patch = ReceivingMatchOrPatchOrSourceCodeFromList(TestPath, 'Patch')
    SourceCode = ReceivingMatchOrPatchOrSourceCodeFromList(SourcePath, 'SourceCode')

    match = CheckAndRunTokenize(match, language)
    SourceCode = CheckAndRunTokenize(SourceCode, language)

    result = SearchInsertIndexInSourseCode(match, SourceCode)

    assert result == 0, f"Test failed for {TestPath}: Expected 0, got {result}"