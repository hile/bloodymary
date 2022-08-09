# Bloodymary blood pressure data loader

This module loades blood pressure data for viewing.

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
bp.records.load('~/Downloads/text-EB45B558F3EA-1.txt')
print(f'last record {bp.records.last}')
print('\n'.join(f'  {record}' for record in bp.records))
```
