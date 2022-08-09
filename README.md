![Unit Tests](https://github.com/hile/bloodymary/actions/workflows/unittest.yml/badge.svg)
![Style Checks](https://github.com/hile/bloodymary/actions/workflows/lint.yml/badge.svg)

# Bloodymary blood pressure data loader

This module loades blood pressure data for viewing.

# Installing the module

This module is available in published version from PyPI:

```
pip install bloodymary
```

It can also be installed with pip from github:

```bash
pip install git+https://github.com/hile/bloodymary
```

# Development instructions

To install this module in an isolated development virtualenv *~/.venv/bloodymary* you can
run following command:

```bash
make virtualenv
. ~/.venv/bloodymary/bin/activate
```

# Running unit tests and linters

Unit tests and style checks can be run either with a make rule or with tox.

Default rule for *make* runs style checks and unittests. The targets can be also run
individually.

Examples:

```bash
make
make lint
make unittest
```

Github Actions run the tests with *tox*.

Examples:

```bash
tox -e lint,unittest
tox -e lint
tox -e unittest
```

## File formats

Currently only supported file format is for the text exports from the IoS application
[Blood Pressure](https://apps.apple.com/us/app/blood-pressure-app-monitor/id1502279381)
that exports a trivial text file with no specific integrations.

New file formats are welcome.

## Configuring the file format

File format to use can be configured with environment variable *BLOODYMARY_FILE_FORMAT*. Valid
values for this variable can be seen in *bloodymary.constants.FileFormat' enum.

```bash
export BLOODYMARY_FILE_FORMAT=ios-blood-pressure
```

Currently only supported value is "*ios-blood-pressure*".

## Loading a data file

Example python commands to load a text data file, show last record and list all records

```python
from bloodymary.formats import BloodPressureData
bp = BloodPressureData('ios-blood-pressure')
bp.records.load('~/Downloads/text-ios-records.txt')
print(f'last record {bp.records.last}')
print('\n'.join(f'  {record}' for record in bp.records))
```

## Pandas support

Pandas dataframe for blood pressure records contains columns
*Time*, *Systolic*, *Diastolic* and *Pulse*.

Example to get a pandas Dataframe from a blood pressure data file:

```python
from bloodymary.formats import BloodPressureData
bp = BloodPressureData('ios-blood-pressure')
bp.records.load('~/Downloads/text-ios-records.txt')
dataframe = bp.get_dataframe()
```

Example to get a pandas Dataframe for last week's blood pressure data records:

```python
from datetime import datetime, timedelta
from bloodymary.formats import BloodPressureData
bp = BloodPressureData('ios-blood-pressure')
bp.records.load('~/Downloads/text-ios-records.txt')
limit = datetime.now() - timedelta(days=7)
dataframe = bp.get_dataframe(bp.records.filter(start_time=limit))
```
