import yaml
import json
import toml as toml


def dictify(absolute_file_path: str, toml_var: str = "META_TOML"):
    """Helper script to extract data from .json, .py, .yaml, .toml files and loads into a python dict

    :param absolute_file_path: absolute path to file to parse data from
    :param toml_var: name of variable you store a toml string into (optional)

    :return: dictionary extracted by dictify
    """
    toml_contents = ""
    derived_metadata = dict()
    if absolute_file_path.endswith('.yaml') or absolute_file_path.endswith('.yml'):
        with open(absolute_file_path, 'r') as yml_file:
            yaml_contents = yaml.safe_load(yml_file)
            toml_contents = toml.dumps(yaml_contents)
    elif absolute_file_path.endswith('.json'):
        with open(absolute_file_path, 'r') as json_file:
            json_contents = json.loads(json_file.read())
            toml_contents = toml.dumps(json_contents)
    elif absolute_file_path.endswith('.toml'):
        with open(absolute_file_path, 'r') as toml_file:
            toml_contents = toml.dumps(toml.load(toml_file))
    elif absolute_file_path.endswith('.py'):
        toml_contents = load_toml_from_meta_toml_str(absolute_file_path=absolute_file_path, toml_var=toml_var)
    else:
        print("Invalid filepath type passed into absolute_file_path")
        return 0
    try:
        derived_metadata = toml.loads(toml_contents)
    except toml.TomlDecodeError:
        print("Error decoding TOML from file")
    return derived_metadata


def load_toml_from_meta_toml_str(absolute_file_path: str, toml_var: str = "META_TOML"):
    """Simple approach to parse out metadata toml declared in a string

    :param absolute_file_path: absolute path to file to parse data from
    :param toml_var: name of variable you store a toml string into (defaulted)

    :rtype: string
    """
    try:
        toml_contents: str = ""
        with open(absolute_file_path, 'r') as file:
            line = file.readline()
            while line:
                if toml_var in line:
                    line = file.readline()
                    while '\"\"\"' not in line:
                        toml_contents += line
                        line = file.readline()
                    break
                else:
                    line = file.readline()
    except Exception as exc:
        print(f"Error while trying to read file's metadata, exception: \n {exc}")
    finally:
        return toml_contents
