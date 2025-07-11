import pytest
from pathlib import Path
import glob
from ParsingCodeAndInstruction import ReceivingMatchOrPatchOrSourceCodeFromList
from TokenizeCode import CheckAndRunTokenize
from SearchCode import SearchInsertIndexInSourceCode, SearchInsertIndexInTokenList

TEST_DIR = Path("test")
PASSED_DIR = TEST_DIR / "PassedTests"
FAILED_DIR = TEST_DIR / "FailedTests"
ADDITIONAL_TEST_DIR = TEST_DIR / "PassedTests"

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
    "unique5": ['Prev', 3, 'r'],
    "unique6": ['Prev', 7, '}'],
    "unique7": ['Next', 7, '}'],
    "unique8": ['Next', 2, 'r'],
    "unique9": 0,
    "unique10": ['Next', 1, '}'],
    "unique11": ['Next', 52, '}'],
    "unique12": ['Prev', 20, ')'],
    "unique13": ['Next', 31, '}'],
    "unique14": ['Next', 3, '}'],
    "unique15": ['Next', 19, '}'],
    "unique16": ['Next', 198, 'k'],
    "unique17": ['Prev', 295, 'f'],
    "unique18": ['Next', 1, '#']
}

EXPECTED_ADDITIONAL_RESULTS = {
    "unique1": 0,
    "unique2": 0,
    "unique3": {'Prev': [10, 0]},
    "unique5":  {'Prev': [41, 9]},
    "unique6": {'Prev': [47, 0]},
    "unique7": {'Next': [47, 0]},
    "unique8": {'Next': [41, 2]},
    "unique9": 0,
    "unique10": {'Next': [17, 0]},
    "unique11": {'Next': [696, 0]},
    "unique12": {'Prev': [82, 0]},
    "unique13": {'Next': [355, 0]},
    "unique14": {'Next': [23, 0]},
    "unique15": {'Next': [317, 0]},
    "unique16": {'Next': [109, 274]},
    "unique17": {'Prev': [209, 5]},
    "unique18": {'Next': [0, 0]},
}

PassedTestFiles = GetFilePairs(PASSED_DIR)
FailedTestFiles = GetFilePairs(FAILED_DIR)
AdditionalTestFiles = GetFilePairs(ADDITIONAL_TEST_DIR)

@pytest.mark.parametrize("TestPath, SourcePath", PassedTestFiles)
def testPassedCases(TestPath, SourcePath):
    language = "cpp"
    match = ReceivingMatchOrPatchOrSourceCodeFromList(TestPath, 'Match')
    patch = ReceivingMatchOrPatchOrSourceCodeFromList(TestPath, 'Patch')
    SourceCode = ReceivingMatchOrPatchOrSourceCodeFromList(SourcePath, 'SourceCode')

    match = CheckAndRunTokenize(match, language)
    SourceCode = CheckAndRunTokenize(SourceCode, language)

    result = SearchInsertIndexInSourceCode(match, SourceCode)

    BaseName = Path(TestPath).stem
    assert BaseName in EXPECTED_PASSED_RESULTS, f"Test failed for {TestPath}: No expected result defined in EXPECTED_PASSED_RESULTS"
    ExpectedResult = EXPECTED_PASSED_RESULTS[BaseName]

    assert isinstance(result, (list, int)), f"Test failed for {TestPath}: Expected a list or int, got {type(result)}"
    if isinstance(result, list):
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

    result = SearchInsertIndexInSourceCode(match, SourceCode)

    assert result == 0, f"Test failed for {TestPath}: Expected 0, got {result}"


@pytest.mark.parametrize("TestPath,SourcePath", PassedTestFiles)
def testAdditionalCases(TestPath, SourcePath):
    language = "cpp"
    try:
        match = ReceivingMatchOrPatchOrSourceCodeFromList(TestPath, 'Match')
        patch = ReceivingMatchOrPatchOrSourceCodeFromList(TestPath, 'Patch')
        SourceCode = ReceivingMatchOrPatchOrSourceCodeFromList(SourcePath, 'SourceCode')
    except Exception as e:
        pytest.fail(f"Test failed for {TestPath}: Error retrieving data - {str(e)}")

    try:
        match = CheckAndRunTokenize(match, language)
        SourceCode = CheckAndRunTokenize(SourceCode, language)
    except Exception as e:
        pytest.fail(f"Test failed for {TestPath}: Error tokenizing data - {str(e)}")

    try:
        result = SearchInsertIndexInTokenList(match, SourceCode)
    except Exception as e:
        pytest.fail(f"Test failed for {TestPath}: Error in SearchInsertIndexInTokenList - {str(e)}")
    BaseName = Path(TestPath).stem

    if BaseName not in EXPECTED_ADDITIONAL_RESULTS:
        pytest.fail(f"Test failed for {TestPath}: No expected result defined in EXPECTED_ADDITIONAL_RESULTS")

    ExpectedResult = EXPECTED_ADDITIONAL_RESULTS[BaseName]
    if not isinstance(result, (list, int, dict)):
        pytest.fail(f"Test failed for {TestPath}: Expected a list, int, or dict, got {type(result)}")

    if isinstance(result, list) and len(result) != 3:
        pytest.fail(f"Test failed for {TestPath}: Expected list of length 3, got {len(result)}")

    if result != ExpectedResult:
        pytest.fail(f"Test failed for {TestPath}: Expected {ExpectedResult}, got {result}")