import argparse
import sys
from Utilities import ReceivingMatchOrPatchOrSourceCodeFromList, DetectProgrammingLanguage, ComparingListsLength
from TokenizeCode import CheckAndRunTokenize
from Insert import RunInsert

def process_match_mode(match_path, in_path, out_path, patch_path=None):
    try:
        language = DetectProgrammingLanguage(in_path)
        matches = ReceivingMatchOrPatchOrSourceCodeFromList(match_path, 'Match')
        patches = ReceivingMatchOrPatchOrSourceCodeFromList(patch_path, 'Patch') if patch_path else ReceivingMatchOrPatchOrSourceCodeFromList(match_path, 'Patch')
        if ComparingListsLength(matches, patches):
            for i, (match, patch) in enumerate(zip(matches, patches)):
                SourceCode = ReceivingMatchOrPatchOrSourceCodeFromList(in_path, 'SourceCode')
                match = CheckAndRunTokenize(match, language)
                SourceCode = CheckAndRunTokenize(SourceCode, language)
                RunInsert(match, patch, SourceCode, in_path, out_path)
                print(f"Match  № {i} успешно вставлен")
        else:
            raise ValueError("Количество match и patch не совпадает")
        return f"Режим match: обработан {in_path}, результат Insert сохранен в {out_path}"
    except (Exception, ValueError) as e:
        return f"Ошибка в режиме match: {e}"

def main():
    parser = argparse.ArgumentParser(description="Программа для анализа кода с match и вставки патча")

    parser.add_argument('--match', type=str, help='Путь к файлу match (например, file.md)')
    parser.add_argument('--patch', type=str, help='Путь к файлу patch, не обязателен (например, patch.md)', default=None)
    parser.add_argument('--in', type=str, dest='in_file', help='Путь к входному файлу (например, 1.cpp)')
    parser.add_argument('--out', type=str, help='Путь к выходному файлу (например, 1_r.txt)')

    args = parser.parse_args()

    if args.match and args.in_file and args.out:
        result = process_match_mode(args.match, args.in_file, args.out, args.patch)
        print(result)
    else:
        print("Ошибка: некорректные аргументы. Требуются --match, --in и --out")
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()