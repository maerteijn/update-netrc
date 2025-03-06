# update-netrc
A simple command line utility to update netrc credentials.

[![CI](https://github.com/maerteijn/update-netrc/actions/workflows/ci.yml/badge.svg)](https://github.com/maerteijn/update-netrc/actions/workflows/ci.yml)
![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)
![PyPI version](https://badge.fury.io/py/update-netrc.svg?dummy=unused)
![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)
![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)
![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)
![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)
![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)
![No Dependencies](https://img.shields.io/badge/no%20dependencies-orange)


## Usage
```bash

$  update-netrc --help
usage: update-netrc [-h] [--netrc-path NETRC_PATH] {update} ...

Default .netrc path: /Users/martijn/.netrc

positional arguments:
  {update}

options:
  -h, --help            show this help message and exit
  --netrc-path NETRC_PATH
                        Specify an alternative location for the used netrc file
```

```bash
$ update-netrc update --help
usage: update-netrc update [-h] [--login LOGIN] [--account ACCOUNT] [--password PASSWORD] host

positional arguments:
  host                 Selects the host (machine) you want to update

options:
  -h, --help           show this help message and exit
  --login LOGIN        Update the login of specified host
  --account ACCOUNT    Update the account of the specified host
  --password PASSWORD  Update the password of the specified host
```

## Examples

To update the password of the `localhost` machine:

```sh
$ update-netrc update localhost --password my-secret-password
```

To update the login of the `default` machine
```sh
$ update-netrc update default --login my-login
```

You can also add new entries, `--login` and `--password` are then required:
```sh
$ update-netrc update my-new-host --login my-login --password my-password
```

## Installation

```sh
pip install update-netrc
```

## Development setup

### First clone this repository
```
git clone https://github.com/maerteijn/update-netrc.git
```

### Install the python project
```bash
pyenv virtualenv update-netrc  # or your alternative to create a venv
pyenv activate update-netrc
make install
```

### Linting
`ruff` and `mypy` are installed and configured
```bash
make lint
```

### Formatting

`ruff` is configured
```bash
make format
```

### Test

Pytest with coverage is default enabled
```bash
make cov
```
