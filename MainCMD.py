import argparse
import sys
from Utilities import ReceivingMatchOrPatchOrSourceCodeFromList, DetectProgrammingLanguage, ComparingListsLength, InsertOperatorStatus, WriteFile
from TokenizeCode import CheckAndRunTokenize
from Insert import RunInsert

def process_match_mode(match_path, in_path, out_path, patch_path=None, language = None):
    try:
        if language:
            language = language.lower()
        else:
            language = DetectProgrammingLanguage(in_path)
        matches = ReceivingMatchOrPatchOrSourceCodeFromList(match_path, 'Match')
        patches = ReceivingMatchOrPatchOrSourceCodeFromList(patch_path, 'Patch') if patch_path else ReceivingMatchOrPatchOrSourceCodeFromList(match_path, 'Patch')
        ResultCode = ReceivingMatchOrPatchOrSourceCodeFromList(in_path, "SourceCode")
        WriteFile(out_path, ResultCode)
        CompletionStatus = 0
        if ComparingListsLength(matches, patches):
            for i, (match, patch) in enumerate(zip(matches, patches)):
                SourceCode = ReceivingMatchOrPatchOrSourceCodeFromList(out_path, "SourceCode")
                SourceCode = CheckAndRunTokenize(SourceCode, language)
                if not SourceCode:
                    break
                match = CheckAndRunTokenize(match, language)
                IsOnlyOneInsert = InsertOperatorStatus(match)
                if IsOnlyOneInsert == 1:
                    CompletionStatus = RunInsert(match, patch, SourceCode, out_path, out_path)
                elif IsOnlyOneInsert == 2:
                    raise ValueError("There is more than one insert in match")
                else:
                    raise ValueError("There is no insertion point in match")
                if CompletionStatus == 1:
                    print(f"Match  № {i} successfully inserted")
        else:
            raise ValueError("The number of match and patch does not match")
        if CompletionStatus:
            return f"Match mode: {in_path} processed, result Insert saved in {out_path}"
        else:
            return f"Insertion error in Match mode "
    except (Exception, ValueError) as e:
        return f"Error in Match mode: {e}"

def main():
    parser = argparse.ArgumentParser(description="Hatch is designed to simplify the process of applying Git patches. Traditional patches are complex to analyze and apply, especially in large projects. The Hatch logical language allows changes to be described declaratively, improving readability and automating the process.Hatch is designed to simplify the process of applying Git patches. Traditional patches are complex to analyze and apply, especially in large projects. The Hatch logical language allows changes to be described declaratively, improving readability and automating the process.")

    parser.add_argument('--match', type=str, help='Path to the match file (e.g., file.md)')
    parser.add_argument('--patch', type=str, help='Path to the patch file, optional (e.g., patch.md)', default=None)
    parser.add_argument('--in', type=str, dest='in_file', help='Path to the input file (e.g., 1.cpp)')
    parser.add_argument('--out', type=str, help='Path to the output file (e.g., 1_r.txt)')
    parser.add_argument('--language', type=str, help='Programming language (e.g., cpp)')

    args = parser.parse_args()

    if args.match and args.in_file and args.out:
        result = process_match_mode(args.match, args.in_file, args.out, args.patch, args.language)
        print(result)
    else:
        print("Ошибка: некорректные аргументы. Требуются --match, --in и --out")
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()