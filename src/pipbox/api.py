"""pipbox.api"""
import utils


def pip_install_dependencies(dependencies):
    return utils.pip_install_dependencies(dependencies=dependencies)


def read_file_metadata_toml(absolute_file_path):
    return utils.read_file_metadata_toml(absolute_file_path=absolute_file_path)


def read_dependencies_from_toml(loaded_toml):
    return utils.read_dependencies_from_metadata_toml(derived_toml=loaded_toml)


def pip_uninstall_dependencies(dependencies, exclusions):
    return utils.pip_uninstall_dependencies(dependencies=dependencies, exclusions=exclusions)
