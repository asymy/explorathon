from pathlib import Path
import json
import sys


def init():
    global thermodeInfo, monitorInfo
    global thermode, monitor
    global gender, program
    thermodeInfo = json_read(Path('CalibrationFiles'), 'thermodeinfo')
    monitorInfo = json_read(Path('CalibrationFiles'), 'monitorinfo')
    thermode = ''
    monitor = ''
    gender = ''
    program = ''


def json_read(data_folder, fileName):
    DataFile = Path(data_folder / (fileName + '.json'))
    with open(DataFile, 'r') as filehandle:
        data = json.load(filehandle)
    return data
