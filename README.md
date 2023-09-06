# Autometa

**Autometa** is a simple & focused solution to reading metadata from a variety of file formats into a python class obj

```python
>>> from autometa.autometa import Autometa
>>> md = Autometa(absolute_file_path="/example/file/path")
>>> md.update_metadata(toml_var="META_TOML") #toml_var only needed if you are reading a toml string from a .py 

>>> md.get_metadata()
{'project': {'dependencies': ['example1', 'example2', 'example3']}}

>>> md.parse_dependencies()
"Dependencies successfully parsed: ['example1', 'example2', 'example3']"

>>>md.pip_install_dependencies(dependencies=["additionalPkg1", "additionalPkg2"])
'''Collecting additionalPkg1 -> install attempt...  Collecting additionalPkg2 -> install attempt...
   Collecting example1... -> install attempt, Collecting example2 -> install attempt... ,
   Collecting example3 -> install attempt...  '''

>>> md.pip_uninstall_dependencies(exclusions=["additionalPkg1","example1"])
'''Found existing installation: example2 -> Uninstalling example2...
   Found existing installation: example3 -> Uninstalling example3...
'''
```

autometa allows you to easily parse in data from .json, .yaml/.yml, .toml, and .py files into a dictionary object in 
    a python class object with a helper function to parse in a list of dependencies listed in said files.

## Installing autometa

autometa is available on PyPI:

```console
$ python -m pip install autometa
```

## Features & Best Practices

Requests is ready for the demands of building robust and reliable HTTP–speaking applications, for the needs of today.

- Parse in a variety of formatted data into an object holding a dictionary of parsed data using a single function call
- Pip install / uninstall a list of user-input or file-fed dependencies
- By default, dependencies are searched for under a structure that looks like this:
  - for .json:
    {
        "project":
                {
                    "dependencies": ['example1', 'example2', 'example3']
                }
    }

  - for .yaml/.yml:
    project:
        dependencies: ['example1', 'example2', 'example3']
  
  - for .toml
    [project]
    dependencies = ["scrapy", "requests", "numpy"]

  - for .py
    META_TOML = '''
    [project]
    dependencies = ["man", "thing", "wahoo"]
    '''
    
## Cloning the repository

```shell
git clone https://github.com/mikl-o/autometa.git
```
