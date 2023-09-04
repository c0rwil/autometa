from subprocess import check_call, check_output
from sys import executable
from os import path
import toml as toml


class MetadataTOML(object):
    """ An object to hold v
    """

    # PIP_FREEZE = [executable, 'm', 'pip', 'freeze']
    __attrs__ = [
        "source_file_path",
        "exclusions_file_path",
        "dependencies",
        "exclusions",
        "metadata"
        ]

    def __init__(self, absolute_file_path: str, dependencies=None, exclusions_files_path: str = None,
                 exclusions=None):
        if dependencies is None:
            dependencies = []
        if exclusions is None:
            exclusions = []
        try:
            if path.exists(absolute_file_path):
                self.source_file_path = absolute_file_path
                self.dependencies = dependencies
                self.exclusions_files_path = exclusions_files_path
                self.exclusions = exclusions
                self.metadata = None
            else:
                raise Exception(f"Source file path {absolute_file_path} does not exist.")
        except Exception as exc:
            raise Exception(f"Exception raised: {exc}")

    def get_source_file_path(self):
        sfp = self.source_file_path
        return sfp

    def get_file_metadata(self):
        md = self.metadata
        return md

    def get_dependencies(self):
        gd = self.dependencies
        return gd

    def get_exclusions(self):
        ge = self.exclusions
        return ge

    def set_metadata_from_toml(self, toml_var: str = "META_TOML"):
        """ Returns metadata toml from file into a variable for use by script
        :param toml_var: variable name that is storing toml string
        :return: meta toml
        """
        meta_toml = ""
        try:
            source_file_path = self.source_file_path
            if path.exists(source_file_path):
                with open(source_file_path, 'r') as file:
                    line = file.readline()
                    while line:
                        if toml_var in line:
                            line = file.readline()
                            while '\"\"\"' not in line:
                                meta_toml += line
                                line = file.readline()
                            break
                        else:
                            line = file.readline()
        except Exception as exc:
            print(f"error while trying to read file's metadata, exception: \n {exc}")
        finally:
            derived_toml = []
            try:
                derived_toml = toml.loads(meta_toml)
            except toml.TomlDecodeError:
                print("Error decoding TOML from file")
            self.__setattr__(self.metadata, derived_toml)

    def set_dependencies(self, toml_table_key: str = "project", toml_table_value: str = "dependencies"):
        """
            :param toml_table_value: variable name in toml that you want to pull a list from
            :param toml_table_key: subheading / table name in TOML holding the dependencies variable
            :return: list of strings, pip-package install-list if present
        """
        dependencies = []
        derived_metadata = self.get_file_metadata()
        try:
            if toml_table_key in derived_metadata and toml_table_value in derived_metadata[toml_table_key]:
                dependencies = derived_metadata[toml_table_key][toml_table_value]
        except Exception as exc:
            raise Exception(f"Failed to set dependencies, Exception: {exc}")
        if dependencies:
            self.__setattr__(self.dependencies, dependencies)
        else:
            print("Dependencies list is empty")

    def pip_install_dependencies(self, dependencies: list):
        """ attempts to pip install packages in dependencies
            :param dependencies: list of pypi package names to install
        """
        dependencies.append(self.get_dependencies())
        for dependency in dependencies:
            check_call([executable, '-m', 'pip', 'install', dependency])
        reqs = check_output([executable, 'm', 'pip', 'freeze'])

        installed_packages = [r.decode().split("==")[0] for r in reqs.split()]
        for dependency in dependencies:
            if dependency not in installed_packages:
                raise Exception(f"failed to pip install {dependency}")

    def pip_uninstall_dependencies(self, dependencies: list, exclusions: list):
        """attempts to pip uninstall packages listed
            :param exclusions: list of pypi packages to never uninstall
            :param dependencies: list of pypi package names to install
        """

        dependencies.append(self.get_dependencies())
        exclusions.append(self.get_exclusions())
        uninstall_list = []

        for dependency in dependencies:
            if dependency not in exclusions:
                uninstall_list.append(dependency)

        for dependency in uninstall_list:
            check_call([executable, '-m', 'pip', 'uninstall', dependency, '-y'])
        reqs = check_output([executable, 'm', 'pip', 'freeze'])

        installed_packages = [r.decode().split("==")[0] for r in reqs.split()]
        for dependency in uninstall_list:
            if dependency in installed_packages and dependency in uninstall_list:
                raise Exception(f"failed to pip uninstall {dependency}")
