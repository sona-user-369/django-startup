import ast
import os
import re


def change_variable_value(variable_name, value: [str, list], filename, type_variable='str', with_comma=True):
    if type_variable == '':
        raise ValueError('Type of variable must variable')

    if type_variable not in ['str', 'list', 'dict']:
        raise ValueError('type_variable must be str or list or dict')

    if not with_comma:
        change_str_variable_value(variable_name, value, filename, with_comma=False)
    elif type_variable == 'str':
        change_str_variable_value(variable_name, value, filename)
    elif type_variable == 'list':
        change_list_variable_value(variable_name, value, filename)


def change_str_variable_value(variable_name, value, filename, with_comma=True):
    with open(filename, "r") as f:
        content = f.read()

    # Match: variable_name = "old_value" (handling spaces & comments)
    pattern = rf"^\s*{variable_name}\s*=\s*.*?"
    replacement = f'{variable_name} = "{value}"' if with_comma else f'{variable_name} = {value}'

    if re.search(pattern, content, re.MULTILINE):
        modified_content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
    else:
        # If the variable doesn't exist, append it at the end
        modified_content = content + f'\n{replacement}\n'

    with open(filename, "w") as f:
        f.write(modified_content)


def create_env_file(folder_path, env_vars):
    """
    Creates a .env file in the specified folder and writes environment variables to it.

    :param folder_path: The directory where .env should be created.
    :param env_vars: A dictionary of environment variables to write.
    """
    # Ensure the folder exists
    os.makedirs(folder_path, exist_ok=True)

    # Define the file path
    env_file_path = os.path.join(folder_path, ".env")

    # Write environment variables to the file
    with open(env_file_path, "w") as f:
        for key, value in env_vars.items():
            f.write(f"{key}={value}\n")

    print(f".env file created successfully at {env_file_path}")


def add_variable_value(variable_name, value, filename):
    """
    Add a variable to the file with the specified value
    :param variable_name: The name of the variable to add the file.
    :param value: A value of variable.
    :param filename: The path of the file to modifying
    """
    with open(filename, "r") as f:
        content = f.readlines()

    content.append(f"{variable_name} = {value}\n")

    with open(filename, "w") as f:
        f.writelines(content)


def change_list_variable_value(variable_name, value: [str, list], filename):
    with open(filename, "r") as f:
        content = f.read()

    # Trouver la liste actuelle
    match = re.search(rf'{variable_name}\s*=\s*(\[[^\]]*\])', content, re.MULTILINE)
    if match:
        actual_list = ast.literal_eval(match.group(1))  # Convertir en liste Python
        if isinstance(value, str):
            if value not in actual_list:
                actual_list.append(value)

        if isinstance(value, list):
            actual_list = actual_list + value

        # Replace file content
        content_modified = content.replace(match.group(1), str(actual_list))

        with open(filename, "w") as f:
            f.write(content_modified)
