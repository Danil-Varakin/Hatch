import argparse
import sys
from Utilities import ReceivingMatchOrPatchOrSourceCodeFromList, DetectProgrammingLanguage, ComparingListsLength, InsertOperatorStatus, WriteFile
from TokenizeCode import CheckAndRunTokenize
from Insert import RunInsert
from Logging import setup_logger, log_function
from CompressionVersion import RunAddInstruction
from CompressionInput import CreateMarkdownInstructions

logger = setup_logger()


# ============================================================================
# APPLY COMMAND - Apply patch instructions to source files
# ============================================================================

@log_function(args=False, result=False)
def ProcessApplyMode(match_path, in_path, out_path, patch_path=None, language=None):

    try:
        if language:
            language = language.lower()
        else:
            language = DetectProgrammingLanguage(in_path)

        matches = ReceivingMatchOrPatchOrSourceCodeFromList(match_path, 'Match')
        patches = ReceivingMatchOrPatchOrSourceCodeFromList(patch_path,
                                                            'Patch') if patch_path else ReceivingMatchOrPatchOrSourceCodeFromList(
            match_path, 'Patch')
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
                    CompletionStatus, _ = RunInsert(match, patch, SourceCode, out_path, out_path)
                elif IsOnlyOneInsert == 2:
                    raise ValueError("There is more than one insert in match")
                else:
                    raise ValueError("There is no insertion point in match")

                if CompletionStatus == 1:
                    logger.info(f"Match № {i} successfully inserted")
        else:
            raise ValueError("The number of match and patch does not match")

        if CompletionStatus:
            logger.info(f"Apply mode: {in_path} processed, result saved in {out_path}")
        else:
            logger.error(f"Insertion error in Apply mode")

    except ValueError as e:
        logger.error(f"Error in Apply mode: {e}")
    except Exception as e:
        logger.critical(f"Error in Apply mode: {e}")


# ============================================================================
# GENERATE COMMAND - Generate patch instructions from file differences
# ============================================================================

@log_function(args=False, result=False)
def ProcessGenerateMdMode(in_file, old_file_in, out_md, branch = None, language = None, agree_each_match = False):
    try:
        if not language:
            language = DetectProgrammingLanguage(in_file)
            logger.info(f"The programming language is automatically detected: {language}")
        if branch:
            effective_branch = branch.strip() if branch and branch.strip() else "master"
            logger.info(f"Comparison with a branch: {effective_branch}")
        else:
            effective_branch = branch


        Match, Patch =  RunAddInstruction(in_file, language, AgreeEachMatch= agree_each_match, MainBranch= effective_branch, OldFilePath= old_file_in)
        if Match and Patch:
            success = CreateMarkdownInstructions(out_md, Match, Patch)

            if success:
                logger.info(f"Markdown-instructions have been successfully created: {out_md}")
            else:
                raise RuntimeError("Error in creating markdown instructions")
        else:
            raise RuntimeError("Error in creating markdown-Match, Patch instructions were not created")
    except ValueError as e:
        logger.error(f"Error in MD generation mode: {e}")

@log_function(args=False, result=False)

# ============================================================================
# MAIN CLI INTERFACE
# ============================================================================

def main():

    parser = argparse.ArgumentParser(
        prog='hatch',
        description='Hatch - Smart Patches Tool. Simplifies Git patch management using declarative Hatch language.',
        epilog='Use "hatch <command> --help" for more information about a command.'
    )

    subparsers = parser.add_subparsers(
        title='Commands',
        description='Available Hatch commands',
        dest='command',
        help='Command to execute'
    )

    # ========================================================================
    # APPLY SUBCOMMAND
    # ========================================================================
    ApplyParser = subparsers.add_parser(
        'apply',
        help='Apply Hatch patch instructions to a source file',
        description='Apply declarative Hatch patch instructions from a markdown file to a source code file.'
    )

    ApplyParser.add_argument(
        '--match',
        type=str,
        required=True,
        help='Path to the match file (e.g., changes.md)'
    )

    ApplyParser.add_argument(
        '--patch',
        type=str,
        default=None,
        help='Path to separate patch file (optional, e.g., patch.md)'
    )

    ApplyParser.add_argument(
        '--in',
        type=str,
        dest='in_file',
        required=True,
        help='Path to the input source file (e.g., main.cpp)'
    )

    ApplyParser.add_argument(
        '--out',
        type=str,
        required=True,
        help='Path to the output file (e.g., main_patched.cpp)'
    )

    ApplyParser.add_argument(
        '--language',
        type=str,
        default=None,
        help='Programming language (e.g., cpp, python). Auto-detected if not specified.'
    )

    # ========================================================================
    # GENERATE SUBCOMMAND
    # ========================================================================
    GenerateParser = subparsers.add_parser(
        'generate',
        help='Generate Hatch patch instructions from file differences',
        description='Generate declarative Hatch instructions (.md) by comparing two versions of a file.'
    )

    GenerateParser.add_argument(
        '--in',
        type=str,
        dest='in_file',
        required=True,
        help='Path to the new version of the file (e.g., src/main.cpp)'
    )

    GenerateParser.add_argument(
        '--in-old',
        type=str,
        dest='old_in_file',
        required=True,
        help='Path to the old version of the file (e.g., src/main_old.cpp)'
    )

    GenerateParser.add_argument(
        '--out',
        dest='out_file',
        type=str,
        required=True,
        help='Path to the output markdown file (e.g., changes.md)'
    )

    GenerateParser.add_argument(
        '--branch',
        type=str,
        default='master',
        help='Git branch for comparison (default: master)'
    )

    GenerateParser.add_argument(
        '--language',
        type=str,
        default=None,
        help='Programming language (e.g., cpp, python). Auto-detected if not specified.'
    )

    GenerateParser.add_argument(
        '-a', '--agreement',
        action='store_true',
        help='Enable matching mode for each individual match'
    )

    # ========================================================================
    # PARSE AND EXECUTE
    # ========================================================================

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == 'apply':
        if not args.in_file or not args.out or not args.match:
            logger.error("Error: apply requires --match, --in and --out arguments")
            ApplyParser.print_help()
            sys.exit(1)

        ProcessApplyMode(
            match_path=args.match,
            in_path=args.in_file,
            out_path=args.out,
            patch_path=args.patch,
            language=args.language
        )

    elif args.command == 'generate':
        if not args.in_file or not args.out_file or not args.old_in_file:
            logger.error("Error: generate requires --in, --in-old and --out arguments")
            GenerateParser.print_help()
            sys.exit(1)

        ProcessGenerateMdMode(
            in_file=args.in_file,
            old_file_in=args.old_in_file,
            out_md=args.out_file,
            branch=args.branch,
            language=args.language,
            agree_each_match=args.agreement
        )


if __name__ == "__main__":
    main()