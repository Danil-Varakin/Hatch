import subprocess
import sys
import os
import tempfile
from Logging import setup_logger, log_function
from Utilities import ReceivingMatchOrPatchOrSourceCodeFromList

logger = setup_logger()

@log_function(args=False, result=False)
def HandleMatchConflict(match: list[str], patch: list[str]):
    print("Fix the  matches or abort the program execution.")

    while True:
        answer = input("Do you want to change the match [Y/N]: ").strip().upper()

        if answer == 'Y':

            Match, Patch = CallEditor(match, patch)

            if not Match:
                print("Warning: No match entries found in edited file.")
                retry = input("Do you want to edit again? [Y/N]: ").strip().upper()
                if retry == 'Y':
                    continue
                else:
                    print("Aborting program execution...")
                    sys.exit(0)

            if len(Match) != len(Patch):
                print(
                    f"Error: Number of match entries ({len(Match)}) doesn't equal number of patch entries ({len(Patch)})")
                retry = input("Do you want to edit again? [Y/N]: ").strip().upper()
                if retry == 'Y':
                    continue
                else:
                    print("Aborting program execution...")
                    sys.exit(0)

            return Match, Patch


        elif answer == 'N':
            print("Aborting program execution...")
            sys.exit(0)

        else:
            print("Invalid input. Please enter Y or N.")

@log_function(args=False, result=False)
def CallEditor(match: list[str], patch: list[str]):
    temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8')
    temp_filename = temp_file.name
    try:
        success = CreateMarkdownInstructions(temp_filename, match, patch)
        if not success:
            raise ValueError("Error creating temporary file. Aborting...")

        print(f"Opening editor")

        if sys.platform == 'darwin':
            editor = os.environ.get('EDITOR')
            if editor:
                subprocess.run([editor, temp_filename])
            else:
                subprocess.run(['open', '-t', temp_filename])
                input("Press Enter after you've finished editing and closed the editor...")
        elif os.name == 'nt':
            subprocess.run(['notepad.exe', temp_filename])
        else:
            editor = os.environ.get('EDITOR', 'nano')
            subprocess.run([editor, temp_filename])

        print("Editor closed. Reading changes...")

        if not os.path.exists(temp_filename):
            raise ValueError("Error: Temporary file was deleted.")

        Match = ReceivingMatchOrPatchOrSourceCodeFromList(temp_filename, "Match")
        Patch = ReceivingMatchOrPatchOrSourceCodeFromList(temp_filename, "Patch")
        return Match, Patch

    except Exception as e:
        logger.error(f"{str(e)}")

    finally:
        if os.path.exists(temp_filename):
            os.remove(temp_filename)

@log_function(args=False, result=False)
def AgreeEachMatchCommand():
    answer = input("Are you coordinating this match? [Y/N]: ").strip().upper()
    if answer == 'Y':
        return False
    elif answer == 'N':
        return True
    return None


@log_function(args=False, result=False)
def CreateMarkdownInstructions(OutPath: str, Match: list, Patch: list) -> bool:
    try:
        with open(OutPath, 'w', encoding='utf-8') as MdFile:
            if not Match:
                raise ValueError("The list of instructions is empty")

            for idx  in range(len(Match)):
                MdFile.write(f"### match\n")
                MdFile.write(f"```\n{Match[idx]}\n```\n")

                MdFile.write(f"### patch\n")

                MdFile.write(f"```\n{Patch[idx]}\n```\n\n")

        logger.info(f"Markdown file has been created successfully: {OutPath}")
        return True

    except Exception as e:
        logger.error(f"Error when creating a Markdown file: {str(e)}")
        return False
