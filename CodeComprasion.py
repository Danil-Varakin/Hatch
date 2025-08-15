from Utilities import GetFileOldAndNewVersion
from TokenizeCode import CheckAndRunTokenize
from Utilities import  DetectProgrammingLanguage

def ComparisonFile(FilePath):
    Language = DetectProgrammingLanguage(FilePath)
    FileDictionary = GetFileOldAndNewVersion(FilePath)
    OldVersionFile = FileDictionary["OldVersion"]
    CurrentVersionFile = FileDictionary["CurrentVersion"]
    OldVersionTokenList = CheckAndRunTokenize(OldVersionFile, Language)
    NewVersionTokenList = CheckAndRunTokenize(CurrentVersionFile, Language)
    CurrentOldVersionTokenIndex = 0
    for OldVersionTokenIndex in range(CurrentOldVersionTokenIndex,OldVersionTokenList):
        if OldVersionTokenList[OldVersionTokenIndex] != NewVersionTokenList[OldVersionTokenIndex]:
            CurrentNewVersionToken = NewVersionTokenList[OldVersionTokenIndex]
            for NewVersionTokenIndex in range(CurrentNewVersionToken, NewVersionTokenList):
                if OldVersionTokenList[OldVersionTokenIndex] == NewVersionTokenList[NewVersionTokenIndex]:
                    OldVersionTokenIndex = NewVersionTokenIndex
                    break

