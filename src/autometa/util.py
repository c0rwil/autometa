import yaml
import json
import toml as toml


def tomlify(absolute_file_path: str, toml_var:str = "META_TOML"):
    toml_contents = ""
    derived_toml = dict()
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
            toml_contents = toml.load(toml_file)
    elif absolute_file_path.endswith('.py'):
        toml_contents = load_toml_from_meta_toml_str(absolute_file_path=absolute_file_path, toml_var=toml_var)
    try:
        print(toml_contents)
        derived_toml = toml.loads(toml_contents)
        print(derived_toml)
    except toml.TomlDecodeError:
        print("Error decoding TOML from file")
    return derived_toml


def load_toml_from_meta_toml_str(absolute_file_path:str, toml_var:str = "META_TOML"):
    """

    :rtype: string
    """
    toml_contents = ""
    try:
        with open(absolute_file_path, 'r') as file:
            line = file.readline()
            while line:
                if toml_var in line:
                    line = file.readline()
                    while '\"\"\"' not in line:
                        toml_contents += line
                        print(toml_contents)
                        line = file.readline()
                        break
                else:
                    line = file.readline()
    except Exception as exc:
        print(f"Error while trying to read file's metadata, exception: \n {exc}")
    finally:
        print(toml_contents)
        return toml_contents
