# from subprocess import check_call, check_output
# from sys import executable
# from os import path
# import toml as toml
#
# PIP_FREEZE = [executable, 'm', 'pip', 'freeze']
#
#
# def fetch_file_metadata_toml(absolute_file_path: str, toml_var: str = "META_TOML"):
#     """Returns metadata toml from file into a variable for use by script
#     :param toml_var: variable name that is storing toml string
#     :param absolute_file_path: path/to/file
#     :return: meta toml
#     """
#     meta_toml = ""
#     try:
#         if path.exists(absolute_file_path):
#             with open(absolute_file_path, 'r') as file:
#                 line = file.readline()
#                 while line:
#                     if toml_var in line:
#                         line = file.readline()
#                         while '\"\"\"' not in line:
#                             meta_toml += line
#                             line = file.readline()
#                         break
#                     else:
#                         line = file.readline()
#     except Exception as exc:
#         print(f"error while trying to fetch file metadata, exception: \n {exc}")
#     finally:
#         derived_toml = []
#         try:
#             derived_toml = toml.loads(meta_toml)
#         except toml.TomlDecodeError:
#             print("Error decoding TOML from file")
#         return derived_toml
#
#
# def fetch_dependencies_from_metadata_toml(derived_toml, toml_table_key: str = "project",
#                                           toml_table_value: str = "dependencies"):
#     """
#     :param toml_table_value: variable name in toml that you want to pull a list from
#     :param toml_table_key: subheading / table name in TOML holding the dependencies variable
#     :param derived_toml: ingested metadata toml
#     :return: list of strings, pip-package install-list if present
#     """
#     dependencies = []
#     try:
#         if toml_table_key in derived_toml and toml_table_value in derived_toml[toml_table_key]:
#             dependencies = derived_toml[toml_table_key][toml_table_value]
#     except Exception as exc:
#         raise Exception(f"Failed to fetch dependencies: {exc}")
#     if dependencies:
#         return dependencies
#
#
# def pip_install_dependencies(dependencies: list):
#     """ attempts to pip install packages in dependencies
#     :param dependencies: list of pypi package names to install
#     """
#     for dependency in dependencies:
#         check_call([executable, '-m', 'pip', 'install', dependency])
#     reqs = check_output(PIP_FREEZE)
#
#     installed_packages = [r.decode().split("==")[0] for r in reqs.split()]
#     for dependency in dependencies:
#         if dependency not in installed_packages:
#             raise Exception(f"failed to pip install {dependency}")
#
#
# def pip_uninstall_dependencies(dependencies: list, exclusions: list = None):
#     """ attempts to pip uninstall packages listed
#     :param exclusions: list of pypi packages to never uninstall
#     :param dependencies: list of pypi package names to install
#     """
#     uninstall_list = []
#     for dependency in dependencies:
#         if dependency not in exclusions:
#             uninstall_list.append(dependency)
#
#     for dependency in uninstall_list:
#         check_call([executable, '-m', 'pip', 'uninstall', dependency, '-y'])
#     reqs = check_output(PIP_FREEZE)
#
#     installed_packages = [r.decode().split("==")[0] for r in reqs.split()]
#     for dependency in uninstall_list:
#         if dependency in installed_packages and dependency in uninstall_list:
#             raise Exception(f"failed to pip uninstall {dependency}")
#
#
# def fetch_dependencies_and_pip_install(absolute_file_path: str, toml_var_name: str = "META_TOML",
#                                        toml_table_key: str = "project",
#                                        toml_table_value: str = "dependencies"):
#     try:
#         fetched_toml = fetch_file_metadata_toml(absolute_file_path=absolute_file_path, toml_var=toml_var_name)
#         dependency_list = fetch_dependencies_from_metadata_toml(derived_toml=fetched_toml,
#                                                                 toml_table_key=toml_table_key,
#                                                                 toml_table_value=toml_table_value)
#         pip_install_dependencies(dependencies=dependency_list)
#         print(f"Successfully installed all dependencies...\n {dependency_list}")
#     except Exception as exc:
#         print(f"exception occurred: \n {exc}")
#
#
# def fetch_dependencies_and_pip_uninstall(absolute_file_path: str, toml_var_name: str = "META_TOML",
#                                          toml_table_key: str = "project",
#                                          toml_table_value: str = "dependencies",
#                                          excluded_dependencies_path: str = None):
#     try:
#         fetched_toml = fetch_file_metadata_toml(absolute_file_path=absolute_file_path, toml_var=toml_var_name)
#         dependency_list = fetch_dependencies_from_metadata_toml(derived_toml=fetched_toml,
#                                                                 toml_table_key=toml_table_key,
#                                                                 toml_table_value=toml_table_value)
#         exclusions_list = []
#         if excluded_dependencies_path:
#             exclusions_toml = fetch_file_metadata_toml(absolute_file_path=excluded_dependencies_path,
#                                                        toml_var=toml_var_name)
#             exclusions_list = fetch_dependencies_from_metadata_toml(derived_toml=exclusions_toml,
#                                                                     toml_table_key=toml_table_key,
#                                                                     toml_table_value=toml_table_value)
#         pip_uninstall_dependencies(dependencies=dependency_list, exclusions=exclusions_list)
#         print(f"Successfully installed all dependencies...\n {dependency_list}")
#     except Exception as exc:
#         print(f"exception occurred: \n {exc}")
