"""pipbox.api"""
from . import utils


def pip_install_dependencies(dependencies):
    return utils.pip_install_dependencies(dependencies=dependencies)


def pip_uninstall_dependencies(dependencies, exclusions=None):
    return utils.pip_uninstall_dependencies(dependencies=dependencies, exclusions=exclusions)


def fetch_file_metadata_toml(absolute_file_path, toml_var="META_TOML"):
    return utils.fetch_file_metadata_toml(absolute_file_path=absolute_file_path, toml_var=toml_var)


def fetch_dependencies_from_toml(loaded_toml, toml_table_key: str = "project", toml_table_value: str = "dependencies"):
    return utils.fetch_dependencies_from_metadata_toml(derived_toml=loaded_toml, toml_table_key=toml_table_key,
                                                       toml_table_value=toml_table_value)


def fetch_dependencies_and_pip_install(absolute_file_path: str, toml_var_name: str = "META_TOML",
                                       toml_table_key: str = "project",
                                       toml_table_value: str = "dependencies"):
    return utils.fetch_dependencies_and_pip_install(absolute_file_path=absolute_file_path, toml_var_name=toml_var_name,
                                                    toml_table_key=toml_table_key,
                                                    toml_table_value=toml_table_value)


def fetch_dependencies_and_pip_uninstall(absolute_file_path: str, toml_var_name: str = "META_TOML",
                                         toml_table_key: str = "project",
                                         toml_table_value: str = "dependencies",
                                         excluded_dependencies_path: str = None):
    return utils.fetch_dependencies_and_pip_uninstall(absolute_file_path=absolute_file_path,
                                                      toml_var_name=toml_var_name, toml_table_key=toml_table_key,
                                                      toml_table_value=toml_table_value,
                                                      excluded_dependencies_path=excluded_dependencies_path)
