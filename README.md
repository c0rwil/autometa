# Autometa

**Autometa** is a simple & focused solution to reading metadata from a variety of file formats into a python class obj

```python
>>> import autometa
>>> r = requests.get('https://httpbin.org/basic-auth/user/pass', auth=('user', 'pass'))
>>> r.status_code
200
>>> r.headers['content-type']
'application/json; charset=utf8'
>>> r.encoding
'utf-8'
>>> r.text
'{"authenticated": true, ...'
>>> r.json()
{'authenticated': True, ...}
```

autometa allows you to easily parse in data from .json, .yaml/.yml, .toml, and .py files into a dictionary object in 
    a python class object with a helper function to parse in a list of dependencies listed in said files.

## Installing Requests and Supported Versions

autometa is available on PyPI:

```console
$ python -m pip install autometa
```

## Supported Features & Best–Practices

Requests is ready for the demands of building robust and reliable HTTP–speaking applications, for the needs of today.

- Parse in a variety of formatted data into an object holding a dictionary of parsed data using a single function call
- Pip install / uninstall a list of user-input or file-fed dependencies

## Cloning the repository

```shell
git clone https://github.com/mikl-o/autometa.git
```
