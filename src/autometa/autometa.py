from subprocess import check_call, check_output
from sys import executable
from os import path
from autometa.util import dictify


class Autometa:
    """ An object to hold necessary attributes for parsing a variety of metadata
    """

    __attrs__ = [
        "source_file_path",
        "exclusions_file_path",
        "dependencies",
        "exclusions",
        "metadata",
        "preinstalled_packages",
        ]

    def __init__(self, absolute_file_path: str = "", dependencies=None, exclusions_files_path: str = "",
                 exclusions=None):
        """

        :param absolute_file_path: required to instantiate object, path to file to parse from
            #TODO: make this recursively append files from directory instead of 1 file?
        :param dependencies: can be added manually or will be populated later using class functions
        :param exclusions_files_path: optional filepath to excluded_from_uninstall packages
        :param exclusions: can be added manually in instantiation as a list of strings, or populated by class
        """

        if dependencies is None:
            dependencies = []
        if exclusions is None:
            exclusions = []
        try:
            if absolute_file_path != "":    # if absolute file path is not defaulted, attempt to pass in file path
                if path.exists(absolute_file_path):  # check if path to file actually exists...
                    self.source_file_path = absolute_file_path  # set if user input path verified
                else:
                    raise Exception(f"Source file path does not exist.")
            else:
                self.source_file_path = None
                print("No absolute file path was passed... instantiating autometa object in user input mode")

            self.dependencies = dependencies
            self.exclusions_files_path = exclusions_files_path
            self.exclusions = exclusions
            self.metadata = None
            self.preinstalled_packages = None
        except Exception as exc:
            raise Exception(f"Exception raised: {exc}")
        self.set_preinstalled_packages()

    def get_source_file_path(self):
        sfp = self.source_file_path
        return sfp

    def get_preinstalled_packages(self):
        prepackaged = self.preinstalled_packages
        return prepackaged

    def get_metadata(self):
        md = self.metadata
        return md

    def get_dependencies(self):
        gd = self.dependencies
        return gd

    def get_exclusions(self):
        ge = self.exclusions
        return ge

    def set_preinstalled_packages(self):
        reqs = check_output([executable, '-m', 'pip', 'freeze'])
        preinstalled = [r.decode().split("==")[0] for r in reqs.split()]
        preinstalled = [r.lower() for r in preinstalled]
        self.preinstalled_packages = preinstalled

    def set_source_file_path(self, absolute_filepath=""):
        if path.exists(absolute_filepath):  # check if path to file actually exists...
            self.source_file_path = absolute_filepath  # set if user input path verified
            return True  # to validate if setting filepath was successful or not
        else:
            print(f"Absolute file path {absolute_filepath} does not exist... failed to change self.source_file_path")
            return False

    def set_metadata(self, metadata):
        self.metadata = metadata

    def set_dependencies(self, dependencies: list):
        self.dependencies = dependencies

    def update_metadata(self, toml_var: str = "META_TOML"):
        """ set metadata toml from file into a variable for use by autometa object

        :param toml_var: variable name that is storing metadata toml string
        """
        derived_toml = dictify(absolute_file_path=self.get_source_file_path(), toml_var=toml_var)
        self.set_metadata(derived_toml)

    def parse_dependencies(self, toml_table_key: str = "project", toml_table_value: str = "dependencies"):
        """

        :param toml_table_value: variable name in toml that you want to pull a list from
        :param toml_table_key: subheading / table name in TOML holding the dependencies variable

        :return: list of strings, pip-package install-list if present
        """
        dependencies = []
        if not self.metadata:
            self.update_metadata()
            print(f"metadata wasn't populated, doing now... {self.metadata}")
        derived_metadata = self.get_metadata()
        if derived_metadata:
            try:
                if toml_table_key in derived_metadata and toml_table_value in derived_metadata[toml_table_key]:
                    dependencies = derived_metadata[toml_table_key][toml_table_value]
            except Exception as exc:
                raise Exception(f"Failed to set dependencies, Exception: {exc}")
            if dependencies:
                self.set_dependencies(dependencies)
                print(f"Dependencies successfully parsed: {self.get_dependencies()}")
            else:
                print("Dependencies list is empty")

    def pip_install_dependencies(self, dependencies: list = []):
        """ attempts to pip install packages in dependencies

        :param dependencies: list of pypi package names to install
        """
        obj_dependencies = self.get_dependencies()
        preinstalled = self.get_preinstalled_packages()

        for dependency in dependencies:
            obj_dependencies.append(dependency)

        for dependency in obj_dependencies:
            check_call([executable, '-m', 'pip', 'install', dependency])

        reqs = check_output([executable, '-m', 'pip', 'freeze'])
        installed_packages = [r.decode().split("==")[0] for r in reqs.split()]

        for dependency in obj_dependencies:
            if dependency.lower() not in installed_packages:
                raise Exception(f"failed to pip install {dependency}")
            else:
                newly_added = list(set(installed_packages) - set(preinstalled))
                self.set_dependencies(newly_added)


    def pip_uninstall_dependencies(self, dependencies: list = [], exclusions: list = []):
        """attempts to pip uninstall packages listed

        :param exclusions: list of pypi packages to never uninstall
        :param dependencies: list of pypi package names to install
        """
        for dependency in self.get_dependencies():
            dependencies.append(dependency.lower())
        for dependency in self.get_exclusions():
            exclusions.append(dependency.lower())

        uninstalls_attempted_list = []
        pre_installed_packages = self.get_preinstalled_packages()
        uninstall_set = list(set(dependencies) - set(pre_installed_packages) - set(exclusions))
        for dependency in uninstall_set:
            check_call([executable, '-m', 'pip', 'uninstall', dependency, '-y'])
            uninstalls_attempted_list.append(dependency)

        reqs = check_output([executable, '-m', 'pip', 'freeze'])
        installed_packages = [r.lower().decode().split("==")[0] for r in reqs.split()]

        for dependency in uninstall_set:
            if dependency.lower() in uninstalls_attempted_list and dependency in installed_packages:
                raise Exception(f"failed to pip uninstall {dependency}")
