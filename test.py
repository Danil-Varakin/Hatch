from ComprasionVersion import CompareFileVersions, CompareFileContents
from tree_sitter_language_pack import get_language, get_parser
import os
from tree_sitter import Point
from Logging import setup_logger, log_function
import subprocess
from Utilities import ReadFile

logger = setup_logger(log_file="CodeComprasion/my_app.log")

# Инициализация tree-sitter для C++
CPP_LANGUAGE = get_language('cpp')
parser = get_parser('cpp')

@log_function
def ReadLastGitCommit(PathFile, MainBranch):
    try:
        RepositoryPath = os.path.relpath(PathFile, start=os.getcwd()).replace(os.sep, "/")
        OldContent = subprocess.check_output(
            ["git", "show", f"{MainBranch}:{RepositoryPath}"],
            text=True,
            encoding="utf-8")
        GitCommitFileContent = OldContent
        return GitCommitFileContent
    except subprocess.CalledProcessError as e:
        logger.error(f"Ошибка при получении старой версии файла из ветки {MainBranch}: {str(e)}")
        raise


@log_function
def FindEnclosingConstructs(file_path, changes):
    try:
        # Read the original code from the last commit
        code_commit = ReadLastGitCommit(file_path, MainBranch="development")
        # Read the current (new) version of the file
        code_current = ReadFile(file_path)
        results = {}
        for idx, change in enumerate(changes):
            line_number, action, abs_start, abs_end, added, deleted = change

            # Select code to analyze based on action
            if action == 'delete':
                code_analyze = code_commit  # Use old version for deletions
                change_start = abs_start
                change_end = abs_start + len(deleted)
            elif action == 'insert':
                code_analyze = code_current  # Use new version for insertions
                change_start = abs_start
                change_end = abs_start + len(added)
            elif action == 'replace':
                code_analyze = code_current  # Use new version for replacements (focus on added content)
                change_start = abs_start
                change_end = abs_start + len(added)
            else:
                raise ValueError(f"Unknown action: {action}")

            tree = parser.parse(code_analyze.encode('utf-8'))
            print(change_start, change_end, code_commit[change_start:change_end])
            if tree.root_node.type == 'ERROR':
                raise ValueError(f"Синтаксическая ошибка в файле {file_path}. AST содержит узел ERROR.")

            # Compute start_point and end_point
            prefix_start = code_analyze[:change_start]
            lines_start = prefix_start.splitlines()
            start_line = len(lines_start) - 1
            start_col = len(lines_start[-1]) if lines_start else 0

            prefix_end = code_analyze[:change_end]
            lines_end = prefix_end.splitlines()
            end_line = len(lines_end) - 1
            end_col = len(lines_end[-1]) if lines_end else 0

            # Adjust for leading whitespace in change
            current_pos = change_start
            while current_pos < change_end and code_analyze[current_pos].isspace():
                current_pos += 1
            if current_pos > change_start:
                prefix_start = code_analyze[:current_pos]
                lines_start = prefix_start.splitlines()
                start_line = len(lines_start) - 1
                start_col = len(lines_start[-1]) if lines_start else 0

            # Adjust for trailing whitespace in change
            current_pos_end = change_end - 1
            while current_pos_end >= change_start and code_analyze[current_pos_end].isspace():
                current_pos_end -= 1
            current_pos_end += 1
            if current_pos_end < change_end:
                prefix_end = code_analyze[:current_pos_end]
                lines_end = prefix_end.splitlines()
                end_line = len(lines_end) - 1
                end_col = len(lines_end[-1]) if lines_end else 0

            start_point = Point(row=start_line, column=start_col)
            end_point = Point(row=end_line, column=end_col)

            # Function to check if node contains the entire range
            def contains_range(Node, s_pt, e_pt):
                ns_pt = Node.start_point
                ne_pt = Node.end_point
                start_cond = (ns_pt.row < s_pt.row or (ns_pt.row == s_pt.row and ns_pt.column <= s_pt.column))
                end_cond = (ne_pt.row > e_pt.row or (ne_pt.row == e_pt.row and ne_pt.column >= e_pt.column))
                return start_cond and end_cond

            # Find the closest enclosing node and path
            node = tree.root_node
            path = []
            enclosing_node = None
            while node:
                path.append(node.type)
                enclosing_node = node
                next_node = None
                for child in node.children:
                    if contains_range(child, start_point, end_point):
                        next_node = child
                        break
                node = next_node

            # Find nearest function (innermost containing the range)
            nearest_function = None
            def find_nearest_function(Node):
                nonlocal nearest_function
                for Child in Node.children:
                    find_nearest_function(Child)
                if nearest_function is None and Node.type == 'function_definition' and contains_range(Node, start_point, end_point):
                    nearest_function = {
                        'type': Node.type,
                        'start_point': Node.start_point,
                        'end_point': Node.end_point
                    }

            find_nearest_function(tree.root_node)

            # Find nearest control flow (innermost containing the range)
            control_flow_types = {'if_statement', 'while_statement', 'for_statement', 'elif_clause', 'else_clause', 'try_statement', 'except_clause'}
            nearest_control_flow = None
            def find_nearest_control_flow(Node):
                nonlocal nearest_control_flow
                for Child in Node.children:
                    find_nearest_control_flow(Child)
                if nearest_control_flow is None and Node.type in control_flow_types and contains_range(Node, start_point, end_point):
                    nearest_control_flow = {
                        'type': Node.type,
                        'start_point': Node.start_point,
                        'end_point': Node.end_point
                    }

            find_nearest_control_flow(tree.root_node)

            # Find nearest siblings
            previous_sibling = None
            next_sibling = None
            if enclosing_node and enclosing_node.parent:
                siblings = enclosing_node.parent.children
                enclosing_index = siblings.index(enclosing_node)
                if enclosing_index > 0:
                    prev_node = siblings[enclosing_index - 1]
                    previous_sibling = {
                        'type': prev_node.type,
                        'start_point': prev_node.start_point,
                        'end_point': prev_node.end_point
                    }
                if enclosing_index < len(siblings) - 1:
                    next_node = siblings[enclosing_index + 1]
                    next_sibling = {
                        'type': next_node.type,
                        'start_point': next_node.start_point,
                        'end_point': next_node.end_point
                    }

            # Form result
            results[idx] = {
                'change': change,
                'enclosing_path': path,
                'details': {
                    'closest_enclosing_node': {
                        'type': enclosing_node.type if enclosing_node else None,
                        'start_point': enclosing_node.start_point if enclosing_node else None,
                        'end_point': enclosing_node.end_point if enclosing_node else None
                    } if enclosing_node else None,
                    'nearest_function': nearest_function,
                    'nearest_control_flow': nearest_control_flow,
                    'previous_sibling': previous_sibling,
                    'next_sibling': next_sibling
                }
            }

        if not results:
            raise ValueError("Нет enclosing конструкций для изменений")

        return results

    except Exception as e:
        logger.error(f"logic error: {str(e)}")
        raise
# Основной код
FilePath = r"C:\Users\droby\Hatch\test\PassedTests\unique13.cpp"
ComparisonResult = CompareFileVersions(FilePath, MainBranch="development")
print("Changes:", ComparisonResult)

# Проверка, что файл существует
if os.path.exists(FilePath):
    EnclosingResult = FindEnclosingConstructs(FilePath, ComparisonResult)
    print("Enclosing Constructs:", EnclosingResult)
else:
    print(f"Error: File {FilePath} does not exist.")