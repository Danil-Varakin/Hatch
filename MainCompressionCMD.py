import argparse
import sys
from Logging import setup_logger, log_function
from CompressionVersion import  RunAddInstruction
from CompressionInput  import CreateMarkdownInstructions
from Utilities import DetectProgrammingLanguage
from gitUtils import ReadLastGitCommit
logger = setup_logger()

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
def main():
    parser = argparse.ArgumentParser(description="Generation of Hatch instructions (.md) for changes in a file relative to a Git commit. "
"Compares the current version of the file with the last commit in the specified branch "
"and creates human-readable declarative instructions for applying these changes."
    )

    parser.add_argument('--in', type=str, dest='in_file', required=True,
                        help='The path to the source file (for example, src/main.cpp )')
    parser.add_argument('--in_old', type=str, dest='old_in_file', required=True,
                        help='The path to the original old version of the source file (for example, src/main.cpp )')
    parser.add_argument('--out', dest='out_file',type=str, required=True,
                        help='The path to the output .md file (for example, changes.md )')
    parser.add_argument('--branch', type=str, default='master',
                        help='Git branch for comparison (default: master)')
    parser.add_argument('--language', type=str, default=None,
                        help='Programming language (for example, cpp, python). If not specified, it is detected automatically.')
    parser.add_argument('-a', '--agreement', action='store_true',
                        help='enable the matching mode for each individual match')

    args = parser.parse_args()

    if not args.in_file or not args.out_file:
        logger.error("Error: required arguments --in and --out")
        parser.print_help()
        sys.exit(1)

    ProcessGenerateMdMode( in_file=args.in_file, old_file_in = args.old_in_file, out_md=args.out_file, branch=args.branch, language=args.language, agree_each_match = args.agreement)


if __name__ == "__main__":
    main()