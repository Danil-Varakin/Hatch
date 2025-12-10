import argparse
import sys
from Logging import setup_logger, log_function
from ComprasionVersion import CreateMarkdownInstructions, ParseDiffToChange
from tree_sitter_language_pack import  get_parser
from Utilities import DetectProgrammingLanguage
from gitUtils import ReadLastGitCommit
logger = setup_logger()

@log_function(args=False, result=False)
def ProcessGenerateMdMode(in_file, out_md, branch = None, language = None):
    try:
        if not language:
            language = DetectProgrammingLanguage(in_file)
            logger.info(f"Автоопределён язык программирования: {language}")

        parser = get_parser(language)

        effective_branch = branch.strip() if branch and branch.strip() else "master"
        logger.info(f"Сравнение с веткой: {effective_branch}")

        PreviousSource = ReadLastGitCommit(in_file, effective_branch)
        if PreviousSource is None:
            raise ValueError(f"Не удалось найти файл {in_file} в ветке '{effective_branch}'")

        success = CreateMarkdownInstructions(out_md, in_file, effective_branch, parser, language)

        if success:
            logger.info(f"Markdown-инструкции успешно созданы: {out_md}")
        else:
            raise RuntimeError("Ошибка в создании markdown-инструкции")

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
    parser.add_argument('--out', type=str, required=True,
                        help='Путь к выходному .md файлу (например, changes.md)')
    parser.add_argument('--branch', type=str, default='master',
                        help='Ветка Git для сравнения (по умолчанию: master)')
    parser.add_argument('--language', type=str, default=None,
                        help='Язык программирования (например, cpp, python). Если не указан — определяется автоматически')

    args = parser.parse_args()

    if not args.in_file or not args.out:
        logger.error("Ошибка: обязательные аргументы --in и --out")
        parser.print_help()
        sys.exit(1)

    ProcessGenerateMdMode(
        in_file=args.in_file,
        out_md=args.out,
        branch=args.branch,
        language=args.language
    )


if __name__ == "__main__":
    main()