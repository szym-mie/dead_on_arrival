import os
from pathlib import Path
from sys import argv


def get_param(index):
    return argv[index + 1]


def read_script_from_file(filename, params):
    with open(filename, "r") as f:
        script = f.read()
        for param_key, param_replace in params.items():
            script = script.replace(f"${param_key}", str(param_replace))

        return script


def find_files(pattern, search_filepath):
    search_path = Path(search_filepath)
    return map(lambda p: (p, p.relative_to(search_path)),
               Path(search_path).glob(pattern))


def create_filepath(filepath):
    try:
        Path(filepath).parent.mkdir(parents=True)
        print('filepath created')
    except FileExistsError:
        print('filepath already present')


def exec_command(command):
    os.system(command.replace("\n", " "))
