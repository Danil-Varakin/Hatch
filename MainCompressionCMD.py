import argparse
import sys
from Logging import setup_logger, log_function
from CompressionVersion import  AddInstruction
from CompressionInput  import CreateMarkdownInstructions
from Utilities import DetectProgrammingLanguage
from gitUtils import ReadLastGitCommit
logger = setup_logger()

@log_function(args=False, result=False)
def ProcessGenerateMdMode(in_file, out_md, branch = None, language = None, agree_each_match = False):
    try:
        if not language:
            language = DetectProgrammingLanguage(in_file)
            logger.info(f"Автоопределён язык программирования: {language}")

        effective_branch = branch.strip() if branch and branch.strip() else "master"
        logger.info(f"Сравнение с веткой: {effective_branch}")

        PreviousSource = ReadLastGitCommit(in_file, effective_branch)
        if PreviousSource is None:
            raise ValueError(f"Не удалось найти файл {in_file} в ветке '{effective_branch}'")

        Match, Patch = AddInstruction( in_file, effective_branch, language, agree_each_match)
        if Match and Patch:
            success = CreateMarkdownInstructions(out_md, Match, Patch)

            if success:
                logger.info(f"Markdown-инструкции успешно созданы: {out_md}")
            else:
                raise RuntimeError("Ошибка в создании markdown-инструкции")
        else:
            raise RuntimeError("Ошибка в создании markdown-инструкции Match, Patch не созданы")
    except ValueError as e:
        logger.error(f"Ошибка в режиме генерации MD: {e}")

@log_function(args=False, result=False)
def main():
    parser = argparse.ArgumentParser(description="Генерация Hatch-инструкций (.md) по изменениям в файле относительно Git-коммита. "
                    "Сравнивает текущую версию файла с последним коммитом в указанной ветке "
                    "и создаёт человекочитаемые декларативные инструкции для применения этих изменений."
    )

    parser.add_argument('--in', type=str, dest='in_file', required=True,
                        help='Путь к исходному файлу (например, src/main.cpp)')
    parser.add_argument('--out', dest='out_file',type=str, required=True,
                        help='Путь к выходному .md файлу (например, changes.md)')
    parser.add_argument('--branch', type=str, default='master',
                        help='Ветка Git для сравнения (по умолчанию: master)')
    parser.add_argument('--language', type=str, default=None,
                        help='Язык программирования (например, cpp, python). Если не указан — определяется автоматически')
    parser.add_argument('-a', '--agreement', action='store_true',
                        help='включить режим согласования каждого отдельного match')

    args = parser.parse_args()

    if not args.in_file or not args.out_file:
        logger.error("Ошибка: обязательные аргументы --in и --out")
        parser.print_help()
        sys.exit(1)

    ProcessGenerateMdMode( in_file=args.in_file, out_md=args.out_file, branch=args.branch, language=args.language, agree_each_match = args.agreement)


if __name__ == "__main__":
    main()