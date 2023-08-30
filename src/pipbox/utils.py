import subprocess
import sys
import os
import toml as toml


def read_file_metadata_toml(absolute_file_path: str):
    """Reads metadata toml from file into a variable for use by script
    :param absolute_file_path: path/to/file
    :return: meta toml
    """
    meta_toml = ""
    try:
        if os.path.exists(absolute_file_path):
            with open(absolute_file_path, 'r') as file:
                line = file.readline()
                while line:
                    if "META_TOML" in line:
                        line = file.readline()
                        while '\"\"\"' not in line:
                            meta_toml += line
                            line = file.readline()
                        break
                    else:
                        line = file.readline()
    except Exception as exc:
        print(f"error while trying to read file metadata, exception: \n {exc}")
        return 0
    finally:
        if meta_toml.strip() == "":
            return 0
        try:
            derived_toml = toml.loads(meta_toml)
        except toml.TomlDecodeError:
            print("Error decoding TOML from file")
            return 0
        return derived_toml


def read_dependencies_from_metadata_toml(derived_toml):
    """
    :param derived_toml: ingested metadata toml
    :return: list of strings, pip-package install-list if present
    """
    dependencies = ""
    try:
        if 'project' in derived_toml and 'dependencies' in derived_toml['project']:
            dependencies = derived_toml['project']['dependencies']
    except Exception as exc:
        raise Exception(f"Failed to read dependencies: {exc}")
    if dependencies:
        return dependencies


def pip_install_dependencies(dependencies: list):
    """ attempts to pip install packages in dependencies
    :param dependencies: list of pypi package names to install
    """
    for dependency in dependencies:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', dependency])
    reqs = subprocess.check_output([sys.executable, 'm', 'pip', 'freeze'])

    installed_packages = [r.decode().split("==")[0] for r in reqs.split()]
    for dependency in dependencies:
        if dependency not in installed_packages:
            raise Exception(f"failed to pip install {dependency}")


def pip_uninstall_dependencies(dependencies: list, exclusions: list = None):
    """ attempts to pip uninstall packages listed
    :param exclusions:
    :param dependencies: list of pypi package names to install
    """
    for dependency in dependencies:
        if dependency not in exclusions:
            subprocess.check_call([sys.executable, '-m', 'pip', 'uninstall', dependency, '-y'])
    reqs = subprocess.check_output([sys.executable, 'm', 'pip', 'freeze'])

    installed_packages = [r.decode().split("==")[0] for r in reqs.split()]
    for dependency in dependencies:
        if dependency in installed_packages and dependency not in exclusions:
            raise Exception(f"failed to pip uninstall {dependency}")
