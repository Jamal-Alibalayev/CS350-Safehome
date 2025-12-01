"""
This is the script to extract class methods and standalone functions from Python files
in the 'safehome' directory and format them for further processing.

This script is not a part of the main application and is intended for development use only.
"""

import ast
import os


def find_python_files(directory):
    """Recursively finds all Python files in the given directory."""
    python_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                python_files.append(os.path.join(root, file))
    return python_files


def extract_functions_from_file(file_path):
    """
    Extracts class methods and standalone functions from a Python file
    and returns them in the specified format.
    """
    functions_to_check = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read(), filename=file_path)

        # Add parent links to AST nodes for easier traversal
        for node in ast.walk(tree):
            for child in ast.iter_child_nodes(node):
                child.parent = node

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                function_name = node.name
                if not function_name.startswith("__"):  # Ignore dunder methods
                    current_class = None
                    # Traverse up the parent chain to find if the function is inside a class
                    parent_node = getattr(node, "parent", None)
                    while parent_node:
                        if isinstance(parent_node, ast.ClassDef):
                            current_class = parent_node.name
                            break
                        parent_node = getattr(parent_node, "parent", None)

                    if current_class:
                        functions_to_check.append(
                            f'class: "{current_class}", function: "{function_name}"'
                        )
                    else:
                        # It's a standalone function (not nested in a class)
                        functions_to_check.append(
                            f'class: "None", function: "{function_name}"'
                        )
    except Exception as e:
        # In a real scenario, you might want to log this error.
        # print(f"Error processing {file_path}: {e}")
        pass
    return functions_to_check


# Main script logic
project_root = os.getcwd()
safehome_dir = os.path.join(project_root, "safehome")
all_python_files = find_python_files(safehome_dir)

all_functions_to_check = []
for file_path in all_python_files:
    all_functions_to_check.extend(extract_functions_from_file(file_path))

for res in all_functions_to_check:
    print(res)
