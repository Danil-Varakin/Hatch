import subprocess
import sys
import re
import os
import tempfile
from Logging import setup_logger, log_function


logger = setup_logger()

def handle_match_conflict(match: list[str], patch: list[str]) -> tuple[list[str], list[str]]:


    print("The match already exists, fix the previous matches or abort the program execution.")

    while True:
        answer = input("Do you want to change the previous match [Y/N]: ").strip().upper()

        if answer == 'Y':
            with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as temp_file:
                temp_filename = temp_file.name

            try:
                success = CreateMarkdownInstructions(temp_filename, match, patch)

                if not success:
                    print("Error creating temporary file. Aborting...")
                    sys.exit(1)

                if os.name == 'nt':
                    subprocess.call(['notepad', temp_filename])
                else:
                    editor = os.environ.get('EDITOR', 'nano')
                    subprocess.call([editor, temp_filename])

                with open(temp_filename, 'r', encoding='utf-8') as f:
                    edited_content = f.read()

                new_match, new_patch = parse_markdown_instructions(edited_content)

                if not new_match:
                    print("Warning: No match entries found in edited file.")
                    continue

                if len(new_match) != len(new_patch):
                    print(
                        f"Error: Number of match entries ({len(new_match)}) doesn't equal number of patch entries ({len(new_patch)})")
                    retry = input("Do you want to edit again? [Y/N]: ").strip().upper()
                    if retry == 'Y':
                        continue
                    else:
                        print("Aborting program execution...")
                        sys.exit(0)

                return new_match, new_patch

            finally:
                if os.path.exists(temp_filename):
                    os.remove(temp_filename)

        elif answer == 'N':
            print("Aborting program execution...")
            sys.exit(0)

        else:
            print("Invalid input. Please enter Y or N.")


def parse_markdown_instructions(content: str) -> tuple[list[str], list[str]]:
    match_list = []
    patch_list = []

    sections = re.split(r'###\s+match\s*\n', content)

    for section in sections[1:]:  # Пропускаем первый пустой элемент
        match_pattern = r'```\s*\n(.*?)\n```'
        match_blocks = re.findall(match_pattern, section, re.DOTALL)

        if len(match_blocks) < 1:
            continue

        match_content = match_blocks[0].strip()

        patch_search = re.search(r'###\s+patch\s*\n```\s*\n(.*?)\n```', section, re.DOTALL)

        if patch_search:
            patch_content = patch_search.group(1).strip()
        else:
            patch_content = ""

        match_list.append(match_content)
        patch_list.append(patch_content)

    return match_list, patch_list

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
