"""
autometa.api
~~~~~~~~~~~~

This module implements the Autometa API.

"""
from . import autometa


def fetch_metadata(absolute_file_path: str, toml_var: str = "META_TOML"):
    """ parses out metadata from absolute_file_path and returns a metadata dictionary object

    :param absolute_file_path: mandatory to pass, filepath to fetch data from
    :param toml_var: name for the toml-formatted string variable (if reading from .py)
    """
    if absolute_file_path:
        automd = autometa.Autometa(absolute_file_path=absolute_file_path)
        automd.update_metadata(toml_var=toml_var)
        return automd.get_metadata()
    else:
        raise Exception("Didn't pass in a valid filepath string")


def fetch_dependencies(absolute_file_path: str, toml_var: str = "META_TOML",
                       toml_table_key: str = "project", toml_table_value: str = "dependencies"):
    """ parses out dependencies from a file, populating Autometa.metadata if empty before call
    :param absolute_file_path: requires a filepoth to fetch data from
    :param toml_var: name for the toml-formatted string variable (if reading from .py)
    :param toml_table_value: variable name in toml that you want to pull a list from
    :param toml_table_key: subheading / table name in TOML holding the dependencies variable

    :return: list of strings, pip-package install-list if present
    """
    if absolute_file_path:
        automd = autometa.Autometa(absolute_file_path=absolute_file_path)
        automd.update_metadata(toml_var=toml_var)
        automd.parse_dependencies(toml_table_key=toml_table_key, toml_table_value=toml_table_value)
        return automd.get_dependencies()
    else:
        raise Exception("Didn't pass in a valid filepath string")


def pip_install(manual_input_list: list = None, absolute_file_path: str = "", toml_var: str = "META_TOML",
                toml_table_key: str = "project", toml_table_value: str = "dependencies"):
    """ pip installs dependencies listed in Autometa.dependencies or in user-input list of dependency names

    """
    try:
        if absolute_file_path:
            automd = autometa.Autometa(absolute_file_path=absolute_file_path)
            automd.update_metadata(toml_var=toml_var)
            automd.parse_dependencies(toml_table_key=toml_table_key, toml_table_value=toml_table_value)
            if manual_input_list:
                automd.pip_install_dependencies(dependencies=manual_input_list)
            else:
                automd.pip_install_dependencies(dependencies=[])
        elif manual_input_list:
            automd = autometa.Autometa(dependencies=manual_input_list)
            automd.pip_install_dependencies(automd.get_dependencies())
        else:
            print("Didn't pass anything into the function call...")
    except Exception as exc:
        raise Exception(f"{exc}")


def pip_uninstall(absolute_file_path: str = "", manual_input_list: list = [], exclusions_list: list = [], toml_var: str = "META_TOML",
                  toml_table_key: str = "project", toml_table_value: str = "dependencies"):
    """ pip uninstalls dependencies listed in Autometa.dependencies, skipping packages in exclusions list if it exists

    """
    try:
        if absolute_file_path != "":
            automd = autometa.Autometa(absolute_file_path=absolute_file_path,dependencies=manual_input_list,
                                       exclusions=exclusions_list)
            automd.update_metadata(toml_var=toml_var)
            automd.parse_dependencies(toml_table_key=toml_table_key, toml_table_value=toml_table_value)
            automd.pip_uninstall_dependencies()
        elif manual_input_list:
            automd = autometa.Autometa(dependencies=manual_input_list, exclusions=exclusions_list)
            automd.pip_uninstall_dependencies()
        else:
            print("Didn't pass anything into the function call...")
    except Exception as exc:
        raise Exception(f"{exc}")

